from pprint import pprint

from research_lab.lab import run


if __name__ == "__main__":
    result = run(seed=7, population=10, generations=5)
    print("=== AI TRADING EVOLUTION / LAB 001 ===")
    print("Mode: SIMULATION ONLY")
    print("Population:", result["population"])
    print("Generations:", result["generations"])
    print("Best genome:")
    pprint(result["best_genome"])
    print("Validation:")
    pprint(result["validation"])
    print("Unseen test:")
    pprint(result["test"])
