"""
Implementation of the War card game using the card engine in this project
2 players, 1 deck divided evenly among the two players
Win by winning all the cards
"""

from card import WarCard
from deck import Deck
from player import Player


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
    if player_card.value() > dealer_card.value():
        print(f'{player.name} won the war!')
        player.add_card(player_card)
        player.add_card(dealer_card)
        for card in war_cards:
            player.add_card(card)
    elif player_card.value() < dealer_card.value():
        print(f'{dealer.name} won this hand')
        dealer.add_card(player_card)
        dealer.add_card(dealer_card)
        for card in war_cards:
            dealer.add_card(card)
    elif player_card.value() == dealer_card.value():
        war_option(player, dealer)

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
    player2: Player = Player('Player 2')
    deck: Deck = Deck()
    deck.create_deck(NUM_DECKS, 'war')
    deck.shuffle_deck()
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
    for cards in range(len(deck) // 2):
        player1.add_card(deck.pop_deck())
        player2.add_card(deck.pop_deck())
    print(f'{len(player1)} and {len(player2)}')
    player1.shuffle_hand()
    player2.shuffle_hand()
    while len(player1) <= 52 or len(player2) <= 52:
        if player1 and player2:
            card1 = player1.pop_top_card()
            card2 = player2.pop_top_card()
        else:
            return
        print(f'{player1.name} revealed a {card1}. {player2.name} revealed a {card2}')
        if card1.value() > card2.value():
            print(f'{player1.name} won this hand')
            player1.add_card(card1)
            player1.add_card(card2)
        elif card1.value() < card2.value():
            print(f'{player2.name} won this hand')
            player2.add_card(card1)
            player2.add_card(card2)
        elif card1.value() == card2.value():
            played_cards = [card1, card2]
            war_option(player1, player2, played_cards)
        print(f'{player1.name} has {len(player1)} cards. {player2.name} has {len(player2)} cards')
        input()
    if len(player1) == 52:
        winner = player1.name
        player1.add_money(total_bet)
    elif len(player2) == 52:
        winner = player2.name
        player1.subtract_money(total_bet)
    else:
        print('Uh oh there is no winner. Something went wrong')
        winner = 'None'
    print(f'Game Over. {winner} won')
