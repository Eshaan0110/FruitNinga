import cv2 as cv
import time
import random
import mediapipe as mp
import math
import numpy as np

# ── MediaPipe setup ──────────────────────────────────────────────────────────
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)

# ── Game config ───────────────────────────────────────────────────────────────
FRUIT_RADIUS = 30
SPAWN_RATE = 1          # fruits per second
INITIAL_SPEED = [0, 5]
SLASH_TRAIL_LENGTH = 19

# ── Game state ────────────────────────────────────────────────────────────────
score = 0
lives = 10
difficulty = 1
game_over = False
speed = INITIAL_SPEED.copy()

prev_frame_time = 0

slash_trail = np.array([[]], np.int32)
slash_color = (255, 255, 255)
next_spawn_time = 0
fruits = []

w = h = 0


# ── Helpers ───────────────────────────────────────────────────────────────────

def spawn_fruit():
    """Append a new fruit at a random x position near the bottom of the frame."""
    x = random.randint(15, 600)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    fruits.append({
        "color": color,
        "position": [x, 440],
    })


def update_fruits(frame, current_speed):
    """Move every fruit upward; remove those that leave the frame and deduct a life."""
    global lives

    for fruit in fruits[:]:
        x, y = fruit["position"]

        # Fruit escaped without being sliced
        if y < 20 or x > 650:
            lives -= 1
            fruits.remove(fruit)
            continue

        cv.circle(frame, (x, y), FRUIT_RADIUS, fruit["color"], -1)

        fruit["position"][0] += current_speed[0]
        fruit["position"][1] -= current_speed[1]


def distance(a, b):
    """Euclidean distance between two 2-D points."""
    return int(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))


def draw_hud(frame, fps):
    """Overlay score, lives, level and FPS on the frame."""
    cv.putText(frame, f"Score: {score}", (int(w * 0.35), 90),
               cv.FONT_HERSHEY_TRIPLEX, 1, (187, 212, 61), 3)
    cv.putText(frame, f"Level: {difficulty}", (int(w * 0.01), 90),
               cv.FONT_HERSHEY_TRIPLEX, 1, (187, 212, 61), 3)
    cv.putText(frame, f"Lives: {lives}", (200, 50),
               cv.FONT_HERSHEY_TRIPLEX, 0.8, (187, 212, 61), 2)
    cv.putText(frame, f"FPS: {fps}", (int(w * 0.82), 50),
               cv.FONT_HERSHEY_TRIPLEX, 0.6, (18, 24, 181), 2)


# ── Main loop ─────────────────────────────────────────────────────────────────

cap = cv.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        continue

    h, w, _ = img.shape

    # Hand tracking (MediaPipe expects RGB)
    img = cv.cvtColor(cv.flip(img, 1), cv.COLOR_BGR2RGB)
    results = hands.process(img)
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )

            for idx, lm in enumerate(hand_landmarks.landmark):
                if idx == 8:  # Index finger tip
                    tip = (int(lm.x * w), int(lm.y * h))

                    # Draw fingertip cursor
                    cv.circle(img, tip, 18, slash_color, -1)

                    # Grow slash trail
                    slash_trail = np.append(slash_trail, tip)
                    while len(slash_trail) >= SLASH_TRAIL_LENGTH:
                        slash_trail = np.delete(slash_trail, 0)

                    # Collision detection
                    for fruit in fruits[:]:
                        if distance(tip, fruit["position"]) < FRUIT_RADIUS:
                            score += 100
                            slash_color = fruit["color"]
                            fruits.remove(fruit)

        # Difficulty scaling: increase every 1 000 points
        if score > 0 and score % 1000 == 0:
            difficulty = int(score / 1000) + 1
            speed[0] = INITIAL_SPEED[0] * difficulty
            speed[1] = int(5 * difficulty / 2)

    # Draw slash trail
    trail = slash_trail.reshape((-1, 1, 2))
    cv.polylines(img, [trail], False, slash_color, 15)

    # FPS calculation
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_frame_time)) if prev_frame_time else 0
    prev_frame_time = curr_time

    draw_hud(img, fps)

    if lives <= 0:
        game_over = True

    if not game_over:
        if time.time() > next_spawn_time:
            spawn_fruit()
            next_spawn_time = time.time() + (1 / SPAWN_RATE)
        update_fruits(img, speed)
    else:
        cv.putText(img, "GAME OVER", (int(w * 0.1), int(h * 0.6)),
                   cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
        fruits.clear()

    cv.imshow("Fruit Ninja", img)

    if cv.waitKey(5) & 0xFF == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
