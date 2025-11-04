# 🧮 Math Adventures — AI-Powered Adaptive Learning Prototype

An adaptive math learning web app for children (ages 5–10) that dynamically adjusts difficulty based on each learner’s performance.  
Built with **Python + Streamlit**, featuring both **rule-based** and **ML-ready** adaptive engines.

---

## 🌟 Features

✅ Dynamic puzzle generation (Addition, Subtraction, Multiplication, Division)  
✅ Adaptive difficulty — Easy ↔ Medium ↔ Hard  
✅ Real-time performance tracking (accuracy, response time)  
✅ Per-user adaptive learning flow  
✅ Kid-friendly UI with emojis, colors, progress bar & confetti 🎉  
✅ Visual performance summary with **accuracy trend chart**  
✅ ML-ready logic for data-driven adaptation  
✅ Save sessions to CSV for long-term learning analytics  

---

## 🏗️ Architecture

![Architecture Diagram](./math_adventures_architecture.png)

**Core Modules**

| Module | Purpose |
|---------|----------|
| `main.py` | Streamlit interface and app flow |
| `puzzle_generator.py` | Creates random math questions per difficulty |
| `tracker.py` | Logs correctness, response time, and user data |
| `adaptive_engine.py` | Handles adaptive logic (Rule or ML) |
| `data/sessions.csv` | Stores session data for analytics & ML training |

---

## 🧠 Adaptive Logic

### Rule-based (default)

| Condition | Action |
|------------|---------|
| Accuracy ≥ 80% and Avg Time ≤ 5s | Increase difficulty |
| Accuracy ≤ 50% | Decrease difficulty |
| Otherwise | Keep the same |

### ML-based (optional)

- Uses **Logistic Regression** to predict next difficulty level from past data.  
- Trains automatically on `data/sessions.csv` when sufficient data exists.  
- Falls back to rule-based logic if data is missing (safe mode).

---


Contains:
- System architecture & adaptive flow diagram  
- Explanation of rule-based and ML-based logic  
- Key metrics and performance signals  
- Design rationale and future improvements  

---

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/<your-username>/math-adaptive-learning.git
cd math-adaptive-prototype

# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate     # (Windows)
# OR
source venv/bin/activate  # (Linux/Mac)

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run src/main.py
