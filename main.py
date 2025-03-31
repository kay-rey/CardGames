import sys

from blackjack import playBlackjack
from deck import Deck
from player import Player, clearHands, yesNoInput


def main():
    player = Player('Kevin', 1000)
    dealer = Player('Dealer')
    num_decks = 1
    # decks = createDeck(num_decks)
    deck = Deck()
    deck.createDeck(num_decks)
    deck.shuffleDeck()
    deckAmount = len(deck)
    while True:
        playBlackjack(player, dealer, deck)
        if player.money <= 0:
            print('You ran out of money. BYE!')
            sys.exit()
        print('Would you like to play again? Y/N')
        playAgainInput = yesNoInput()
        if playAgainInput:
            if len(deck) < int(deckAmount // 2):
                deck.createDeck(num_decks)
                deck.shuffleDeck()
            clearHands([player, dealer])
        else:
            print(f'You left with {player.money} in your pocket')
            print('BYEEE!!')
            sys.exit()


if __name__ == '__main__':
    main()
