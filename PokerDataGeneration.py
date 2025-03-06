import random
from itertools import combinations
from Main import Deck
from Main import Player


class PokerDataGenerator:
    def __init__(self, num_simulations=1000, num_players=6):
        self.num_simulations = num_simulations
        self.num_players = num_players

    def generate_hand(self):
        """Generates a random poker hand with hole cards and community cards."""
        deck = Deck()  # Create and shuffle the deck
        players = [Player(f"Player {i + 1}") for i in range(self.num_players)]

        # Deal hole cards to each player
        for player in players:
            player.receive_cards(deck.deal(2))

        # Generate community cards
        community_cards = deck.deal(5)

        return {
            "players": {player.name: player.hand for player in players},
            "community_cards": community_cards
        }

    def generate_dataset(self):
        """Generates a dataset of simulated poker hands."""
        dataset = []
        for _ in range(self.num_simulations):
            hand = self.generate_hand()
            dataset.append(hand)

        return dataset

    def save_dataset(self, filename="poker_data.json"):
        """Saves generated poker hands to a JSON file."""
        import json
        dataset = self.generate_dataset()
        with open(filename, "w") as file:
            json.dump(dataset, file, indent=4)
        print(f"Dataset saved to {filename}")


# Example usage
if __name__ == "__main__":
    generator = PokerDataGenerator(num_simulations=100)
    generator.save_dataset()
