import random

class BlackjackGame:
    """Simple Blackjack environment for bots:
       - 4 decks
       - Aces = 1 or 11
       - Dealer hits to 17
       - step('hit') or step('stand') → (state, reward, done)
    """
    def __init__(self, num_decks: int = 4):
        self.num_decks = num_decks
        self._build_deck()

    def _build_deck(self):
        # One deck has: A=1×4, 2–9 each 4×, 10/J/Q/K = 16× total
        base = [1]*4 + [2]*4 + [3]*4 + [4]*4 + [5]*4 + \
               [6]*4 + [7]*4 + [8]*4 + [9]*4 + [10]*16
        self.deck = base * self.num_decks
        random.shuffle(self.deck)

    def _draw(self) -> int:
        if len(self.deck) < 15:  # reshuffle if low
            self._build_deck()
        return self.deck.pop()

    def _hand_value(self, hand: list[int]) -> int:
        total = sum(hand)
        # if there's at least one ace (1) and treating one ace as 11 doesn't bust:
        if 1 in hand and total + 10 <= 21:
            return total + 10
        return total

    def reset(self) -> dict:
        """Start a new round. Returns initial state."""
        self.player = [self._draw(), self._draw()]
        self.dealer = [self._draw(), self._draw()]
        self.done = False
        return {
            'player_hand': self.player.copy(),
            'dealer_upcard': self.dealer[0]
        }

    def step(self, action: str) -> tuple[dict, int, bool]:
        """
        action: 'hit' or 'stand'
        Returns: (state, reward, done)
          reward: +1 win, 0 tie, -1 loss
        """
        if self.done:
            raise RuntimeError("Round over — call reset() to start again.")

        # Player hits
        if action == 'hit':
            self.player.append(self._draw())
            if self._hand_value(self.player) > 21:
                self.done = True
                return (
                    {'player_hand': self.player.copy(),
                     'dealer_upcard': self.dealer[0]},
                    -1,  # player bust
                    True
                )
            else:
                return (
                    {'player_hand': self.player.copy(),
                     'dealer_upcard': self.dealer[0]},
                    0,
                    False
                )

        # Player stands → dealer’s turn
        elif action == 'stand':
            while self._hand_value(self.dealer) < 17:
                self.dealer.append(self._draw())

            player_val = self._hand_value(self.player)
            dealer_val = self._hand_value(self.dealer)

            if dealer_val > 21:
                reward = +1
            elif dealer_val > player_val:
                reward = -1
            elif dealer_val < player_val:
                reward = +1
            else:
                reward = 0

            self.done = True
            return (
                {
                    'player_hand': self.player.copy(),
                    'dealer_upcard': self.dealer[0],
                    'dealer_hand': self.dealer.copy()
                },
                reward,
                True
            )

        else:
            raise ValueError("Action must be 'hit' or 'stand'.")
