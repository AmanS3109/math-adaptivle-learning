import random
from typing import Tuple

class PuzzleGenerator:
   
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
        self.operations = {
            "easy": ["+", "-"],
            "medium": ["+", "-", "*"],
            "hard": ["+", "-", "*", "/"],
        }

    def generate_puzzle(self, difficulty: str) -> Tuple[str, float]:
        difficulty = difficulty.lower()

        if difficulty == "easy":
            a, b = random.randint(1, 9), random.randint(1, 9)
        else:
            a, b = random.randint(10, 99), random.randint(1, 99)

        op = random.choice(self.operations.get(difficulty, ["+"]))

        if op == "/":
            b = random.randint(1, 9) 
            a = b * random.randint(1, 12)  
            answer = a / b
        elif op == "+":
            answer = a + b
        elif op == "-":
            answer = a - b
        elif op == "*":
            answer = a * b
        else:
            raise ValueError("Unknown operation")

        question = f"{a} {op} {b} = ?"
        return question, round(answer, 2)
