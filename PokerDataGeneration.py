import itertools
import pandas as pd
import random
import subprocess

# Poker hand rankings
HAND_RANKS = [
    "High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight",
    "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"
]

# Generate all 52 cards
RANKS = '23456789TJQKA'
SUITS = 'CDHS'
DECK = [r + s for r in RANKS for s in SUITS]

def pokerstove_eval(hole_cards, board_cards):
    """Run PokerStove to get hand equity"""
    command = f'echo "{hole_cards}: xx xx" | pokerstove -board {board_cards} -eval'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    try:
        equity_line = result.stdout.splitlines()[-1]
        equity = float(equity_line.split()[2])  # Extract % win probability
        return equity
    except Exception as e:
        print("PokerStove Error:", e)
        return None

def generate_poker_data(num_samples=10000):
    data = []

    for _ in range(num_samples):
        deck = DECK.copy()
        random.shuffle(deck)

        hole_cards = deck[:2]  # Player's hole cards
        flop = deck[2:5]  # Flop (3 cards)
        turn = deck[5]  # Turn (1 card)
        river = deck[6]  # River (1 card)

        board = flop + [turn, river]
        equity = pokerstove_eval(" ".join(hole_cards), " ".join(board))

        if equity is None:
            continue  # Skip invalid results

        # Assign a rank based on equity (simplified approach)
        hand_rank = HAND_RANKS[min(int(equity / 10), 9)]

        data.append({
            "Hole Cards": ", ".join(hole_cards),
            "Flop": ", ".join(flop),
            "Turn": turn,
            "River": river,
            "Hand Rank": hand_rank
        })

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv("data/poker_data.csv", index=False)
    print(f"✅ Poker data saved: data/poker_data.csv ({len(data)} hands)")

# Run the generator
if __name__ == "__main__":
    generate_poker_data(10000)
