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

def test_build_trajectory_zero_runs():
    arr = build_trajectory(lambda *args, **kw: 0, lambda s: 'stand', runs=0, max_hands=5)
    assert arr.shape == (0, 5)

def test_build_trajectory_zero_hands():
    arr = build_trajectory(lambda *args, **kw: 0, lambda s: 'stand', runs=5, max_hands=0)
    assert arr.shape == (5, 0)

def test_build_trajectory_kwargs_passed():
    def sim_fn(strat_fn, num_hands, **kwargs):
        # Echo a custom kwarg
        return kwargs.get('foo', -1)
    arr = build_trajectory(sim_fn, lambda s: None, runs=2, max_hands=3, foo=42)
    assert (arr == 42).all()

def test_build_trajectory_diff_strat_fn():
    def sim_fn(strat_fn, num_hands, **kwargs):
        return 1 if strat_fn is dummy1 else 2
    def dummy1(state): pass
    def dummy2(state): pass

    arr1 = build_trajectory(sim_fn, dummy1, runs=1, max_hands=1)
    arr2 = build_trajectory(sim_fn, dummy2, runs=1, max_hands=1)

    assert arr1[0,0] == 1
    assert arr2[0,0] == 2