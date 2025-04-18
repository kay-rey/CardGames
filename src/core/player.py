"""
Player module for card games.

This module provides the Player class and related utility functions for managing
players in various card games. It handles player attributes like name, money,
cards in hand, and winnings pile.
"""

import random
from dataclasses import dataclass, field

from src.core import Card, WarCard, Deck


@dataclass
class Player:
    """
       Represents a player in card games.

       Attributes:
           name (str): Player's name
           money (int): Player's current money/chips
           hand (list[Card]): Cards currently in player's hand
           winnings_pile (list[Card]): Cards won by the player (used in War)
       """
    name: str
    money: int = 0
    hand: list[Card] = field(default_factory=list)
    winnings_pile: list[Card] = field(default_factory=list)

    def __str__(self):
        return f'{self.name} has ${self.money}. With a hand of {self.hand}'

    def __repr__(self):
        return f'Player(name=\'{self.name}\', money={self.money}, hand={self.hand}'

    def __hash__(self) -> int:
        """Enables using Player objects as dictionary keys."""
        return hash(self.name)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return (self.name, self.hand) == (other.name, other.hand)

    def __len__(self) -> int:
        """Returns the number of cards in the player's hand."""
        return len(self.hand)

    def add_money(self, amount: int) -> None:
        if amount > 0:
            print('You won $' + str(amount))
            self.money += amount

    def subtract_money(self, amount: int) -> None:
        if amount > 0:
            print('You lost $' + str(amount))
            self.money -= amount

    def clear_hand(self):
        self.hand.clear()
        self.winnings_pile.clear()

    def add_card(self, card: Card):
        if isinstance(card, Card):
            self.hand.append(card)

    def pop_top_card(self):
        if self.hand:
            return self.hand.pop(0)
        else:
            print('No more cards in hand')
            return None

    def shuffle_hand(self):
        if self.hand:
            random.shuffle(self.hand)

    def get_hand_value(self) -> int:
        """
        Calculates the total value of the player's hand for Blackjack.

        Handles Ace values (1 or 11) automatically based on the total.

        Returns:
            int: The total value of the hand
        """
        blackjack = 21
        hand_total = 0
        num_aces = 0
        for card in self.hand:
            card_value: int = card.value()
            if card_value == 11:  # deals with aces
                num_aces += 1
            hand_total += card_value

        while hand_total > blackjack and num_aces > 0:  # implements soft totals with aces
            hand_total -= 10
            num_aces -= 1
        return hand_total

    def add_to_winnings(self, winnings_pile: list[WarCard]):
        if winnings_pile:
            for card in winnings_pile:
                self.winnings_pile.append(card)

    def add_winnings_to_hand(self):
        if self.winnings_pile:
            print(f'Shuffling winnings into {self.name}\'s hand...')
            self.hand += self.winnings_pile
            self.shuffle_hand()
            self.winnings_pile.clear()

    def get_bet_amount(self) -> int:
        while True:  # loop starts the betting
            try:
                bet_amount = int(input('How much would you like to bet?\n'))
                if 1 <= bet_amount <= self.money:
                    print(f'You bet {bet_amount}')
                    return bet_amount
                print('Enter a valid input')
            except ValueError:
                print('Enter a valid number')


# Utility functions
def clear_list_of_hands(players: list[Player]):
    for player in players:
        player.clear_hand()


def yes_no_input() -> bool:
    while True:
        player_input = input()
        if isinstance(player_input, str):
            player_input_lowered: str = player_input.lower()
            if player_input_lowered == 'y':
                return True
            elif player_input_lowered == 'n':
                return False
        print('Input a valid option')


def deal_card(player_hand: list[Card], deck: Deck):
    player_hand.append(deck.pop_deck())

