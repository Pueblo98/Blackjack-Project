import numpy as np
import matplotlib.pyplot as plt
from blackjack_game.strategy_tester import build_trajectory
from blackjack_game.bj_bots import (
    # Core functionality
    simulate_strategy,
    simulate_martingale_strategy,
    simulate_card_counting_strategy,
    
    # Strategy implementations
    basic_strategy,
    always_stand_strategy, 
    hit_until_19_strategy,
    basic_strategy_ignoring_count,
    index_play_strategy,
)


def main():
    runs, hands = 100, 100
    init_credits = 100.0
    base_bet     = 1.0

    # Basic fixed‐bet strategy
    basic_arr = build_trajectory(
        simulate_strategy,
        basic_strategy,
        runs=runs,
        max_hands=hands,
        initial_credits=init_credits,
        bet=base_bet
    )
    #always stand
    basic_stand = build_trajectory(
        simulate_strategy,
        always_stand_strategy,
        runs=runs,
        max_hands=hands,
        initial_credits=init_credits,
        bet=base_bet
    )
    #hit until 19
    basic_hit = build_trajectory(
        simulate_strategy,
        hit_until_19_strategy,
        runs=runs,
        max_hands=hands,
        initial_credits=init_credits,
        bet=base_bet
    )
    
    # Martingale on basic strategy
    mart_arr = build_trajectory(
        simulate_martingale_strategy,
        basic_strategy,
        runs=runs,
        max_hands=hands,
        initial_credits=init_credits,
        initial_bet=base_bet
    )

    # Hi-Lo card counting with index deviations
    cc_arr = build_trajectory(
        simulate_card_counting_strategy,
        index_play_strategy,
        runs=runs,
        max_hands=hands,
        initial_credits=init_credits,
        base_bet=base_bet,
        num_decks=4
    
    )
    
    basic_strategy_with_count = build_trajectory(
        simulate_card_counting_strategy,
        basic_strategy_ignoring_count,
        runs=runs,
        max_hands=hands,
        initial_credits=init_credits,
        base_bet=base_bet,
        num_decks=4        
    )

    avg_basic = basic_arr.mean(axis=0)
    avg_mart  = mart_arr.mean(axis=0)
    avg_cc    = cc_arr.mean(axis=0)
    avg_stand = basic_stand.mean(axis=0)
    avg_hit   = basic_hit.mean(axis=0)
    avg_count_basic = basic_strategy_with_count.mean(axis=0)

    plt.figure(figsize=(8,5))
    plt.plot(range(1, hands+1), avg_basic, label='Basic Strategy')
    plt.plot(range(1, hands+1), avg_mart,  label='Martingale')
    plt.plot(range(1, hands+1), avg_cc,    label='Card Counting')
    plt.plot(range(1, hands+1), avg_stand, label='always stand')
    plt.plot(range(1, hands+1), avg_hit,   label='hit until 19')
    plt.plot(range(1, hands+1), avg_count_basic,   label=' Counting strategy with basic play')
    plt.xlabel('Hand Number')
    plt.ylabel('Average Credits')
    plt.title(f'Average Credit Trajectory over {hands} Hands ({runs} Runs)')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()