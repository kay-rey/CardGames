"""
Implementation of the War card game using the card engine in this project
2 players, 1 deck divided evenly among the two players
Win by winning all the cards
"""

from card import WarCard
from deck import Deck
from player import Player


# TODO: Test this function when it is recursively called more than once
def war_option(player: Player, dealer: Player, played_cards: list[WarCard]):
    """
    Used when the players have the same value card. 3 cards are drawn but only the last card that players drew is used to compare to find the winner
    :param player: player1
    :param dealer: player2
    :param played_cards: takes in the cards that were just played to be able to give to the winner
    :return: None
    """
    print('WAR!!')
    war_cards = played_cards
    if (len(player.hand) < 3 and len(player.winnings_pile) < 3) or (
            len(dealer.hand) < 3 and len(dealer.winnings_pile) < 3):
        print('Not enough cards to go to WAR')
        for card in war_cards:
            player.add_card(card)
            dealer.add_card(card)
        return
    if len(player) <= 3:
        player.add_winnings_to_hand()
    if len(dealer) <= 3:
        dealer.add_winnings_to_hand()
    for _ in range(2):
        war_cards.append(player.pop_top_card())
        war_cards.append(dealer.pop_top_card())
    if len(player) > 0 and len(dealer) > 0:
        player_card = player.pop_top_card()
        dealer_card = dealer.pop_top_card()
    else:
        print('There are no more cards')
        return
    print(f'Player 1 revealed a {player_card}. Player 2 revealed a {dealer_card}')
    war_cards += [player_card, dealer_card]
    if player_card.value() > dealer_card.value():
        print(f'{player.name} won the war!')
        player.add_to_winnings(war_cards)
    elif player_card.value() < dealer_card.value():
        print(f'{dealer.name} won this hand')
        dealer.add_to_winnings(war_cards)
    elif player_card.value() == dealer_card.value():
        war_option(player, dealer, war_cards)


def does_player_have_enough_cards(player: Player) -> bool:
    if len(player.hand) < 3 and len(player.winnings_pile) < 3:
        return False
    return True


# TODO: Convert this into an object
def play_war(player: Player):
    """
    The implementation of the card game War
    :param player: takes in the player to also be able to use the money that the player has
    :return: None
    """
    NUM_DECKS: int = 1
    card1: WarCard
    card2: WarCard
    total_bet: int = 0
    player1: Player = player
    player2: Player = Player('Dealer')
    player1_winner = False
    player2_winner = False
    player1_total = 0
    player2_total = 0
    deck: Deck = Deck()
    deck.create_deck(NUM_DECKS, 'war')
    deck.shuffle_deck()
    while True:  # loop starts the betting
        try:
            initial_bet = int(input('How much would you like to bet?\n'))
            total_bet = initial_bet
            if 1 <= total_bet <= player1.money:
                print(f'You bet {total_bet}')
                break
            print('Enter a valid input')
        except ValueError:
            print('Enter a valid number')
    for cards in range(len(deck) // 2):
        player1.add_card(deck.pop_deck())
        player2.add_card(deck.pop_deck())
    print(f'{len(player1)} and {len(player2)}')
    player1.shuffle_hand()
    player2.shuffle_hand()
    player1_total = len(player1.hand) + len(player1.winnings_pile)
    player2_total = len(player2.hand) + len(player2.winnings_pile)
    while min(player1_total, player2_total) > 0:
        if len(player1) <= 1:
            player1.add_winnings_to_hand()
        if len(player2) <= 1:
            player2.add_winnings_to_hand()
        if player1 and player2:
            card1 = player1.pop_top_card()
            card2 = player2.pop_top_card()
        else:
            return
        print(f'{player1.name} revealed a {card1}. {player2.name} revealed a {card2}')
        played_cards = [card1, card2]
        if card1.value() > card2.value():
            print(f'{player1.name} won this hand')
            player1.add_to_winnings(played_cards)
        elif card1.value() < card2.value():
            print(f'{player2.name} won this hand')
            player2.add_to_winnings(played_cards)
        elif card1.value() == card2.value():
            for player_from_list in [player1, player2]:
                if len(player_from_list) > 3 >= len(player_from_list.winnings_pile):
                    player_from_list.add_winnings_to_hand()
            if not does_player_have_enough_cards(player1):
                print('Not enough card to go to war')
                for cards in range(len(player2.hand)):
                    card_moved = player2.pop_top_card()
                    player1.add_card(card_moved)
            elif not does_player_have_enough_cards(player2):
                print('Not enough card to go to war')
                for cards in range(len(player1.hand)):
                    card_moved = player1.pop_top_card()
                    player2.add_card(card_moved)
            else:
                war_option(player1, player2, played_cards)
        player1_total = len(player1.hand) + len(player1.winnings_pile)
        player2_total = len(player2.hand) + len(player2.winnings_pile)
        print(f'{player1_total + player2_total} cards in total')
        print(
            f'{player1.name}:{len(player1)} in hand {len(player1.winnings_pile)} in pile.\n{player2.name}:{len(player2)} in hand {len(player2.winnings_pile)} in pile.')
        # input()
    if player1_total == 52:
        winner = player1.name
        player1.add_money(total_bet)
    elif player2_total == 52:
        winner = player2.name
        player1.subtract_money(total_bet)
    else:
        print('Uh oh there is no winner. Something went wrong')
        winner = 'None'
    print(f'Game Over. {winner} won')
    return
