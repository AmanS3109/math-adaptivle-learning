import time
import pandas as pd
from typing import List, Dict, Any


class PerformanceTracker:
   
    def __init__(self):
        self.records: List[Dict[str, Any]] = []
        self.start_time = None

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self) -> float:
        if self.start_time is None:
            return 0.0
        return round(time.time() - self.start_time, 2)

    def log_attempt(self, user: str, difficulty: str, question: str,
                    user_answer: float, correct_answer: float, correct: bool,
                    response_time: float):
        self.records.append({
            "user": user,
            "difficulty": difficulty,
            "question": question,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "correct": correct,
            "response_time": response_time
        })

    def summary(self) -> Dict[str, Any]:
        if not self.records:
            return {"accuracy": 0, "avg_time": 0, "total": 0}

        total = len(self.records)
        correct_count = sum(1 for r in self.records if r["correct"])
        avg_time = round(sum(r["response_time"] for r in self.records) / total, 2)
        accuracy = round((correct_count / total) * 100, 2)

        return {"accuracy": accuracy, "avg_time": avg_time, "total": total}

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.records)

    def save_to_csv(self, path: str):
        df = self.to_dataframe()
        try:
            existing = pd.read_csv(path)
            df = pd.concat([existing, df], ignore_index=True)
        except FileNotFoundError:
            pass 
        df.to_csv(path, index=False)
