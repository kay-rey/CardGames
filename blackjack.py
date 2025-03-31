from typing import Dict

from card import Card
from deck import Deck
from player import Player, handTotals, dealACard

# Constants (Good practice to define these at the top)
DEALER_STAND_NUMBER: int = 17
BLACKJACK: int = 21

# Global Variables
HANDS_IN_PLAY: Dict[Player, int] = {}  # Type hint for clarity
SPLIT_HAND_COUNT: int
GAME_DECK: Deck
PLAYER_TURN: bool


def hitOrStandPlayerInput() -> str:
    while True:
        try:
            playerInput = int(input('Would you like to [1]Hit, [2]Stand, or [3]Double Down?\n'))
            if isinstance(playerInput, int):
                if playerInput == 1:
                    return 'HIT'
                elif playerInput == 2:
                    return 'STAND'
                elif playerInput == 3:
                    return 'DOUBLEDOWN'
            print('That\'s not a valid option')
        except ValueError:
            print('Enter a valid number')


def splitOrHitOrStand() -> str:  # if the player has two of the same value cards
    while True:
        try:
            playerInput = int(input('Would you like to [1]Hit, [2]Stand, [3]Double Down, or [4]Split?\n'))
            if isinstance(playerInput, int):
                if playerInput == 1:
                    return 'HIT'
                elif playerInput == 2:
                    return 'STAND'
                elif playerInput == 3:
                    return 'DOUBLEDOWN'
                elif playerInput == 4:
                    return 'SPLIT'
            print('That\'s not a valid option')
        except ValueError:
            print('Enter a valid number')


def splitGameplay(player: Player, player_bank: Player, initial_bet: int) -> None:
    """
        Handles the gameplay logic for a split hand.  REMOVED GLOBAL VARIABLES
        Args:
            player: The Player object representing the split hand.
            player_bank: The Player object representing the player's bank.
            initial_bet: The initial bet amount for this hand.
        """
    global PLAYER_TURN, SPLIT_HAND_COUNT, HANDS_IN_PLAY
    curr_bet: int = initial_bet
    dealACard(player.hand, GAME_DECK)
    print(f'This hand consists of: {player.hand[0]} and {player.hand[1]}')
    while True:
        if player.hand[0].number == player.hand[1].number:
            playerInput: str = splitOrHitOrStand()
        else:
            playerInput: str = hitOrStandPlayerInput()
        print('You chose to ' + playerInput)
        if playerInput == 'HIT':
            dealACard(player.hand, GAME_DECK)
            playerTotal = handTotals(player)
            print(f'You were dealt a {player.hand[-1]}, your total is now {playerTotal}')
            if playerTotal > BLACKJACK:
                print('You busted! Bye Bye!!')
                player_bank.subtractMoney(curr_bet)
                break
        elif playerInput == 'STAND':
            HANDS_IN_PLAY[player] = curr_bet
            PLAYER_TURN = False
            break
        elif playerInput == 'DOUBLEDOWN':
            totalBet = curr_bet * 2
            dealACard(player.hand, GAME_DECK)
            print(f'You were dealt a {player.hand[-1]} with a total of {handTotals(player)}')
            if handTotals(player) > BLACKJACK:
                print('You BUSTED. Better luck next time')
                player.subtractMoney(totalBet)
                break
            HANDS_IN_PLAY[player] = totalBet
            PLAYER_TURN = False
            break
        elif playerInput == 'SPLIT':
            SPLIT_HAND_COUNT += 1
            extraHand = Player('split hand: ' + SPLIT_HAND_COUNT, 0, [player.hand.pop()])
            splitGameplay(extraHand, player_bank, initial_bet)
            splitGameplay(player, player_bank, initial_bet)
            PLAYER_TURN = False


def playerOutcome(player_total: int, dealer_total: int) -> str:
    if dealer_total < player_total <= BLACKJACK:
        return 'WIN'
    elif player_total < dealer_total <= BLACKJACK:
        return 'LOSE'
    else:
        return 'PUSH'


def playBlackjack(player: Player, dealer: Player, decks: Deck) -> None:
    """
        Plays a game of Blackjack.
        Args:
            player: The Player object representing the player.
            dealer: The Player object representing the dealer.
            decks: The Deck object to use for the game.
    """
    global GAME_DECK, PLAYER_TURN, SPLIT_HAND_COUNT, HANDS_IN_PLAY
    heartsTwo = Card('2', 'Heart')
    clubsTwo = Card('2', 'Club')
    testingPlayer = Player('Testing', 200, [heartsTwo, clubsTwo])
    playerTotal: int
    dealerTotal: int
    totalBet: int
    # Initialize for a new game
    SPLIT_HAND_COUNT = 0
    HANDS_IN_PLAY = {}
    GAME_DECK = decks
    PLAYER_TURN = True
    print(f'You have ${player.money} in the bank')
    while True:  # loop starts the betting
        try:
            initial_bet = int(input('How much would you like to bet?\n'))
            totalBet = initial_bet
            if 1 <= totalBet <= player.money:
                print(f'You bet {totalBet}')
                break
            print('Enter a valid input')
        except ValueError:
            print('Enter a valid number')
    while True:  # blackjack begins here
        print('Dealing the cards...')
        for _ in range(2):
            dealACard(player.hand, GAME_DECK)
            dealACard(dealer.hand, GAME_DECK)
        playerTotal = handTotals(player)
        dealerTotal = handTotals(dealer)
        if playerTotal == 21:
            winnings = int(totalBet * 1.5)
            print('You hit blackjack with a hand of ' + str(player.hand[0]) + ' and ' + str(player.hand[1]))
            player.addMoney(winnings)
            return
        if dealerTotal == 21:
            print('The dealer hit blackjack with a hand of ' + str(dealer.hand[0]) + ' and ' + str(
                dealer.hand[1]) + '. Better luck next time')
            player.subtractMoney(totalBet)
            return
        print(f'The dealer revealed a {dealer.hand[0]}')
        print(f'You have a hand total of {str(playerTotal)} with a hand of {player.hand[0]} and {player.hand[1]}')
        while PLAYER_TURN:
            if player.hand[0].number == player.hand[
                1].number:  # checks to see if the cards are the same value to give the user the option to split
                playerInput: str = splitOrHitOrStand()
            else:
                playerInput: str = hitOrStandPlayerInput()
            print('You chose to ' + playerInput)
            if playerInput == 'HIT':
                dealACard(player.hand, GAME_DECK)
                playerTotal = handTotals(player)
                print(f'You were dealt a {player.hand[-1]}, your total is now {playerTotal}')
                if playerTotal > BLACKJACK:
                    print('You busted! Bye Bye!!')
                    player.subtractMoney(totalBet)
                    return
            elif playerInput == 'STAND':
                HANDS_IN_PLAY[player] = totalBet
                PLAYER_TURN = False
            elif playerInput == 'DOUBLEDOWN':
                totalBet = initial_bet * 2
                dealACard(player.hand, GAME_DECK)
                print(f'You were dealt a {player.hand[-1]}')
                if handTotals(player) > BLACKJACK:
                    print('You BUSTED. Better luck next time')
                    player.subtractMoney(totalBet)
                    return
                HANDS_IN_PLAY[player] = totalBet
                PLAYER_TURN = False
            elif playerInput == 'SPLIT':
                SPLIT_HAND_COUNT += 1
                extraHand = Player('split hand : ' + str(SPLIT_HAND_COUNT), 0, [player.hand.pop()])
                splitGameplay(extraHand, player, initial_bet)
                splitGameplay(player, player, initial_bet)
                PLAYER_TURN = False

        if not HANDS_IN_PLAY:
            print('No more hands to play. Better luck next time')
            return
        print(
            f'The dealer reveals their second card: {dealer.hand[-1]}. Their hand total is {handTotals(dealer)}')
        while handTotals(dealer) < DEALER_STAND_NUMBER:
            dealACard(dealer.hand, GAME_DECK)
            print(f'The dealer drew a {dealer.hand[-1]}. Their total is now {handTotals(dealer)}')
        dealer_total = handTotals(dealer)
        if dealer_total > BLACKJACK:
            print('The dealer BUSTED. You win!')
            for betted_hand in HANDS_IN_PLAY:
                player.addMoney(HANDS_IN_PLAY[betted_hand])
            return
        for hand, bet_amount in HANDS_IN_PLAY.items():  # goes through all the hands if the player split hands
            playerOutcomeCondition = playerOutcome(handTotals(hand), dealer_total)
            if playerOutcomeCondition == 'PUSH':
                print(f'You and the dealer both have {handTotals(hand)}. Push! No one wins')
            elif playerOutcomeCondition == 'WIN':
                print(
                    f'Your hand of {handTotals(hand)} beat the dealer\'s {handTotals(dealer)}. You WON!! Congrats')
                player.addMoney(bet_amount)
            else:
                print(f'Your hand of {handTotals(hand)} lost to the dealer\'s {handTotals(dealer)}. You LOST!!')
                player.subtractMoney(bet_amount)
            return
