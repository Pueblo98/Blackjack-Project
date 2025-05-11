from blackjack_game import (
    simulate_martingale_strategy,
    basic_strategy,

)
if __name__ == "__main__":
    result = simulate_martingale_strategy(basic_strategy, num_hands=100, initial_credits=100, initial_bet=1)
    print(f"Martingale Strategy result after 100 hands: {result}")
