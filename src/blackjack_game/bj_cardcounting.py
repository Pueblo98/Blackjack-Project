from bj import BlackjackGame


def compute_payout(is_blackjack: bool, reward: int, bet: float) -> float:
    """
    Calculate the payout given outcome.
    """
    if reward == 1:
        return 1.5 * bet if is_blackjack else 1.0 * bet
    elif reward == -1:
        return -1.0 * bet
    return 0.0


def hi_lo_value(card: int) -> int:
    """Hi-Lo count: 2-6=+1; 7-9=0; 10/Ace=-1"""
    if 2 <= card <= 6:
        return 1
    if 7 <= card <= 9:
        return 0
    return -1


def basic_strategy(state: dict) -> str:
    """Standard basic strategy (hard/soft)."""
    cards = state['player_hand']
    dealer = state['dealer_upcard']
    total = sum(cards)
    aces = cards.count(1)
    soft_total = total + 10 if aces and total + 10 <= 21 else total
    is_soft = (soft_total != total)
    val = soft_total if is_soft else total

    # Soft hands
    if is_soft:
        if val <= 17:
            return 'hit'
        if val == 18:
            return 'stand' if dealer in range(2, 9) else 'hit'
        return 'stand'
    # Hard hands
    if val <= 11:
        return 'hit'
    if val >= 17:
        return 'stand'
    if 12 <= val <= 16:
        return 'stand' if dealer in range(2, 7) else 'hit'
    return 'stand'


def index_play_strategy(state: dict, true_count: float) -> str:
    """
    Deviations from basic strategy based on Hi-Lo true count indices:
    - Hard 16 vs 10: stand if TC >= 0, else hit
    - Hard 15 vs 10: stand if TC >= 4, else hit
    - Hard 12 vs 3: hit if TC < 2, else stand
    Otherwise, fallback to basic_strategy
    """
    cards = state['player_hand']
    dealer = state['dealer_upcard']
    total = sum(cards)
    aces = cards.count(1)
    soft_total = total + 10 if aces and total + 10 <= 21 else total
    is_soft = (soft_total != total)
    val = soft_total if is_soft else total

    # Only apply to hard hands
    if not is_soft:
        # 16 vs 10
        if val == 16 and dealer == 10:
            return 'stand' if true_count >= 0 else 'hit'
        # 15 vs 10
        if val == 15 and dealer == 10:
            return 'stand' if true_count >= 4 else 'hit'
        # 12 vs 3
        if val == 12 and dealer == 3:
            return 'stand' if true_count >= 2 else 'hit'
    # Fallback
    return basic_strategy(state)


def simulate_card_counting_strategy(
    strategy_fn,
    num_hands: int = 100,
    initial_credits: float = 100.0,
    base_bet: float = 1.0,
    num_decks: int = 6
) -> float:
    """
    Hi-Lo card counting with index plays and bet ramp:
    - Tracks running and true count
    - Bets = base_bet * max(1, int(true_count))
    - Uses strategy_fn(state, true_count) for play decisions
    """
    game = BlackjackGame(num_decks=num_decks)
    credits = initial_credits
    running_count = 0

    for _ in range(num_hands):
        # Compute true count
        decks_remaining = max(1, len(game.deck) / 52)
        true_count = running_count / decks_remaining
        # Determine bet size
        bet = base_bet * max(1, int(true_count))
        bet = min(bet, credits)

        # Deal initial
        state = game.reset()
        player_cards = state['player_hand']
        dealer_up = state['dealer_upcard']
        # Count initial cards
        for c in player_cards + [dealer_up]:
            running_count += hi_lo_value(c)

        done, reward = False, 0
        # Player decisions
        while not done:
            action = strategy_fn(state, true_count)
            state, reward, done = game.step(action)
            if action == 'hit' and not done:
                running_count += hi_lo_value(state['player_hand'][-1])

        # Count dealer hole cards
        for c in state.get('dealer_hand', [])[1:]:
            running_count += hi_lo_value(c)

        # Payout
        is_bj = game._hand_value(player_cards) == 21
        credits += compute_payout(is_bj, reward, bet)

        # Reshuffle if shoe low
        if len(game.deck) < 52:
            game._build_deck()
            running_count = 0
        if credits <= 0:
            break

    return credits

if __name__ == '__main__':
    final = simulate_card_counting_strategy(index_play_strategy)
    print(f"Final credits after 100 hands (Hi-Lo + indices): {final}")
