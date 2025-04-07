"""
CardGames - A collection of classic card games implemented in Python.

This module serves as the main entry point for the card games application.
It provides a command-line interface for users to choose and play different
card games including Blackjack and War.

Games available:
    - Blackjack: A classic casino game where players try to get as close to 21 as possible
    - War: A two-player card game where the highest card wins

Usage:
    Run this file directly to start the game:
    $ python main.py
"""

import sys

from blackjack import Blackjack
from deck import Deck
from player import Player, yes_no_input
from war import War


def get_game_choice():
    """
        Prompts the user to choose a game to play.

        Returns:
            int: The user's game choice:
                 1 for Blackjack
                 2 for War
                 3 to exit the program
        """
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
    """
        Main game loop that handles game selection and player progression.

        Initializes the player with starting money and manages the deck of cards.
        Allows the player to switch between games or exit the program.
        """
    # Initialize player with starting money
    player = Player('Kevin', 1000)
    # Main game selection loop
    game_choice = get_game_choice()
    while game_choice == 1:  # Blackjack
        blackjack = Blackjack(player)
        blackjack.play_blackjack()
        player.clear_hand()
        if player.money <= 0:
            print('You ran out of money. BYE!')
            sys.exit()
        print('Would you like to play again? Y/N')
        play_again_input = yes_no_input()
        if not play_again_input:
            game_choice = get_game_choice()

    while game_choice == 2:  # War
        war = War(player)
        war.play_war()
        player.clear_hand()
        game_choice = get_game_choice()

    if game_choice == 3:  # Exit
        print(f'You left with {player.money} in your pocket')
        print('BYEEE!!')
        sys.exit()


if __name__ == '__main__':
    main()
