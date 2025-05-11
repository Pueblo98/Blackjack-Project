from blackjack_game import (
    simulate_strategy,
    simulate_martingale_strategy,
    simulate_card_counting_strategy,
    basic_strategy,
    always_stand_strategy,
    hit_until_19_strategy,
    basic_strategy_ignoring_count,
    index_play_strategy,
)


if __name__ == "__main__":
    result = simulate_strategy(basic_strategy, num_hands=100, initial_credits=100, bet=1)
    print(f"Basic Strategy result after 100 hands: {result}")

    print("Always Stand Strategy:")
    final_credits_stand = simulate_strategy(always_stand_strategy)
    print(f"  Final credits after 100 hands: {final_credits_stand}\n")

    print("Hit Until 19 Strategy:")
    final_credits_hit19 = simulate_strategy(hit_until_19_strategy)
    print(f"  Final credits after 100 hands: {final_credits_hit19}\n")

    print("Basic Strategy:")
    final_credits_basic = simulate_strategy(basic_strategy)
    print(f"  Final credits after 100 hands: {final_credits_basic}\n")
    
    print("Martingale with Basic Strategy:")
    final_martingale = simulate_martingale_strategy(basic_strategy)
    print(f"  Final credits after 100 hands: {final_martingale}\n")

    print("Card counting with Basic Strategy:")
    final = simulate_card_counting_strategy(basic_strategy_ignoring_count)
    print(f"Final credits after 100 hands: {final}\n")
    
    print("Card counting with index play Strategy:")
    final = simulate_card_counting_strategy(index_play_strategy)
    print(f"Final credits after 100 hands : {final}\n")

