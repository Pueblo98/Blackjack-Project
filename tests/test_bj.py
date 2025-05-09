import pytest
from blackjack_game.bj import BlackjackGame

def test_ace_value():
    game = BlackjackGame(num_decks=1)
    assert game._hand_value([1, 9]) == 20
    assert game._hand_value([1, 1, 8]) == 20

def test_bust():
    game = BlackjackGame(num_decks=1)
    assert game._hand_value([10, 5, 7]) == 22