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


class Blackjack:
    # Global Constants
    NUM_DECKS: int = 1
    DEALER_STAND_NUMBER: int = 17
    BLACKJACK: int = 21
    # Global variables
    player_turn: bool
    hands_in_play: Dict[Player, int] = {}  # Type hint for clarity
    split_hand_count: int

    def __init__(self, player: Player, deck: Deck):
        self.player = player
        self.deck = deck
        self.dealer = Player('Dealer')

    def play_blackjack(self):
        print(f'You have ${self.player.money} in the bank')
        while True:  # loop starts the betting
            try:
                initial_bet = int(input('How much would you like to bet?\n'))
                total_bet = initial_bet
                if 1 <= total_bet <= self.player.money:
                    print(f'You bet {total_bet}')
                    break
                print('Enter a valid input')
            except ValueError:
                print('Enter a valid number')
        while True:  # blackjack begins here
            print('Dealing the cards...')
            for _ in range(2):
                deal_card(self.player.hand, self.deck)
                deal_card(self.dealer.hand, self.deck)
            player_total = self.player.get_hand_value()
            dealer_total = self.dealer.get_hand_value()
            if player_total == 21:
                winnings = int(total_bet * 1.5)
                print(
                    'You hit blackjack with a hand of ' + str(self.player.hand[0]) + ' and ' + str(self.player.hand[1]))
                self.player.add_money(winnings)
                return
            if dealer_total == 21:
                print('The dealer hit blackjack with a hand of ' + str(self.dealer.hand[0]) + ' and ' + str(
                    self.dealer.hand[1]) + '. Better luck next time')
                self.player.subtract_money(total_bet)
                return
            print(f'The dealer revealed a {self.dealer.hand[0]}')
            print(
                f'You have a hand total of {str(player_total)} with a hand of {self.player.hand[0]} and {self.player.hand[1]}')
            # Player's turn
            self.player_turn = True
            while self.player_turn:
                player_input = self.split_or_hit_or_stand()
                print('You chose to ' + player_input)
                if player_input == 'HIT':
                    deal_card(self.player.hand, self.deck)
                    player_total = self.player.get_hand_value()
                    print(f'You were dealt a {self.player.hand[-1]}, your total is now {player_total}')
                    if player_total > self.BLACKJACK:
                        print('You busted! Bye Bye!!')
                        self.player.subtract_money(total_bet)
                        return
                elif player_input == 'STAND':
                    self.hands_in_play[self.player] = total_bet
                    self.player_turn = False
                elif player_input == 'DOUBLEDOWN':
                    total_bet = initial_bet * 2
                    deal_card(self.player.hand, self.deck)
                    player_total = self.player.get_hand_value()
                    print(f'You were dealt a {self.player.hand[-1]}')
                    if player_total > self.BLACKJACK:
                        print('You BUSTED. Better luck next time')
                        self.player.subtract_money(total_bet)
                        return
                    self.hands_in_play[self.player] = total_bet
                    self.player_turn = False
                elif player_input == 'SPLIT':
                    self.split_hand_count += 1
                    extraHand = Player('split hand : ' + str(self.split_hand_count), 0, [self.player.hand.pop()])
                    self.split_gameplay(extraHand, self.player, initial_bet)
                    self.split_gameplay(self.player, self.player, initial_bet)
                    self.player_turn = False

            if not self.hands_in_play:
                print('No more hands to play. Better luck next time')
                return
            dealer_total = self.dealer.get_hand_value()
            print(
                f'The dealer reveals their second card: {self.dealer.hand[-1]}. Their hand total is {dealer_total}')
            while dealer_total < self.DEALER_STAND_NUMBER:
                deal_card(self.dealer.hand, self.deck)
                dealer_total = self.dealer.get_hand_value()
                print(f'The dealer drew a {self.dealer.hand[-1]}. Their total is now {dealer_total}')
            dealer_total = self.dealer.get_hand_value()
            if dealer_total > self.BLACKJACK:
                print('The dealer BUSTED. You win!')
                for betted_hand in self.hands_in_play:
                    self.player.add_money(self.hands_in_play[betted_hand])
                return
            for hand, bet_amount in self.hands_in_play.items():  # goes through all the hands if the player split hands
                player_total = self.player.get_hand_value()
                player_outcome_condition = self.player_outcome(player_total, dealer_total)
                if player_outcome_condition == 'PUSH':
                    print(f'You and the dealer both have {player_total}. Push! No one wins')
                elif player_outcome_condition == 'WIN':
                    print(
                        f'Your hand of {player_total} beat the dealer\'s {dealer_total}. You WON!! Congrats')
                    self.player.add_money(bet_amount)
                else:
                    print(f'Your hand of {player_total} lost to the dealer\'s {dealer_total}. You LOST!!')
                    self.player.subtract_money(bet_amount)
                return

    def player_outcome(self, player_total: int, dealer_total: int) -> str:
        if dealer_total < player_total <= self.BLACKJACK:
            return 'WIN'
        elif player_total < dealer_total <= self.BLACKJACK:
            return 'LOSE'
        else:
            return 'PUSH'

    def split_or_hit_or_stand(self) -> str:
        """
            Prompts the player for their next action when split is available.

            Returns:
                str: Player's choice:
                    'HIT' - Draw another card
                    'STAND' - Keep current hand
                    'DOUBLEDOWN' - Double bet and receive one final card
                    'SPLIT' - Split matching cards into two hands
            """
        # checks to see if the cards are the same value to give the user the option to split
        if self.player.hand[0].number == self.player.hand[1].number:
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
        else:
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

    def split_gameplay(self, player: Player, player_bank: Player, initial_bet: int) -> None:
        """
            Handles the gameplay logic for a split hand.  REMOVED GLOBAL VARIABLES
            Args:
                player: The Player object representing the split hand.
                player_bank: The Player object representing the player's bank.
                initial_bet: The initial bet amount for this hand.
        """
        curr_bet: int = initial_bet
        deal_card(player.hand, self.deck)
        print(f'This hand consists of: {player.hand[0]} and {player.hand[1]}')
        while True:
            player_input: str = self.split_or_hit_or_stand()
            print('You chose to ' + player_input)
            if player_input == 'HIT':
                deal_card(player.hand, self.deck)
                player_total = player.get_hand_value()
                print(f'You were dealt a {player.hand[-1]}, your total is now {player_total}')
                if player_total > self.BLACKJACK:
                    print('You busted! Bye Bye!!')
                    player_bank.subtract_money(curr_bet)
                    break
            elif player_input == 'STAND':
                self.hands_in_play[player] = curr_bet
                self.player_turn = False
                break
            elif player_input == 'DOUBLEDOWN':
                total_bet = curr_bet * 2
                deal_card(player.hand, self.deck)
                player_total = player.get_hand_value()
                print(f'You were dealt a {player.hand[-1]} with a total of {player_total}')
                if player_total > self.BLACKJACK:
                    print('You BUSTED. Better luck next time')
                    player.subtract_money(total_bet)
                    break
                self.hands_in_play[player] = total_bet
                self.player_turn = False
                return
            elif player_input == 'SPLIT':
                self.split_hand_count += 1
                extraHand = Player('split hand: ' + str(self.split_hand_count), 0, [player.hand.pop()])
                self.split_gameplay(extraHand, player_bank, initial_bet)
                self.split_gameplay(player, player_bank, initial_bet)
                self.player_turn = False
