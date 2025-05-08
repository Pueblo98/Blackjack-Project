from bj_bots import simulate_strategy, basic_strategy

if __name__ == "__main__":
    result = simulate_strategy(basic_strategy, num_hands=100, initial_credits=100, bet=1)
    print(f"Basic Strategy result after 100 hands: {result}")
