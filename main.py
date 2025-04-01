import sys

from blackjack import play_blackjack
from deck import Deck
from player import Player, clear_hands, yes_no_input


def main():
    player = Player('Kevin', 1000)
    dealer = Player('Dealer')
    num_decks = 1
    # decks = createDeck(num_decks)
    deck = Deck()
    deck.create_deck(num_decks)
    deck.shuffle_deck()
    deck_amount = len(deck)
    while True:
        play_blackjack(player, dealer, deck)
        if player.money <= 0:
            print('You ran out of money. BYE!')
            sys.exit()
        print('Would you like to play again? Y/N')
        play_again_input = yes_no_input()
        if play_again_input:
            if len(deck) < int(deck_amount // 2):
                deck.create_deck(num_decks)
                deck.shuffle_deck()
            clear_hands([player, dealer])
        else:
            print(f'You left with {player.money} in your pocket')
            print('BYEEE!!')
            sys.exit()


if __name__ == '__main__':
    main()
