"""
Blackjack game implementation module.

This module contains the core game logic for Blackjack, including:
- Player actions (hit, stand, double down, split)
- Dealer behavior
- Hand evaluation
- Betting mechanics

Game Rules:
- Players try to get as close to 21 as possible without going over
- Number cards are worth their face value
- Face cards (Jack, Queen, King) are worth 10
- Aces are worth 11 or 1
- Dealer must hit on 16 and stand on 17
"""

from typing import Dict

from deck import Deck
from player import Player, deal_card

# Constants (Good practice to define these at the top)
DEALER_STAND_NUMBER: int = 17
BLACKJACK: int = 21

# Global Variables
HANDS_IN_PLAY: Dict[Player, int] = {}  # Type hint for clarity
SPLIT_HAND_COUNT: int
GAME_DECK: Deck
PLAYER_TURN: bool


def hit_or_stand_player_input() -> str:
    """
       Prompts the player for their next action.

       Returns:
           str: Player's choice:
               'HIT' - Draw another card
               'STAND' - Keep current hand
               'DOUBLEDOWN' - Double bet and receive one final card
       """
    while True:
        try:
            player_input = int(input('Would you like to [1]Hit, [2]Stand, or [3]Double Down?\n'))
            if isinstance(player_input, int):
                if player_input == 1:
                    return 'HIT'
                elif player_input == 2:
                    return 'STAND'
                elif player_input == 3:
                    return 'DOUBLEDOWN'
            print('That\'s not a valid option')
        except ValueError:
            print('Enter a valid number')


def split_or_hit_or_stand() -> str:
    """
        Prompts the player for their next action when split is available.

        Returns:
            str: Player's choice:
                'HIT' - Draw another card
                'STAND' - Keep current hand
                'DOUBLEDOWN' - Double bet and receive one final card
                'SPLIT' - Split matching cards into two hands
        """
    while True:
        try:
            player_input = int(input('Would you like to [1]Hit, [2]Stand, [3]Double Down, or [4]Split?\n'))
            if isinstance(player_input, int):
                if player_input == 1:
                    return 'HIT'
                elif player_input == 2:
                    return 'STAND'
                elif player_input == 3:
                    return 'DOUBLEDOWN'
                elif player_input == 4:
                    return 'SPLIT'
            print('That\'s not a valid option')
        except ValueError:
            print('Enter a valid number')


def split_gameplay(player: Player, player_bank: Player, initial_bet: int) -> None:
    """
        Handles the gameplay logic for a split hand.  REMOVED GLOBAL VARIABLES
        Args:
            player: The Player object representing the split hand.
            player_bank: The Player object representing the player's bank.
            initial_bet: The initial bet amount for this hand.
    """
    global PLAYER_TURN, SPLIT_HAND_COUNT, HANDS_IN_PLAY
    curr_bet: int = initial_bet
    deal_card(player.hand, GAME_DECK)
    print(f'This hand consists of: {player.hand[0]} and {player.hand[1]}')
    while True:
        if player.hand[0].number == player.hand[1].number:
            player_input: str = split_or_hit_or_stand()
        else:
            player_input: str = hit_or_stand_player_input()
        print('You chose to ' + player_input)
        if player_input == 'HIT':
            deal_card(player.hand, GAME_DECK)
            player_total = player.get_hand_value()
            print(f'You were dealt a {player.hand[-1]}, your total is now {player_total}')
            if player_total > BLACKJACK:
                print('You busted! Bye Bye!!')
                player_bank.subtract_money(curr_bet)
                break
        elif player_input == 'STAND':
            HANDS_IN_PLAY[player] = curr_bet
            PLAYER_TURN = False
            break
        elif player_input == 'DOUBLEDOWN':
            total_bet = curr_bet * 2
            deal_card(player.hand, GAME_DECK)
            player_total = player.get_hand_value()
            print(f'You were dealt a {player.hand[-1]} with a total of {player_total}')
            if player_total > BLACKJACK:
                print('You BUSTED. Better luck next time')
                player.subtract_money(total_bet)
                break
            HANDS_IN_PLAY[player] = total_bet
            PLAYER_TURN = False
            return
        elif player_input == 'SPLIT':
            SPLIT_HAND_COUNT += 1
            extraHand = Player('split hand: ' + SPLIT_HAND_COUNT, 0, [player.hand.pop()])
            split_gameplay(extraHand, player_bank, initial_bet)
            split_gameplay(player, player_bank, initial_bet)
            PLAYER_TURN = False


def player_outcome(player_total: int, dealer_total: int) -> str:
    if dealer_total < player_total <= BLACKJACK:
        return 'WIN'
    elif player_total < dealer_total <= BLACKJACK:
        return 'LOSE'
    else:
        return 'PUSH'


# TODO: Convert this into an object
def play_blackjack(player: Player, dealer: Player, decks: Deck) -> None:
    """
        Plays a game of Blackjack.
        Args:
            player: The Player object representing the player.
            dealer: The Player object representing the dealer.
            decks: The Deck object to use for the game.
    """
    global GAME_DECK, PLAYER_TURN, SPLIT_HAND_COUNT, HANDS_IN_PLAY
    player_total: int
    dealer_total: int
    total_bet: int
    # Initialize for a new game
    SPLIT_HAND_COUNT = 0
    HANDS_IN_PLAY = {}
    GAME_DECK = decks
    PLAYER_TURN = True
    print(f'You have ${player.money} in the bank')
    while True:  # loop starts the betting
        try:
            initial_bet = int(input('How much would you like to bet?\n'))
            total_bet = initial_bet
            if 1 <= total_bet <= player.money:
                print(f'You bet {total_bet}')
                break
            print('Enter a valid input')
        except ValueError:
            print('Enter a valid number')
    while True:  # blackjack begins here
        print('Dealing the cards...')
        for _ in range(2):
            deal_card(player.hand, GAME_DECK)
            deal_card(dealer.hand, GAME_DECK)
        player_total = player.get_hand_value()
        dealer_total = dealer.get_hand_value()
        if player_total == 21:
            winnings = int(total_bet * 1.5)
            print('You hit blackjack with a hand of ' + str(player.hand[0]) + ' and ' + str(player.hand[1]))
            player.add_money(winnings)
            return
        if dealer_total == 21:
            print('The dealer hit blackjack with a hand of ' + str(dealer.hand[0]) + ' and ' + str(
                dealer.hand[1]) + '. Better luck next time')
            player.subtract_money(total_bet)
            return
        print(f'The dealer revealed a {dealer.hand[0]}')
        print(f'You have a hand total of {str(player_total)} with a hand of {player.hand[0]} and {player.hand[1]}')
        while PLAYER_TURN:
            if player.hand[0].number == player.hand[
                1].number:  # checks to see if the cards are the same value to give the user the option to split
                player_input: str = split_or_hit_or_stand()
            else:
                player_input: str = hit_or_stand_player_input()
            print('You chose to ' + player_input)
            if player_input == 'HIT':
                deal_card(player.hand, GAME_DECK)
                player_total = player.get_hand_value()
                print(f'You were dealt a {player.hand[-1]}, your total is now {player_total}')
                if player_total > BLACKJACK:
                    print('You busted! Bye Bye!!')
                    player.subtract_money(total_bet)
                    return
            elif player_input == 'STAND':
                HANDS_IN_PLAY[player] = total_bet
                PLAYER_TURN = False
            elif player_input == 'DOUBLEDOWN':
                total_bet = initial_bet * 2
                deal_card(player.hand, GAME_DECK)
                player_total = player.get_hand_value()
                print(f'You were dealt a {player.hand[-1]}')
                if player_total > BLACKJACK:
                    print('You BUSTED. Better luck next time')
                    player.subtract_money(total_bet)
                    return
                HANDS_IN_PLAY[player] = total_bet
                PLAYER_TURN = False
            elif player_input == 'SPLIT':
                SPLIT_HAND_COUNT += 1
                extraHand = Player('split hand : ' + str(SPLIT_HAND_COUNT), 0, [player.hand.pop()])
                split_gameplay(extraHand, player, initial_bet)
                split_gameplay(player, player, initial_bet)
                PLAYER_TURN = False

        if not HANDS_IN_PLAY:
            print('No more hands to play. Better luck next time')
            return
        dealer_total = dealer.get_hand_value()
        print(
            f'The dealer reveals their second card: {dealer.hand[-1]}. Their hand total is {dealer_total}')
        while dealer_total < DEALER_STAND_NUMBER:
            deal_card(dealer.hand, GAME_DECK)
            dealer_total = dealer.get_hand_value()
            print(f'The dealer drew a {dealer.hand[-1]}. Their total is now {dealer_total}')
        dealer_total = dealer.get_hand_value()
        if dealer_total > BLACKJACK:
            print('The dealer BUSTED. You win!')
            for betted_hand in HANDS_IN_PLAY:
                player.add_money(HANDS_IN_PLAY[betted_hand])
            return
        for hand, bet_amount in HANDS_IN_PLAY.items():  # goes through all the hands if the player split hands
            player_total = player.get_hand_value()
            player_outcome_condition = player_outcome(player_total, dealer_total)
            if player_outcome_condition == 'PUSH':
                print(f'You and the dealer both have {player_total}. Push! No one wins')
            elif player_outcome_condition == 'WIN':
                print(
                    f'Your hand of {player_total} beat the dealer\'s {dealer_total}. You WON!! Congrats')
                player.add_money(bet_amount)
            else:
                print(f'Your hand of {player_total} lost to the dealer\'s {dealer_total}. You LOST!!')
                player.subtract_money(bet_amount)
            return
