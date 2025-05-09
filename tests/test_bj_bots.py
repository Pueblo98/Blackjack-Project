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
    # natural blackjack payout
    assert compute_payout(True, 1, 2.0) == 3.0
    # normal win
    assert compute_payout(False, 1, 2.0) == 2.0
    # tie
    assert compute_payout(False, 0, 2.0) == 0.0
    # loss
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

def test_basic_strategy_hard_totals():
    # <=11 → hit
    assert basic_strategy({'player_hand': [5,5], 'dealer_upcard': 2}) == 'hit'
    # >=17 → stand
    assert basic_strategy({'player_hand': [10,7], 'dealer_upcard': 3}) == 'stand'
    # 12–16: stand vs 2–6, else hit
    assert basic_strategy({'player_hand': [8,5], 'dealer_upcard': 3}) == 'stand'
    assert basic_strategy({'player_hand': [8,5], 'dealer_upcard': 7}) == 'hit'

def test_basic_strategy_soft_totals():
    # soft ≤17 → hit
    assert basic_strategy({'player_hand': [1,6], 'dealer_upcard': 2}) == 'hit'
    # soft 18: stand vs 2–8, else hit
    assert basic_strategy({'player_hand': [1,7], 'dealer_upcard': 5}) == 'stand'
    assert basic_strategy({'player_hand': [1,7], 'dealer_upcard': 9}) == 'hit'

def test_basic_strategy_ignoring_count():
    state = {'player_hand': [5,5], 'dealer_upcard': 2}
    # should mirror basic_strategy
    assert basic_strategy_ignoring_count(state, 10) == basic_strategy(state)

def test_index_play_strategy_deviation():
    state = {'player_hand': [10,6], 'dealer_upcard': 10}
    # hard 16 vs 10
    assert index_play_strategy(state, 0) == 'stand'
    assert index_play_strategy(state, -1) == 'hit'
    # fallback case uses basic_strategy
    fallback = index_play_strategy({'player_hand': [10,6], 'dealer_upcard': 9}, -5)
    assert fallback == basic_strategy({'player_hand': [10,6], 'dealer_upcard': 9})
