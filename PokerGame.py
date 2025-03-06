from Main import Deck, Player
from PokerHandEvaluation import HandEvaluator

class PokerGame:
    def __init__(self, players, big_blind=50):
        """
        Initialize the poker game with a list of players and big blind value.
        """
        self.players = players  # List of Player objects
        self.deck = Deck()  # Create and shuffle the deck
        self.pot = 0  # Total chips in the pot
        self.community_cards = []  # Shared board cards
        self.big_blind = big_blind
        self.small_blind = big_blind // 2
        self.current_bet = 0  # The current highest bet in a round
        self.active_players = players[:]  # Players still in the hand

    def assign_blinds(self):
        """Assign small and big blinds to the first two players."""
        self.players[0].bet(self.small_blind)
        self.players[1].bet(self.big_blind)
        self.current_bet = self.big_blind  # Track the highest bet

    def deal_hole_cards(self):
        """Deal two hole cards to each active player."""
        for player in self.players:
            player.receive_cards(self.deck.deal(2))

    def deal_community_cards(self, num):
        """Deal community cards (flop, turn, river)."""
        self.community_cards.extend(self.deck.deal(num))

    def collect_bets(self):
        """Collect all bets from players and add to the pot."""
        for player in self.players:
            self.pot += player.current_bet
            player.current_bet = 0  # Reset individual bets

    def betting_round(self):
        """Handles a betting round where players act in turn."""
        for player in self.active_players:
            if player.active:
                action = input(f"{player.name}, choose action: (check, bet, call, raise, fold): ").lower()
                if action == "fold":
                    player.fold()
                elif action == "bet":
                    amount = int(input(f"Enter bet amount (min {self.big_blind}): "))
                    player.bet(amount)
                    self.current_bet = amount
                elif action == "call":
                    player.call(self.current_bet)
                elif action == "raise":
                    amount = int(input("Enter raise amount: "))
                    player.raise_bet(amount, self.current_bet)
                    self.current_bet += amount
                elif action == "check":
                    player.check()
        self.collect_bets()

    def play_hand(self):
        """Runs through an entire hand of Texas Hold'em."""
        print("\nStarting a new hand...")
        self.assign_blinds()
        self.deal_hole_cards()

        print("\n--- Pre-Flop ---")
        self.betting_round()

        print("\n--- Flop ---")
        self.deal_community_cards(3)
        print(f"Community Cards: {self.community_cards}")
        self.betting_round()

        print("\n--- Turn ---")
        self.deal_community_cards(1)
        print(f"Community Cards: {self.community_cards}")
        self.betting_round()

        print("\n--- River ---")
        self.deal_community_cards(1)
        print(f"Community Cards: {self.community_cards}")
        self.betting_round()

        print("\n--- Showdown ---")
        self.determine_winner()

    def determine_winner(self):
        """Placeholder for hand evaluation logic."""
        print("Evaluating hands... (Hand evaluation logic needed)")

    def reset_round(self):
        """Reset game state for a new round."""
        self.deck = Deck()  # New shuffled deck
        self.pot = 0
        self.community_cards = []
        self.current_bet = 0
        for player in self.players:
            player.reset_for_new_round()

    def determine_winner(self):
        """Determines the winner by evaluating hands."""
        winner, best_hand_value = HandEvaluator.determine_winner(self.active_players, self.community_cards)
        print(f"\nWinner: {winner.name} with hand {best_hand_value}")


if __name__ == "__main__":
    players = [Player("Alice"), Player("Bob"), Player("Charlie")]
    game = PokerGame(players)

    game.play_hand()  # Simulate a full hand

