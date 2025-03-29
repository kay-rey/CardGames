import sys

from blackjack import playBlackjack
from card import createDeck
from player import Player, clearHand, yesNoInput


def main():
    player = Player('Kevin', 1000)
    dealer = Player('Dealer')
    num_decks = 1
    deck = createDeck(num_decks)
    deckAmount = len(deck)
    print(int(3.5))
    while True:
        playBlackjack(player, dealer, deck)
        print('Would you like to play again? Y/N')
        playAgainInput = yesNoInput()
        if playAgainInput:
            if len(deck) < int(deckAmount // 2):
                print('Shuffling deck...')
                deck = createDeck(num_decks)
            clearHand([player, dealer])
        else:
            print(f'You left with {player.money} in your pocket')
            print('BYEEE!!')
            sys.exit()


if __name__ == '__main__':
    main()
