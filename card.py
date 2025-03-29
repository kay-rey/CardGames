from dataclasses import dataclass


@dataclass
class Card:
    number: str
    suit: str

    def __str__(self):
        return f'{self.number} of {self.suit}s'


def createDeck(num_decks) -> list[Card]:
    deck = []
    suits = ['Spade', 'Heart', 'Club', 'Diamond']
    number = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    for currNumber in number:
        for currSuit in suits:
            currCard = Card(currNumber, currSuit)
            deck.append(currCard)
    if num_decks > 0:
        deck *= num_decks
    return deck
