import pandas as pd
from sklearn.linear_model import LogisticRegression
from typing import Dict, Any
import os


class AdaptiveEngine:
   
    def __init__(self, mode: str = "rule"):
        self.mode = mode  # 'rule' or 'ml'
        self.user_levels: Dict[str, str] = {}
        self.model = None

        if self.mode == "ml":
            self._train_model()

    def get_current_level(self, user: str) -> str:
        return self.user_levels.get(user, "easy")

    def update_level(self, user: str, performance: Dict[str, Any]) -> str:
        current_level = self.get_current_level(user)

        if self.mode == "ml" and self.model:
            next_level = self._ml_predict(performance)
        else:
            next_level = self._rule_based_next_level(current_level, performance)

        self.user_levels[user] = next_level
        return next_level

    # ---------------- RULE-BASED LOGIC ----------------
    def _rule_based_next_level(self, current_level: str, performance: Dict[str, Any]) -> str:
        accuracy = performance.get("accuracy", 0)
        avg_time = performance.get("avg_time", 999)

        if accuracy >= 80 and avg_time <= 5:
            return self._increase_difficulty(current_level)
        elif accuracy <= 50:
            return self._decrease_difficulty(current_level)
        else:
            return current_level

    def _increase_difficulty(self, level: str) -> str:
        order = ["easy", "medium", "hard"]
        i = min(order.index(level) + 1, len(order) - 1)
        return order[i]

    def _decrease_difficulty(self, level: str) -> str:
        order = ["easy", "medium", "hard"]
        i = max(order.index(level) - 1, 0)
        return order[i]

    # ---------------- ML LOGIC ----------------
    def _train_model(self):
        data_path = "data/sessions.csv"
        if not os.path.exists(data_path):
            print("No session data found. ML model not trained.")
            return

        df = pd.read_csv(data_path)
        if len(df) < 10:  # not enough data
            print(" Not enough data for ML training. Using rule-based logic.")
            return

        # Prepare features and labels
        df["difficulty_code"] = df["difficulty"].map({"easy": 0, "medium": 1, "hard": 2})
        X = df[["response_time", "correct"]].groupby(df.index).mean()  # features
        y = df["difficulty_code"]

        model = LogisticRegression(max_iter=500)
        model.fit(X, y)
        self.model = model
        print("ML model trained successfully!")

    def _ml_predict(self, performance: Dict[str, Any]) -> str:
        if not self.model:
            return "easy"

        X_new = [[performance.get("avg_time", 5), 1 if performance.get("accuracy", 0) > 70 else 0]]
        pred = self.model.predict(X_new)[0]
        level_map = {0: "easy", 1: "medium", 2: "hard"}
        return level_map.get(pred, "easy")
