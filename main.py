import sys

from blackjack import play_blackjack
from war import play_war
from deck import Deck
from player import Player, clear_list_of_hands, yes_no_input


def main():
    player = Player('Kevin', 1000)
    dealer = Player('Dealer')
    num_decks = 1
    # decks = createDeck(num_decks)
    deck = Deck()
    deck.create_deck(num_decks, 'blackjack')
    deck.shuffle_deck()
    deck_amount = len(deck)
    game_choice: int = 0
    print('Do you want to play [1]Blackjack or [2]War?')
    while True:
        try:
            player_input = int(input())
            if player_input >= 2:
                if player_input == 1:
                    game_choice = 1
                    break
                elif player_input == 2:
                    game_choice = 2
                    break
            print('Input a valid option')
        except ValueError:
            print('Input a valid integer')
    while game_choice == 1:
        play_blackjack(player, dealer, deck)
        if player.money <= 0:
            print('You ran out of money. BYE!')
            sys.exit()
        print('Would you like to play again? Y/N')
        play_again_input = yes_no_input()
        if play_again_input:
            if len(deck) < int(deck_amount // 2):
                deck.create_deck(num_decks, 'blackjack')
                deck.shuffle_deck()
            clear_list_of_hands([player, dealer])
        else:
            print(f'You left with {player.money} in your pocket')
            print('BYEEE!!')
            sys.exit()

    while game_choice == 2:
        play_war(player)

if __name__ == '__main__':
    main()
