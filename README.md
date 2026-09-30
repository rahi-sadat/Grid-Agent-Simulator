# Grid-Agent-Simulator (RuleLab)

> **RuleLab** is an enhanced, interactive rule-based grid agent simulation built with Python and Tkinter (standard library only, zero external dependencies).

---

## 🌟 Key Features

- **Intuitive Dark UI**: Clean three-panel layout featuring the **Rule Engine**, **Simulation Grid**, and **Challenge Panel**.
- **8 Built-in Levels**: Progressive challenge curve spanning Starter, Easy, Medium, and Hard stages.
- **Challenge Objectives**: Real-time progress tracking for steps taken, unique cells explored, and required rule activations.
- **Agent Visuals**: Distinct movement trails for Red and Cyan agents with optional rule-number step indicators.
- **Interactive Controls**: Zoom controls, adjustable simulation speed slider, step-by-step mode, and keyboard shortcuts.
- **Custom Map Support**: Validate and load custom `.txt` grid environments or practice freely.
- **Zero Third-Party Dependencies**: Runs strictly on standard library Python 3 and Tkinter.

---

## 🎮 Keyboard Controls

| Key | Action |
| :--- | :--- |
| <kbd>Space</kbd> | Step forward once |
| <kbd>Enter</kbd> | Run / Pause simulation |
| <kbd>R</kbd> | Reset current level |
| <kbd>N</kbd> | Advance to next level |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ (make sure `tcl/tk and IDLE` is checked during Windows installation).

### Windows
Double-click `run_sim.bat` or run:
```bash
python agent_sim.py
```

### macOS / Linux
```bash
python3 agent_sim.py
```
> *Note for Linux users: If Tkinter is not pre-installed, install it via `sudo apt install python3-tk` (Debian/Ubuntu) or equivalent.*

---

## 🧪 Running Tests

Verify agent movement and rule mechanics using the built-in test suites:

- **Original Movement Regression Test**:
  ```bash
  python agent_sim.py --test
  ```

- **All Levels & Challenges Smoke Test**:
  ```bash
  python agent_sim.py --test-all
  ```

---

## 🗺️ Custom Map Format

Custom maps can be created as plain `.txt` files with rectangular, equal-width rows:

| Symbol | Description |
| :---: | :--- |
| `.` | Free cell |
| `#` | Obstacle |
| `~` | Void / blocked cell |
| `R` | Red agent starting position |
| `C` | Cyan agent starting position |

### Example Map (`sample_map.txt`)
```text
............
...######...
...#....#...
...#....#...
....R..C....
............
```