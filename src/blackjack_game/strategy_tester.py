# strategy_tester.py

import numpy as np
import matplotlib.pyplot as plt

# import your existing bots
from bj_bots import simulate_strategy, basic_strategy, simulate_martingale_strategy
from bj_cardcounting import simulate_card_counting_strategy

def build_trajectory(sim_fn, strategy_fn, runs=1, max_hands=100, **kwargs):
    """
    For each run:
      for h in 1..max_hands: call sim_fn(strategy_fn, num_hands=h, **kwargs)
    Returns an array shape (runs, max_hands) of ending credits.
    """
    traj = np.zeros((runs, max_hands))
    for i in range(runs):
        for h in range(1, max_hands+1):
            # each call returns final credits after h hands
            traj[i, h-1] = sim_fn(strategy_fn, num_hands=h, **kwargs)
    return traj

def main():
    runs, hands = 100, 100
    init_credits = 100.0
    base_bet = 1.0

    # build arrays of shape (runs, hands)
    fixed_arr = build_trajectory(simulate_strategy, basic_strategy,
                                 runs=runs, max_hands=hands,
                                 initial_credits=init_credits, bet=base_bet)

    mart_arr  = build_trajectory(simulate_martingale_strategy, basic_strategy,
                                 runs=runs, max_hands=hands,
                                 initial_credits=init_credits, initial_bet=base_bet)

    cc_arr    = build_trajectory(simulate_card_counting_strategy, basic_strategy,
                                 runs=runs, max_hands=hands,
                                 initial_credits=init_credits, base_bet=base_bet, num_decks=6)

    # average across runs
    avg_fixed = fixed_arr.mean(axis=0)
    avg_mart  = mart_arr.mean(axis=0)
    avg_cc    = cc_arr.mean(axis=0)

    # plot
    plt.figure(figsize=(8,5))
    plt.plot(range(1, hands+1), avg_fixed, label='Basic Strategy')
    plt.plot(range(1, hands+1), avg_mart,  label='Martingale')
    plt.plot(range(1, hands+1), avg_cc,    label='Card Counting')
    plt.xlabel('Hand Number')
    plt.ylabel('Average Credits')
    plt.title(f'Average Credit Trajectory over {hands} Hands ({runs} Runs)')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
