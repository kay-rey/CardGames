"""
Deck module for card games.

This module provides the Deck class which represents a standard deck of playing cards.
It supports creating multiple decks, shuffling, and drawing cards for various card games.
"""

from random import shuffle

from src.core import Card, WarCard


class Deck:
    """
        A class representing a deck of playing cards.

        The deck can be configured for different card games and can contain
        multiple standard 52-card decks shuffled together.

        Attributes:
            cards (list[Card]): List of cards currently in the deck
        """

    def __init__(self):
        """Initialize an empty deck."""
        self.cards: list[Card] = []

    def __len__(self) -> int:
        """Return the number of cards remaining in the deck."""
        return len(self.cards)

    def create_and_shuffle_deck(self, num_decks: int, card_type: str):
        """
                Creates and shuffles a new deck or multiple decks of cards.

                Args:
                    num_decks (int): Number of standard 52-card decks to use
                    card_type (str): Type of cards to create ('war' or 'blackjack')
                """
        deck = []
        suits = ['Spade', 'Heart', 'Club', 'Diamond']
        number = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for curr_number in number:
            for curr_suit in suits:
                if card_type == 'war':
                    currCard = WarCard(curr_number, curr_suit)
                else:
                    currCard = Card(curr_number, curr_suit)
                deck.append(currCard)
        if num_decks > 0:
            deck *= num_decks
        shuffle(deck)
        self.cards = deck

    def shuffle_deck(self):
        print('Shuffling deck')
        shuffle(self.cards)

    def pop_deck(self) -> Card | None:
        if self.cards:
            return self.cards.pop()
        else:
            print('Deck is empty is empty')
            return None
