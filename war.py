"""
Implementation of the War card game.

This module defines the logic for a two-player game of War using a standard deck
of cards. The game continues until one player acquires all the cards.
It relies on external 'card', 'deck', and 'player' modules.

Game Rules:
- 2 players (one human, one computer dealer).
- 1 standard 52-card deck, divided evenly at the start.
- Players reveal the top card of their hand simultaneously.
- The player with the higher card wins both cards and adds them to their winnings pile.
- If cards are equal (War):
    - Each player places two cards face down and one card face up.
    - The player with the higher face-up card wins all cards played in that round (including the initial tied cards and the face-down cards).
    - If the face-up cards are also tied, the War process repeats.
    - If a player runs out of cards during a War, they lose the game.
- A player shuffles their winnings pile into their hand when their hand runs out.
- The game ends when one player has all 52 cards.
"""

from card import WarCard
from deck import Deck
from player import Player, clear_list_of_hands


def does_player_have_enough_cards(player: Player) -> bool:
    """
        Checks if a player has enough cards to participate in a 'War'.

        A player needs at least 3 cards (in hand + winnings pile) to place
        two face-down cards and one face-up card during a War.

        Args:
            player (Player): The player to check.

        Returns:
            bool: True if the player has 3 or more cards total, False otherwise.
        """
    if (len(player.hand) + len(player.winnings_pile)) < 3:
        return False
    return True


class War:
    """
    Manages the state and logic for a game of War.

    This class orchestrates the game flow, including dealing cards,
    handling rounds, resolving Wars, and determining the winner.

    Attributes:
        player (Player): The human player participating in the game.
        deck (Deck): The deck of cards used for the game.
        dealer (Player): The computer-controlled dealer.
    """
    NUM_DECKS: int = 1  # Standard war uses only 1 deck
    DECK_LENGTH: int = (52 * NUM_DECKS)

    def __init__(self, player: Player):
        """
        Initializes a new game of War.

        Sets up the player, creates a dealer opponent, and initializes a new deck.

        Args:
            player (Player): The human player participating in the game.
        """
        self.player: Player = player
        self.deck = Deck()
        self.deck.create_and_shuffle_deck(self.NUM_DECKS, 'war')
        self.dealer = Player('Dealer')
        self.player_list: list[Player] = [self.player, self.dealer]

    def _check_hand_count_and_replenish(self) -> bool:
        for players in self.player_list:
            if (len(players) <= 1) and players.winnings_pile:
                players.add_winnings_to_hand()
            if not players.hand:
                return False
        return True

    def _evaluate_outcome(self, player_card: WarCard, dealer_card: WarCard) -> None:
        """
        Evaluates who the outcome of the round. Calls the _war_option function if both the cards are the same
        :param player_card:
        :param dealer_card:
        :return:
        """
        played_cards = [player_card, dealer_card]
        if player_card.value() > dealer_card.value():
            print(f'>> {self.player.name} wins the hand! <<')
            self.player.add_to_winnings(played_cards)
        elif player_card.value() < dealer_card.value():
            print(f'>> {self.dealer.name} wins the hand! <<')
            self.dealer.add_to_winnings(played_cards)
        elif player_card.value() == dealer_card.value():  # If the cards have the same value, initiate the war gameplay
            print('WAR!!')
            self._war_option(played_cards)

    def play_war(self) -> None:
        """
        Executes the gameplay logic for the card game War.

        This method manages the betting phase, deals cards to the player and dealer,
        compares cards in each round, handles 'war' scenarios when cards have equal value,
        and determines the winner based on who accumulates all the cards. It also
        updates the player's money based on the outcome of the game.
        """
        # --- Betting Phase ---
        initial_bet = self.player.get_bet_amount()
        total_bet = initial_bet

        # --- Dealing Phase ---
        for _ in range(len(self.deck) // 2):  # Deal half the deck to each of the players
            self.player.add_card(self.deck.pop_deck())
            self.dealer.add_card(self.deck.pop_deck())
        player_total = len(self.player.hand) + len(self.player.winnings_pile)
        dealer_total = len(self.dealer.hand) + len(self.dealer.winnings_pile)

        print("\n--- Game Start ---")

        # End the game logic once one player has no cards in hand or their winnings
        round_num = 0
        while min(player_total, dealer_total) > 0:
            round_num += 1
            # Check if players need to replenish their hands from winnings
            if not self._check_hand_count_and_replenish():
                return
            player_card = self.player.pop_top_card()
            dealer_card = self.dealer.pop_top_card()
            print(f'{self.player.name} reveals: {player_card}')
            print(f'{self.dealer.name} reveals: {dealer_card}')
            # Check the card values to evaluate the outcome
            self._evaluate_outcome(player_card, dealer_card)
            # --- Round Summary ---
            player_total = len(self.player.hand) + len(self.player.winnings_pile)
            dealer_total = len(self.dealer.hand) + len(self.dealer.winnings_pile)
            print(f'Card Counts:')
            print(
                f' {self.player.name}: {len(self.player.hand)} hand / {len(self.player.winnings_pile)} winnings (Total: {player_total})')
            print(
                f' {self.dealer.name}: {len(self.dealer.hand)} hand / {len(self.dealer.winnings_pile)} winnings (Total: {dealer_total})')
            # input()
            print('\n')
        if player_total == self.DECK_LENGTH:
            winner = self.player.name
            print(f'{winner} wins the game!')
            self.player.add_money(total_bet)
            print(f'Your total money is now ${self.player.money}.')

        elif dealer_total == self.DECK_LENGTH:
            winner = self.dealer.name
            print(f'{winner} wins the game!')
            self.player.subtract_money(total_bet)
            print(f'Your total money is now ${self.player.money}.')
        else:
            print('Uh oh there is no winner. Something went wrong')
        print(f'The game lasted {round_num} rounds.')
        clear_list_of_hands([self.player, self.dealer])
        return

    def _war_option(self, played_cards: list[WarCard]):
        """
        Used when the players have the same value card. 3 cards are drawn but only the last card that players drew is used to compare to find the winner
        :param played_cards: takes in the cards that were just played to be able to give to the winner
        :return: None
        """
        war_cards = played_cards
        # Check if either player has enough cards to play war
        for player_from_list in [self.player, self.dealer]:
            # If the player has enough in their winnings pile but not in their hand then shuffle the winnings pile into the hand
            if len(player_from_list) < 3 and (len(player_from_list.winnings_pile) + len(player_from_list) >= 3):
                player_from_list.add_winnings_to_hand()
        if not does_player_have_enough_cards(self.player):
            # If player doesn't have enough cards to go to war then that player loses
            print(f'{self.player.name} does not have enough cards for War!')
            for cards in range(len(self.player.hand)):
                war_cards.append(self.player.pop_top_card())
            self.dealer.add_to_winnings(war_cards)
            print(f'{self.dealer.name} wins the War by default.')
            return
        elif not does_player_have_enough_cards(self.dealer):
            print(f'{self.dealer.name} does not have enough cards for War!')
            for cards in range(len(self.dealer.hand)):
                war_cards.append(self.dealer.pop_top_card())
            self.player.add_to_winnings(war_cards)
            print(f'{self.player.name} wins the War by default.')
            return
        # Place 2 face-down cards each
        print("Players place 2 cards face down and 1 face up...")
        for _ in range(2):
            war_cards.append(self.player.pop_top_card())
            war_cards.append(self.dealer.pop_top_card())
        # Place 1 face-up card each (the deciding cards)
        if len(self.player) > 0 and len(self.dealer) > 0:
            player_war_card = self.player.pop_top_card()
            dealer_war_card = self.dealer.pop_top_card()
        else:
            print('There are no more cards')
            return
        print(f'{self.player.name} reveals War card: {player_war_card}')
        print(f'{self.dealer.name} reveals War card: {dealer_war_card}')
        war_cards += [player_war_card, dealer_war_card]
        if player_war_card.value() > dealer_war_card.value():
            print(f'>> {self.player.name} wins the War! <<')
            self.player.add_to_winnings(war_cards)
        elif player_war_card.value() < dealer_war_card.value():
            print(f'>> {self.dealer.name} wins the War! <<')
            self.dealer.add_to_winnings(war_cards)
        elif player_war_card.value() == dealer_war_card.value():
            print("!!! DOUBLE WAR !!! (Tied again!)")
            self._war_option(war_cards)
