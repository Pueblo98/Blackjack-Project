import numpy as np
from blackjack_game.strategy_tester import build_trajectory

def test_build_trajectory_shape_and_values():
    def sim_fn(strat_fn, num_hands, **kwargs):
        return num_hands * 2

    def dummy_strat(state, *args, **kwargs):
        return None

    runs, max_hands = 3, 5
    arr = build_trajectory(sim_fn, dummy_strat, runs=runs, max_hands=max_hands)

    assert isinstance(arr, np.ndarray)
    assert arr.shape == (runs, max_hands)

    # each entry should be 2 * hand_number
    for i in range(runs):
        for h in range(1, max_hands + 1):
            assert arr[i, h-1] == 2 * h
