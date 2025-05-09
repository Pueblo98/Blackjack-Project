import pytest
from blackjack_game.bj import BlackjackGame

def test_hand_value_no_ace():
    game = BlackjackGame(num_decks=1)
    assert game._hand_value([5, 9]) == 14

def test_hand_value_with_ace():
    game = BlackjackGame(num_decks=1)
    # soft 16 (1+5 +10 bonus)
    assert game._hand_value([1, 5]) == 16
    # natural 21
    assert game._hand_value([1, 10]) == 21
    # two aces + 10 => sum=12 (no bonus because 12+10=22)
    assert game._hand_value([1, 10, 1]) == 12

def test_reset_returns_initial_state():
    game = BlackjackGame(num_decks=1)
    state = game.reset()
    # two cards to player
    assert isinstance(state['player_hand'], list)
    assert len(state['player_hand']) == 2
    # one up-card for dealer
    assert isinstance(state['dealer_upcard'], int)

def test_step_after_done_raises():
    game = BlackjackGame(num_decks=1)
    game.done = True
    with pytest.raises(RuntimeError):
        game.step('hit')

def test_invalid_action_raises_value_error():
    game = BlackjackGame(num_decks=1)
    game.reset()
    with pytest.raises(ValueError):
        game.step('invalid_action')
