# 🍉 Fruit Ninja — Hand Tracking Edition

A real-time, computer-vision take on the classic Fruit Ninja game. Use your **index finger** as the blade — detected live through your webcam — to slice fruits before they escape the screen.

Built with Python, OpenCV, and MediaPipe.

---

## Demo

> Point your index finger at the colored circles flying across the screen and slice through them!

---

## Features

- 🖐️ **Real-time hand tracking** via MediaPipe (no controller needed)
- 🍎 **Randomised fruit spawning** with colorful circles
- ⚡ **Dynamic difficulty** — speed and spawn rate increase every 1 000 points
- 🎯 **Slash trail** that follows your fingertip
- 📊 **Live HUD** showing Score, Lives, Level, and FPS

---

## Requirements

| Dependency | Version |
|---|---|
| Python | 3.8 + |
| OpenCV | ≥ 4.5 |
| MediaPipe | ≥ 0.9 |
| NumPy | ≥ 1.21 |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/FruitNinja.git
cd FruitNinja
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the game

```bash
python fruit_ninja.py
```

Press **`Q`** to quit at any time.

---

## How to Play

| Action | Result |
|---|---|
| Move index finger over a fruit | Slice it (+100 pts) |
| Let a fruit leave the screen | Lose a life |
| Reach 0 lives | Game over |
| Score multiples of 1 000 | Difficulty increases |

---

## Project Structure

```
FruitNinja/
├── fruit_ninja.py      # Main game script
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## How It Works

1. **Webcam feed** is captured and horizontally flipped (mirror mode).  
2. **MediaPipe Hands** detects landmark #8 — the index fingertip.  
3. The fingertip position is compared against every active fruit using Euclidean distance; a hit is registered when the distance is smaller than the fruit radius.  
4. A **polyline trail** is drawn by keeping a rolling buffer of recent fingertip positions.  
5. Difficulty scales by increasing vertical speed and spawn rate at each 1 000-point milestone.

---

## Roadmap

- [ ] Actual fruit images instead of solid circles  
- [ ] Bomb objects (slicing = instant game over)  
- [ ] High-score persistence  
- [ ] Start / pause / restart menu  
- [ ] Sound effects  

---

## License

MIT — feel free to fork, extend, and have fun with it.
