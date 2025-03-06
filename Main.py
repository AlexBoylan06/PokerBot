import random


# Card Class
class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"


# Deck Class
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num=1):
        dealt_cards = []
        for _ in range(num):
            if len(self.cards) > 0:
                dealt_cards.append(self.cards.pop(0))
            else:
                print("No more cards to deal.")
        return dealt_cards

    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"

class Player:
    def __init__(self, name, chips=1000):
        """
        Initialize a player with a name and a starting amount of chips.
        """
        self.name = name
        self.chips = chips
        self.hand = []  # Hole cards
        self.current_bet = 0  # Tracks how much the player has bet in the current round
        self.active = True  # Player is still in the hand (not folded)

    def receive_cards(self, cards):
        """Receive hole cards at the start of the round."""
        self.hand = cards

    def bet(self, amount):
        """Player places a bet, reducing their chips."""
        if amount > self.chips:
            print(f"{self.name} does not have enough chips to bet {amount}. Going all-in.")
            amount = self.chips  # All-in if they don't have enough
        self.chips -= amount
        self.current_bet += amount
        return amount

    def fold(self):
        """Player folds and is no longer active in the round."""
        self.active = False
        self.hand = []

    def check(self):
        """Player checks (if no bet is required)."""
        print(f"{self.name} checks.")

    def call(self, amount_to_call):
        """Player calls the current bet."""
        call_amount = min(amount_to_call, self.chips)
        self.chips -= call_amount
        self.current_bet += call_amount
        return call_amount

    def raise_bet(self, amount, current_bet):
        """Player raises the bet if they have enough chips."""
        total_bet = current_bet + amount
        if total_bet > self.chips:
            print(f"{self.name} does not have enough to raise. Going all-in.")
            total_bet = self.chips  # All-in if they can't cover the raise
        self.chips -= total_bet
        self.current_bet += total_bet
        return total_bet

    def reset_for_new_round(self):
        """Reset player state for a new hand."""
        self.hand = []
        self.current_bet = 0
        self.active = True

    def __repr__(self):
        return f"{self.name}: Chips={self.chips}, Hand={self.hand}, Active={self.active}"


if __name__ == "__main__":
    # Create a player
    player1 = Player("Alice", 1500)

    # Create a deck and deal 2 cards
    deck = Deck()
    player1.receive_cards(deck.deal(2))

    print(player1)  # See initial state

    # Betting scenario
    player1.bet(200)
    print(player1)

    # Player folds
    player1.fold()
    print(player1)

    # Reset for a new round
    player1.reset_for_new_round()
    print(player1)

