import pytest
from bj_bots import compute_payout, hi_lo_value

def test_compute_payout_win():
    assert compute_payout(is_blackjack=False, reward=1, bet=10) == 10
def test_compute_payout_blackjack():
    assert compute_payout(is_blackjack=True, reward=1, bet=10) == 15
def test_compute_payout_loss():
    assert compute_payout(is_blackjack=False, reward=-1, bet=10) == -10
def test_compute_payout_tie():
    assert compute_payout(is_blackjack=False, reward=0, bet=10) == 0

def test_hi_lo_value():
    assert hi_lo_value(2) == 1
    assert hi_lo_value(7) == 0
    assert hi_lo_value(10) == -1
    assert hi_lo_value(1) == -1  # Ace
