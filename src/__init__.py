# src/__init__.py
# This file exposes the blackjack_game package

from . import blackjack_game

# Allow direct import of key components from the package
from .blackjack_game import (
    BlackjackGame,
    basic_strategy,
    always_stand_strategy,
    hit_until_19_strategy,
    simulate_strategy,
    simulate_martingale_strategy,
    simulate_card_counting_strategy,
    run_strategy_test
)

__all__ = [
    "blackjack_game",
    "BlackjackGame",
    "basic_strategy",
    "always_stand_strategy",
    "hit_until_19_strategy",
    "simulate_strategy",
    "simulate_martingale_strategy", 
    "simulate_card_counting_strategy",
    "run_strategy_test"
]