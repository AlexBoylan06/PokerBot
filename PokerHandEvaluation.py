from collections import Counter
from itertools import combinations

from Main import Card

class HandEvaluator:
    RANK_ORDER = {rank: index for index, rank in enumerate(Card.RANKS, start=2)}

    @staticmethod
    def get_best_hand(hole_cards, community_cards):
        """Determines the best poker hand from hole and community cards."""
        all_cards = hole_cards + community_cards
        all_combinations = list(combinations(all_cards, 5))  # Generate all 5-card combinations

        best_hand = max(all_combinations, key=HandEvaluator.evaluate_hand)
        return best_hand

    @staticmethod
    def evaluate_hand(hand):
        """Assigns a value to a poker hand based on ranking."""
        ranks = [card.rank for card in hand]
        suits = [card.suit for card in hand]
        rank_counts = Counter(ranks)

        is_flush = len(set(suits)) == 1
        sorted_ranks = sorted([HandEvaluator.RANK_ORDER[r] for r in ranks], reverse=True)
        is_straight = all(sorted_ranks[i] - 1 == sorted_ranks[i + 1] for i in range(len(sorted_ranks) - 1))

        # Assign hand strength values
        if is_flush and is_straight and sorted_ranks[0] == HandEvaluator.RANK_ORDER['A']:
            return (10, sorted_ranks)  # Royal Flush
        elif is_flush and is_straight:
            return (9, sorted_ranks)  # Straight Flush
        elif 4 in rank_counts.values():
            return (8, sorted_ranks)  # Four of a Kind
        elif sorted(rank_counts.values()) == [2, 3]:
            return (7, sorted_ranks)  # Full House
        elif is_flush:
            return (6, sorted_ranks)  # Flush
        elif is_straight:
            return (5, sorted_ranks)  # Straight
        elif 3 in rank_counts.values():
            return (4, sorted_ranks)  # Three of a Kind
        elif list(rank_counts.values()).count(2) == 2:
            return (3, sorted_ranks)  # Two Pair
        elif 2 in rank_counts.values():
            return (2, sorted_ranks)  # One Pair
        else:
            return (1, sorted_ranks)  # High Card

    @staticmethod
    def determine_winner(players, community_cards):
        """Determines the best hand among all players."""
        best_player = None
        best_hand_value = (0, [])

        for player in players:
            if player.active:
                best_hand = HandEvaluator.get_best_hand(player.hand, community_cards)
                hand_value = HandEvaluator.evaluate_hand(best_hand)

                if hand_value > best_hand_value:
                    best_hand_value = hand_value
                    best_player = player

        return best_player, best_hand_value
