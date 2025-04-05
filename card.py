"""
Card module for card games.

This module defines the base Card class and its specialized variant WarCard.
These classes represent playing cards with their values and suits, providing
methods to compare and display cards appropriately for different game types.

Classes:
    Card: Base class for playing cards used in games like Blackjack
    WarCard: Specialized card class for the War card game with different card values
"""

from dataclasses import dataclass


@dataclass
class Card:
    """
            Initializes a Card object.

            Args:
                number: The card's number (e.g., '2', '10', 'J', 'Q', 'K', 'A').
                suit: The card's suit (e.g., 'Heart', 'Club', 'Diamond', 'Spade').
    """
    number: str
    suit: str

    def __str__(self):
        return f'{self.number} of {self.suit}s'

    def __repr__(self):
        return f'Card(number=\'{self.number}\', suit=\'{self.suit}\')'

    def value(self) -> int:
        """
        Returns the numerical value of the card for Blackjack.

        Returns:
            int: Card's value where:
                - Number cards (2-10) = their face value
                - Face cards (Jack, Queen, King) = 10
                - Ace = 11 (can be adjusted to 1 in hand calculation)
        """
        if self.number in ('Jack', 'Queen', 'King'):
            return 10
        if self.number == 'Ace':
            return 11
        else:
            return int(self.number)


class WarCard(Card):
    """
    Specialized card class for the War card game.

    Inherits from Card but implements different card values where:
    - Number cards (2-10) = their face value
    - Jack = 11
    - Queen = 12
    - King = 13
    - Ace = 14

    This ensures proper card comparison in the War game where
    Ace is always highest.
    """

    def value(self) -> int:
        if self.number in ['Jack', 'Queen', 'King', 'Ace']:
            return 11 + ['Jack', 'Queen', 'King', 'Ace'].index(self.number)
        else:
            return int(self.number)
