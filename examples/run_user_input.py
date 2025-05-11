"""
Blackjack Simulator

This script allows you to run simulations of different blackjack strategies and
betting systems with customizable parameters.

Usage:
    python run_user_input.py --bet-strategy fixed --play-strategy basic --hands 1000 --credits 500

For help:
    python run_user_input.py --help
"""

## Example uses
# Run basic strategy with fixed betting
#  - python run_user_input.py --bet-strategy fixed --play-strategy basic --hands 1000 --credits 500

# Try martingale betting with basic strategy
#  - python run_user_input.py --bet-strategy martingale --play-strategy basic --hands 500 --credits 1000 --bet 2

# Use card counting with index plays
# - python run_user_input.py --bet-strategy card_counting --play-strategy index_play --hands 2000 --credits 1000

# List all available strategies
# - python run_user_input.py --list-strategies

import argparse
import time
from typing import Callable, Dict, Any

# Import from the blackjack_game package
from blackjack_game import (
    # Core simulation functions
    simulate_strategy,
    simulate_martingale_strategy,
    simulate_card_counting_strategy,
    
    # Play strategies
    basic_strategy,
    always_stand_strategy,
    hit_until_19_strategy,
    basic_strategy_ignoring_count,
    index_play_strategy,
    
    # Game
    BlackjackGame
)

# Define betting strategy descriptions
BETTING_STRATEGIES = {
    "fixed": {
        "name": "Fixed Bet",
        "description": "Always bet the same amount regardless of wins or losses.",
        "function": simulate_strategy
    },
    "martingale": {
        "name": "Martingale System",
        "description": "Double your bet after each loss, return to base bet after a win.",
        "function": simulate_martingale_strategy
    },
    "card_counting": {
        "name": "Card Counting",
        "description": "Adjust bet size based on the Hi-Lo count (higher count = higher bet).",
        "function": simulate_card_counting_strategy
    }
}

# Define play strategy descriptions
PLAY_STRATEGIES = {
    "basic": {
        "name": "Basic Strategy",
        "description": "Standard blackjack strategy based on player hand vs dealer upcard.",
        "function": basic_strategy,
        "count_function": basic_strategy_ignoring_count
    },
    "always_stand": {
        "name": "Always Stand",
        "description": "Never hit, always stand with initial hand (generally poor strategy).",
        "function": always_stand_strategy
    },
    "hit_until_19": {
        "name": "Hit Until 19",
        "description": "Keep hitting until hand value is 19 or higher.",
        "function": hit_until_19_strategy
    },
    "index_play": {
        "name": "Index Plays",
        "description": "Basic strategy with adjustments based on the true count.",
        "function": index_play_strategy
    }
}

def print_strategy_info():
    """Print information about available strategies."""
    print("\n=== BETTING STRATEGIES ===")
    for key, strategy in BETTING_STRATEGIES.items():
        print(f"\n{strategy['name']} (--bet-strategy {key})")
        print(f"  {strategy['description']}")
    
    print("\n=== PLAY STRATEGIES ===")
    for key, strategy in PLAY_STRATEGIES.items():
        print(f"\n{strategy['name']} (--play-strategy {key})")
        print(f"  {strategy['description']}")
    print("\n")

def run_simulation(args):
    """Run the blackjack simulation with the specified parameters."""
    # Get the betting strategy
    bet_strategy = BETTING_STRATEGIES[args.bet_strategy]["function"]
    bet_strategy_name = BETTING_STRATEGIES[args.bet_strategy]["name"]
    
    # Get the play strategy
    play_strategy = PLAY_STRATEGIES[args.play_strategy]
    play_strategy_name = play_strategy["name"]
    
    # Determine which play strategy function to use
    if args.bet_strategy == "card_counting":
        if args.play_strategy == "index_play" or "count_function" in play_strategy:
            play_function = play_strategy.get("count_function", play_strategy["function"])
        else:
            print(f"Warning: {play_strategy_name} doesn't support card counting. Using basic strategy with count.")
            play_function = basic_strategy_ignoring_count
    else:
        play_function = play_strategy["function"]
    
    print(f"Running simulation with:")
    print(f"  Betting Strategy: {bet_strategy_name}")
    print(f"  Play Strategy: {play_strategy_name}")
    print(f"  Hands: {args.hands}")
    print(f"  Starting Credits: {args.credits}")
    if args.bet_strategy == "fixed":
        print(f"  Bet Size: {args.bet}")
    elif args.bet_strategy == "martingale":
        print(f"  Initial Bet: {args.bet}")
    elif args.bet_strategy == "card_counting":
        print(f"  Base Bet: {args.bet}")
        print(f"  Number of Decks: {args.decks}")
    
    print("\nSimulating...", end="", flush=True)
    start_time = time.time()
    
    # Run the simulation with appropriate parameters
    if args.bet_strategy == "fixed":
        final_credits = bet_strategy(
            play_function,
            num_hands=args.hands,
            initial_credits=args.credits,
            bet=args.bet
        )
    elif args.bet_strategy == "martingale":
        final_credits = bet_strategy(
            play_function,
            num_hands=args.hands,
            initial_credits=args.credits,
            initial_bet=args.bet
        )
    elif args.bet_strategy == "card_counting":
        final_credits = bet_strategy(
            play_function,
            num_hands=args.hands,
            initial_credits=args.credits,
            base_bet=args.bet,
            num_decks=args.decks
        )
    
    elapsed_time = time.time() - start_time
    print(f" done in {elapsed_time:.2f} seconds.")
    
    # Calculate results
    profit = final_credits - args.credits
    roi = (profit / args.credits) * 100
    
    print("\nRESULTS:")
    print(f"  Starting Credits: {args.credits}")
    print(f"  Final Credits: {final_credits:.2f}")
    print(f"  Profit/Loss: {profit:.2f}")
    print(f"  ROI: {roi:.2f}%")
    print(f"  Average Profit Per Hand: {profit/args.hands:.4f}")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Blackjack Strategy Simulator")
    
    # Create a mutually exclusive group for the list-strategies option
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-strategies", action="store_true",
                        help="List available strategies and exit")
    group.add_argument("--bet-strategy", type=str, 
                        choices=BETTING_STRATEGIES.keys(),
                        help="Betting strategy to use")
    
    # Play strategy is only required if bet-strategy is specified
    parser.add_argument("--play-strategy", type=str,
                        choices=PLAY_STRATEGIES.keys(),
                        help="Play strategy to use")
    
    # Optional arguments
    parser.add_argument("--hands", type=int, default=1000,
                        help="Number of hands to simulate (default: 1000)")
    
    parser.add_argument("--credits", type=float, default=1000.0,
                        help="Starting credits (default: 1000.0)")
    
    parser.add_argument("--bet", type=float, default=1.0,
                        help="Base bet size (default: 1.0)")
    
    parser.add_argument("--decks", type=int, default=6,
                        help="Number of decks for card counting (default: 6)")
    
    args = parser.parse_args()
    
    if args.bet_strategy and not args.play_strategy:
        parser.error("--play-strategy is required when using --bet-strategy")
        
    return args

def main():
    """Main entry point for the script."""
    args = parse_arguments()
    
    if args.list_strategies:
        print_strategy_info()
        return
    
    if args.bet_strategy == "card_counting" and args.play_strategy not in ["basic", "index_play"]:
        print(f"Warning: {PLAY_STRATEGIES[args.play_strategy]['name']} may not work optimally with card counting.")
        print("For best results with card counting, use 'basic' or 'index_play' strategies.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Simulation cancelled.")
            return
    
    run_simulation(args)

if __name__ == "__main__":
    main()