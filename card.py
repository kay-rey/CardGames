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
        return f'Card(number=\'{self.number}\', suit=\'{self.suit}\''

    def value(self) -> int:
        """
                Returns the numerical value of the card.

                Jack, Queen, and King are 10. Ace is 11 or 1.
        """
        if self.number in ('J', 'Q', 'K'):
            return 10
        if self.number == 'A':
            return 11
        else:
            return int(self.number)
