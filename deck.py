from card import Card, WarCard
from random import shuffle

class Deck:
    cards: list[Card]

    def __len__(self) -> int:
        return len(self.cards)

    def create_deck(self, num_decks: int, card_type: str):
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