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
    INITIAL_HAND_SIZE: int = 2

    def __init__(self, player: Player, deck: Deck):
        self.player = player
        self.deck = deck
        self.dealer = Player('Dealer')
        self.player_turn: bool = True
        self.hands_in_play: Dict[Player, int] = {}  # Type hint for clarity
        self.split_hand_count: int = 0

    def _get_player_action(self, can_split: bool, can_doubledown: bool) -> str:
        """
        Get the player's next action choice.

        Args:
            can_split: Whether splitting is allowed for current hand
            can_doubledown: Whether doubling down is allowed (only on initial two cards)
        """
        # checks to see if the cards are the same value to give the user the option to split

        options: list[str] = ['HIT', 'STAND']
        prompt_parts = list[str] = ['[1]Hit', '[2]Stand']

        if can_doubledown:
            options.append('DOUBLE')
            prompt_parts.append('[3]DoubleDown')
        if can_split:
            options.append('SPLIT')
            prompt_parts.append(f'[{len(options)}]SPLIT')
        prompt = f'Would you like to {", ".join(prompt_parts[:-1])} or {prompt_parts[-1]}?\n'

        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                print('That\'s not a valid option')
            except ValueError:
                print('Enter a valid number')

    def _handle_hit(self, player: Player, bet: int) -> bool:
        """Handle the hit action. Returns False if the player busts"""
        deal_card(player.hand, self.deck)
        player_total = player.get_hand_value()
        print(f'You were dealt a {player.hand[-1]}, your total is now {player_total}')
        if player_total > self.BLACKJACK:
            print('You busted! Bye Bye!!')
            self.player.subtract_money(bet)
            return False
        return True

    def _handle_doubledown(self, player: Player, initial_bet: int) -> None:
        """Handle the double down action. Returns False if the player busts"""
        curr_bet = initial_bet * 2
        deal_card(player.hand, self.deck)
        total = player.get_hand_value()
        print(f'You were dealt a {player.hand[-1]}')
        if total > self.BLACKJACK:
            print('You BUSTED. Better luck next time')
            player.subtract_money(curr_bet)
            return
        self.hands_in_play[player] = curr_bet

    def _handle_split(self, player: Player, initial_bet: int) -> None:
        """Handle splitting a pair of cards"""
        self.split_hand_count += 1
        new_hand = Player(f'Split hand: {str(self.split_hand_count)}', 0, [player.hand.pop()])
        self.split_gameplay(new_hand, initial_bet)
        self.split_gameplay(player, initial_bet)

    # TODO: Finish these methods to make the code more manageable and cleaner
    def _handle_split_gameplay(self, split_player: Player, initial_bet: int):
        pass

    def _handle_dealer_turn(self):
        pass

    def _evaluate_outcome(self, player_total: int, dealer_total: int):
        pass

    def play_blackjack(self) -> None:
        print(f'You have ${self.player.money} in the bank')
        initial_bet = self.player.get_bet_amount()
        total_bet = initial_bet
        while True:  # blackjack begins here
            print('Dealing the cards...')
            for _ in range(self.INITIAL_HAND_SIZE):
                deal_card(self.player.hand, self.deck)
                deal_card(self.dealer.hand, self.deck)
            player_total = self.player.get_hand_value()
            dealer_total = self.dealer.get_hand_value()

            if self._handle_initial_blackjack(player_total, dealer_total, total_bet):
                return

            print(f'The dealer revealed a {self.dealer.hand[0]}')
            print(
                f'You have a hand total of {str(player_total)} with a hand of {self.player.hand[0]} and {self.player.hand[1]}')
            # Player's turn
            cards_in_hand: int = len(self.player.hand)
            while True:
                can_split = (len(self.player.hand) == self.INITIAL_HAND_SIZE and self.player.hand[0].number ==
                             self.player.hand[1].number)
                can_double = (cards_in_hand == self.INITIAL_HAND_SIZE)
                player_input = self._get_player_action(can_split, can_double)

                print('You chose to ' + player_input)
                if player_input == 'HIT':
                    if not self._handle_hit(self.player, total_bet):
                        return
                elif player_input == 'STAND':
                    self.hands_in_play[self.player] = total_bet
                    break
                elif player_input == 'DOUBLEDOWN':
                    self._handle_doubledown(self.player, initial_bet)
                    break
                elif player_input == 'SPLIT':
                    self._handle_split(self.player, initial_bet)
                    break

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
                player_total = hand.get_hand_value()
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

    def player_outcome(self, player_total: int, dealer_total: int) -> str:
        if dealer_total < player_total <= self.BLACKJACK:
            return 'WIN'
        elif player_total < dealer_total <= self.BLACKJACK:
            return 'LOSE'
        else:
            return 'PUSH'

    def X_get_player_action(self, can_split: bool, can_doubledown: bool) -> str:

        if curr_player.hand[0].number == curr_player.hand[1].number:
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

    def _handle_initial_blackjack(self, player_total: int, dealer_total: int, total_bet: int) -> bool:
        if player_total == self.BLACKJACK and dealer_total == self.BLACKJACK:
            print('You both got a blackjack. No one wins')
            return True
        if player_total == self.BLACKJACK:
            winnings = int(total_bet * 1.5)
            print(
                'You hit blackjack with a hand of ' + str(self.player.hand[0]) + ' and ' + str(self.player.hand[1]))
            self.player.add_money(winnings)
            return True
        if dealer_total == self.BLACKJACK:
            print(f'The dealer hit blackjack with a hand of {str(self.dealer.hand[0])} and + {str(
                self.dealer.hand[1])}. Better luck next time')
            self.player.subtract_money(total_bet)
            return True
        return False

    def split_gameplay(self, split_player: Player, initial_bet: int) -> None:
        """
            Handles the gameplay logic for a split hand.  REMOVED GLOBAL VARIABLES
            Args:
                split_player: The Player object representing the split hand.
                initial_bet: The initial bet amount for this hand.
        """
        curr_bet: int = initial_bet
        deal_card(split_player.hand, self.deck)
        print(f'This hand consists of: {split_player.hand[0]} and {split_player.hand[1]}')
        while True:
            player_input: str = self._get_player_action(split_player)
            print('You chose to ' + player_input)
            if player_input == 'HIT':
                deal_card(split_player.hand, self.deck)
                player_total = split_player.get_hand_value()
                print(f'You were dealt a {split_player.hand[-1]}, your total is now {player_total}')
                if player_total > self.BLACKJACK:
                    print('You busted! Bye Bye!!')
                    self.player.subtract_money(curr_bet)
                    break
            elif player_input == 'STAND':
                self.hands_in_play[split_player] = curr_bet
                self.player_turn = False
                break
            elif player_input == 'DOUBLEDOWN':
                total_bet = curr_bet * 2
                deal_card(split_player.hand, self.deck)
                player_total = split_player.get_hand_value()
                print(f'You were dealt a {split_player.hand[-1]} with a total of {player_total}')
                if player_total > self.BLACKJACK:
                    print('You BUSTED. Better luck next time')
                    self.player.subtract_money(total_bet)
                    break
                self.hands_in_play[split_player] = total_bet
                self.player_turn = False
                return
            elif player_input == 'SPLIT':
                self.split_hand_count += 1
                extraHand = Player('split hand: ' + str(self.split_hand_count), 0, [split_player.hand.pop()])
                self.split_gameplay(extraHand, initial_bet)
                self.split_gameplay(split_player, initial_bet)
                self.player_turn = False
