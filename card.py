from dataclasses import dataclass
from random import shuffle


@dataclass
class Card:
    number: str
    suit: str

    def __str__(self):
        return f'{self.number} of {self.suit}s'


class Deck:
    deck: list[Card]

    def __len__(self) -> int:
        return len(self.deck)

    def createDeck(self, num_decks):
        deck = []
        suits = ['Spade', 'Heart', 'Club', 'Diamond']
        number = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for currNumber in number:
            for currSuit in suits:
                currCard = Card(currNumber, currSuit)
                deck.append(currCard)
        if num_decks > 0:
            deck *= num_decks
        self.deck = deck

    def shuffleDeck(self):
        print('Shuffling deck')
        shuffle(self.deck)

    def popDeck(self) -> Card | None:
        if self.deck:
            return self.deck.pop()
        else:
            print('Deck is empty is empty')
            return None
