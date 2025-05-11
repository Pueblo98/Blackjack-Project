import pytest
from blackjack_game.bj_bots import (
    compute_payout,
    hi_lo_value,
    always_stand_strategy,
    hit_until_19_strategy,
    basic_strategy,
    basic_strategy_ignoring_count,
    index_play_strategy,
)

def test_compute_payout():
    assert compute_payout(True, 1, 2.0) == 3.0
    assert compute_payout(False, 1, 2.0) == 2.0
    assert compute_payout(False, 0, 2.0) == 0.0
    assert compute_payout(False, -1, 2.0) == -2.0

def test_hi_lo_value():
    for card in range(2,7):
        assert hi_lo_value(card) == 1
    for card in (7,8,9):
        assert hi_lo_value(card) == 0
    for card in (1, 10, 11):
        assert hi_lo_value(card) == -1

def test_always_stand_strategy():
    state = {'player_hand': [5,6], 'dealer_upcard': 10}
    assert always_stand_strategy(state) == 'stand'

def test_hit_until_19_strategy():
    state_low = {'player_hand': [5], 'dealer_upcard': 2}
    assert hit_until_19_strategy(state_low) == 'hit'
    state_high = {'player_hand': [10,9], 'dealer_upcard': 5}
    assert hit_until_19_strategy(state_high) == 'stand'


def test_basic_strategy_ignoring_count():
    state = {'player_hand': [5,5], 'dealer_upcard': 2}
    assert basic_strategy_ignoring_count(state, 10) == basic_strategy(state)

def test_compute_payout_zero_bet():
    # Betting zero should always return zero profit/loss
    assert compute_payout(True, 1, 0.0) == 0.0
    assert compute_payout(False, -1, 0.0) == 0.0


def test_basic_strategy_hard_totals():
    assert basic_strategy({'player_hand': [5,5], 'dealer_upcard': 2}) == 'hit'
    assert basic_strategy({'player_hand': [10,7], 'dealer_upcard': 3}) == 'stand'

def test_basic_strategy_hard_boundary():
    assert basic_strategy({'player_hand': [10,2], 'dealer_upcard': 6}) == 'stand'
    assert basic_strategy({'player_hand': [10,2], 'dealer_upcard': 7}) == 'hit'

def test_basic_strategy_soft_totals():
    assert basic_strategy({'player_hand': [1,6], 'dealer_upcard': 2}) == 'hit'
    assert basic_strategy({'player_hand': [1,7], 'dealer_upcard': 5}) == 'stand'
    assert basic_strategy({'player_hand': [1,7], 'dealer_upcard': 9}) == 'hit'

def test_basic_strategy_soft_boundaries():
    assert basic_strategy({'player_hand': [1,7], 'dealer_upcard': 8}) == 'stand'
    assert basic_strategy({'player_hand': [1,7], 'dealer_upcard': 9}) == 'hit'
    assert basic_strategy({'player_hand': [1,8], 'dealer_upcard': 2}) == 'stand'


def test_index_play_strategy_deviation():
    state = {'player_hand': [10,6], 'dealer_upcard': 10}
    assert index_play_strategy(state, 0) == 'stand'
    assert index_play_strategy(state, -1) == 'hit'
    assert index_play_strategy({'player_hand': [15], 'dealer_upcard': 10}, 4) == 'stand'
    assert index_play_strategy({'player_hand': [12], 'dealer_upcard': 3}, 2) == 'stand'
    soft_state = {'player_hand': [1,7], 'dealer_upcard': 2}
    for tc in [-5, 0, 5]:
        assert index_play_strategy(soft_state, tc) == basic_strategy(soft_state)