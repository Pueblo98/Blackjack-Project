from bj import BlackjackGame


def compute_payout(is_blackjack: bool, reward: int, bet: float) -> float:
    """
    Calculate the payout given the outcome.
    - reward: +1 win, 0 tie, -1 loss
    - is_blackjack: True if initial hand is a natural blackjack
    - bet: amount risked
    Returns net profit (can be negative).
    """
    if reward == 1:
        return 1.5 * bet if is_blackjack else 1.0 * bet
    elif reward == -1:
        return -1.0 * bet
    else:
        return 0.0


def simulate_strategy(strategy_fn, num_hands: int = 100, initial_credits: float = 100.0, bet: float = 1.0) -> float:
    """
    Simulate `num_hands` rounds of blackjack with a given strategy function.
    strategy_fn(state) -> 'hit' or 'stand'
    """
    game = BlackjackGame()
    credits = initial_credits

    for _ in range(num_hands):
        state = game.reset()
        player_hand = state['player_hand']
        # Check for natural blackjack
        is_blackjack = game._hand_value(player_hand) == 21
        done = False

        # Bot plays until round ends
        while not done:
            action = strategy_fn(state)
            state, reward, done = game.step(action)

        # Calculate payout and update credits
        payout = compute_payout(is_blackjack, reward, bet)
        credits += payout

    return credits

def simulate_martingale_strategy(strategy_fn, num_hands: int = 100, initial_credits: float = 100.0, initial_bet: float = 1.0) -> float:
    """
    Simulate `num_hands` rounds of blackjack using the Martingale betting system:
    - Double bet after each loss
    - Reset bet to `initial_bet` after each win
    - Keep bet same after a tie
    - Bet is capped by remaining credits
    Uses `strategy_fn` (e.g., basic strategy) for decisions.
    """
    game = BlackjackGame()
    credits = initial_credits
    bet = initial_bet

    for _ in range(num_hands):
        if credits <= 0:
            break
        # Place current bet, but not more than remaining credits
        current_bet = min(bet, credits)

        state = game.reset()
        player_hand = state['player_hand']
        is_blackjack = game._hand_value(player_hand) == 21
        done = False

        while not done:
            action = strategy_fn(state)
            state, reward, done = game.step(action)

        payout = compute_payout(is_blackjack, reward, current_bet)
        credits += payout

        # Adjust bet for next round
        if payout < 0:
            bet = current_bet * 2
        elif payout > 0:
            bet = initial_bet
        # If tie (payout == 0), bet remains the same

    return credits

def hi_lo_value(card: int) -> int:
    """
    Hi-Lo count value:
      2-6 => +1
      7-9 => 0
      10/Ace => -1
    """
    if 2 <= card <= 6:
        return 1
    if 7 <= card <= 9:
        return 0
    return -1

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

# Strategy implementations

def always_stand_strategy(state):
    """Always stand regardless of hand."""
    return 'stand'


def hit_until_19_strategy(state):
    """
    Hit until the hand value is at least 19, then stand.
    state['player_hand'] is a list of ints representing card values (1 for Ace).
    """
    # Compute current hand value using BlackjackGame logic
    game = BlackjackGame()  # Temporary instance to access _hand_value
    # Monkey-patch player hand into game for value calculation
    current_value = game._hand_value(state['player_hand'])
    return 'hit' if current_value < 19 else 'stand'

def basic_strategy(state):
    """
    Basic blackjack strategy (hard/soft totals, hit or stand only).
    - Hard totals: Stand on 17+, hit on 11 or less.
        On 12-16: stand if dealer shows 2-6, else hit.
    - Soft totals: (Ace counted as 11)
        Hit on soft 17 or less.
        Soft 18: stand vs dealer 2-8, else hit.
        Stand on soft 19+.
    """
    # Determine player total and softness
    cards = state['player_hand']
    dealer_up = state['dealer_upcard']
    game = BlackjackGame()
    # Raw sum and count aces
    total = sum(cards)
    ace_count = cards.count(1)
    # Check for a soft total
    soft_total = total + 10 if ace_count > 0 and total + 10 <= 21 else total
    is_soft = (soft_total != total)
    hand_value = soft_total if is_soft else total

    # Soft hand logic
    if is_soft:
        if hand_value <= 17:
            return 'hit'
        if hand_value == 18:
            # Stand vs 2-8, else hit
            return 'stand' if dealer_up in range(2, 9) else 'hit'
        return 'stand'

    # Hard hand logic
    if hand_value <= 11:
        return 'hit'
    if hand_value >= 17:
        return 'stand'
    # 12-16
    if 12 <= hand_value <= 16:
        return 'stand' if dealer_up in range(2, 7) else 'hit'

    # Default
    return 'stand'

def basic_strategy_ignoring_count(state, true_count):
    # Completely ignore true_count, fall back to basic_strategy
    return basic_strategy(state)


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




if __name__ == "__main__":
    print("Always Stand Strategy:")
    final_credits_stand = simulate_strategy(always_stand_strategy)
    print(f"  Final credits after 100 hands: {final_credits_stand}\n")

    print("Hit Until 19 Strategy:")
    final_credits_hit19 = simulate_strategy(hit_until_19_strategy)
    print(f"  Final credits after 100 hands: {final_credits_hit19}\n")

    print("Basic Strategy:")
    final_credits_basic = simulate_strategy(basic_strategy)
    print(f"  Final credits after 100 hands: {final_credits_basic}\n")
    
    print("Martingale with Basic Strategy:")
    final_martingale = simulate_martingale_strategy(basic_strategy)
    print(f"  Final credits after 100 hands: {final_martingale}\n")

    print("Card counting with Basic Strategy:")
    final = simulate_card_counting_strategy(basic_strategy_ignoring_count)
    print(f"Final credits after 100 hands: {final}\n")
    
    print("Card counting with index play Strategy:")
    final = simulate_card_counting_strategy(index_play_strategy)
    print(f"Final credits after 100 hands : {final}\n")

