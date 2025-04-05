import sys

from blackjack import play_blackjack
from deck import Deck
from player import Player, clear_list_of_hands, yes_no_input
from war import War


def get_game_choice():
    print('Do you want to play [1]Blackjack or [2]War? Type [3] to EXIT')
    while True:
        try:
            player_input = int(input())
            if 0 < player_input <= 3:
                game_choice = player_input
                break
            print('Input a valid option')
        except ValueError:
            print('Input a valid integer')
    return game_choice


def main():
    player = Player('Kevin', 1000)
    dealer = Player('Dealer')
    num_decks = 1
    # decks = createDeck(num_decks)
    deck = Deck()
    deck.create_and_shuffle_deck(num_decks, 'blackjack')
    deck.shuffle_deck()
    deck_amount = len(deck)
    game_choice = get_game_choice()
    while game_choice == 1:
        play_blackjack(player, dealer, deck)
        if player.money <= 0:
            print('You ran out of money. BYE!')
            sys.exit()
        print('Would you like to play again? Y/N')
        play_again_input = yes_no_input()
        if play_again_input:
            if len(deck) < int(deck_amount // 2):
                deck.create_and_shuffle_deck(num_decks, 'blackjack')
                deck.shuffle_deck()
            clear_list_of_hands([player, dealer])
        else:
            game_choice = get_game_choice()

    while game_choice == 2:
        war = War(player)
        war.play_war()
        game_choice = get_game_choice()

    if game_choice == 3:
        print(f'You left with {player.money} in your pocket')
        print('BYEEE!!')
        sys.exit()


if __name__ == '__main__':
    main()
