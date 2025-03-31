from card import Card
from random import shuffle

class Deck:
    cards: list[Card]

    def __len__(self) -> int:
        return len(self.cards)

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
        self.cards = deck

    def shuffleDeck(self):
        print('Shuffling deck')
        shuffle(self.cards)

    def popDeck(self) -> Card | None:
        if self.cards:
            return self.cards.pop()
        else:
            print('Deck is empty is empty')
            return None