import pytest
from blackjack_game.bj import BlackjackGame

def test_hand_value_no_ace():
    game = BlackjackGame(num_decks=1)
    assert game._hand_value([5, 9]) == 14

def test_hand_value_with_ace():
    game = BlackjackGame(num_decks=1)
    assert game._hand_value([1, 5]) == 16
    assert game._hand_value([1, 10]) == 21
    assert game._hand_value([1, 10, 1]) == 12

def test_reset_returns_initial_state():
    game = BlackjackGame(num_decks=1)
    state = game.reset()
    assert isinstance(state['player_hand'], list)
    assert len(state['player_hand']) == 2
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

def test_hand_value_no_ace():
    game = BlackjackGame(num_decks=1)
    assert game._hand_value([5, 9]) == 14

def test_hand_value_with_ace():
    game = BlackjackGame(num_decks=1)
    assert game._hand_value([1, 5]) == 16
    assert game._hand_value([1, 10]) == 21
    assert game._hand_value([1, 10, 1]) == 12

def test_hand_value_all_aces():
    game = BlackjackGame(num_decks=1)
    # Three aces: 1+1+1 = 3, but one ace counts as 11 → 13
    assert game._hand_value([1, 1, 1]) == 13

def test_reset_returns_initial_state():
    game = BlackjackGame(num_decks=1)
    state = game.reset()
    assert isinstance(state['player_hand'], list)
    assert len(state['player_hand']) == 2
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

def test_invalid_action_case_sensitive():
    game = BlackjackGame(num_decks=1)
    game.reset()
    # Only lowercase 'hit'/'stand' accepted
    with pytest.raises(ValueError):
        game.step('HIT')

def test_bust_on_hit():
    game = BlackjackGame(num_decks=1)
    game.player = [10, 8]
    game.dealer = [5, 5]
    game.done = False
    # Force next draw to bust
    game.deck.append(5)
    state, reward, done = game.step('hit')
    assert reward == -1
    assert done is True
    assert state['player_hand'][-1] == 5

def test_dealer_busts_player_wins():
    game = BlackjackGame(num_decks=1)
    game.player = [10, 7]
    game.dealer = [10, 6]
    game.done = False
    # Force dealer to draw a card and bust
    game.deck.append(10)
    state, reward, done = game.step('stand')
    assert reward == 1
    assert done is True

def test_dealer_hits_below_17_and_stands_on_soft17():
    game = BlackjackGame(num_decks=1)
    game.player = [10, 5]
    game.dealer = [1, 6]
    game.done = False
    state, reward, done = game.step('stand')
    assert state['dealer_hand'] == [1, 6]
    assert done is True