from adaptive_engine import AdaptiveEngine

def main():
    engine = AdaptiveEngine(mode="ml")
    result = engine.update_level("Aman", {"accuracy": 90, "avg_time": 4})
    print("Predicted next level:", result)

if __name__ == "__main__":
    main()
