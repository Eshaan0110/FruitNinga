import cv2 as cv
import time
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

curr_Frame = 0
prev_Frame = 0
delta_Time = 0
FPS = 0

w = h = 0
slash_color = (255, 255, 255)

# Initialize the webcam
cap = cv.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Skipping frame")
        continue

    h, w, c = img.shape

    img = cv.cvtColor(cv.flip(img, 1), cv.COLOR_BGR2RGB)  # Flip and convert to RGB for MediaPipe
    results = hands.process(img)
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)  # Convert back to BGR for OpenCV display

    if results.multi_hand_landmarks:  # If hands are detected
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the landmarks and connections on the hand
            mp_drawing.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Track the index finger (landmark 8)
            for id, lm in enumerate(hand_landmarks.landmark):
                if id == 8:  # Index finger tip landmark
                    index_pos = (int(lm.x * w), int(lm.y * h))
                    cv.circle(img, index_pos, 18, slash_color, -1)

    # Calculate FPS
    curr_Frame = time.time()
    delta_Time = curr_Frame - prev_Frame
    if delta_Time > 0:
        FPS = int(1 / delta_Time)
    cv.putText(img, f"FPS: {FPS}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    prev_Frame = curr_Frame

    # Show the frame
    cv.imshow("Finger Tracker", img)

    # Press 'q' to quit
    if cv.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
