from random import shuffle  # for shuffle() on the lists

from card import Card, dealACard
from player import Player, handTotals, yesNoInput

DEALER_STAND_NUMBER: int = 17
BLACKJACK: int = 21
TOTAL_BET: int = 0


def hitOrStandPlayerInput() -> str:
    while True:
        playerInput = input('Would you like to [H]it or [S]tand?')
        if isinstance(playerInput, str):
            playerInputLowered: str = playerInput.lower()
            if playerInputLowered == 'h':
                return 'HIT'
            elif playerInputLowered == 's':
                return 'STAND'
        print('Input a valid option')


def playerOutcome(player_total: int, dealer_total: int) -> str:
    if dealer_total < player_total <= BLACKJACK:
        return 'WIN'
    elif player_total < dealer_total <= BLACKJACK:
        return 'LOSE'
    else:
        return 'PUSH'


def playBlackjack(player: Player, dealer: Player, decks: list[Card]):
    player_turn: bool = True
    playerTotal: int
    dealerTotal: int
    initialBet: int
    totalBet: int
    print(f'You have ${player.money} in the bank')
    while True:  # loop starts the betting
        try:
            initialBet = int(input('How much would you like to bet?\n'))
            totalBet = initialBet
            if 1 <= initialBet <= player.money:
                print(f'You bet {initialBet}')
                break
            print('Enter a valid input')
        except ValueError:
            print('Enter a valid number')
    while True:  # blackjack begins here
        shuffle(decks)
        print('Dealing the cards...')
        for i in range(2):
            dealACard(player.hand, decks)
            dealACard(dealer.hand, decks)
        playerTotal = handTotals(player.hand)
        dealerTotal = handTotals(dealer.hand)
        if playerTotal == 21:
            winnings = initialBet * 2
            print('You hit blackjack with a hand of ' + str(player.hand[0]) + ' and ' + str(player.hand[1]))
            print(f'You won ${str(winnings)}')
            break
        if dealerTotal == 21:
            print('The dealer hit blackjack with a hand of ' + str(dealer.hand[0]) + ' and ' + str(
                dealer.hand[1]) + '. Better luck next time')
            player.money -= initialBet
            print(f'You lost ${initialBet}')
            break
        print(f'The dealer revealed a {dealer.hand[0]}')
        print(f'You have a hand total of {str(playerTotal)} with a hand of {player.hand[0]} and {player.hand[1]}')
        print('Would you like to double down?')
        doubleDownAnswer = yesNoInput()
        if doubleDownAnswer:
            totalBet = initialBet * 2
            dealACard(player.hand, decks)
            print(f'You were dealt a {player.hand[-1]}')
            player_turn = False
        while player_turn:
            playerInput: str = hitOrStandPlayerInput()
            print('You chose to ' + playerInput)
            if playerInput == 'STAND':
                player_turn = False
            elif playerInput == 'HIT':
                dealACard(player.hand, decks)
                playerTotal = handTotals(player.hand)
                print(f'You were dealt a {player.hand[-1]}, your total is now {playerTotal}')
                if playerTotal > BLACKJACK:
                    print('You busted! Bye Bye!!')
                    break
        while not player_turn:
            print(
                f'The dealer reveals their second card: {dealer.hand[-1]}. Their hand total is {handTotals(dealer.hand)}')
            while handTotals(dealer.hand) < 17:
                dealACard(dealer.hand, decks)
                print(f'The dealer drew a {dealer.hand[-1]}. Their total is now {handTotals(dealer.hand)}')
            playerOutcomeCondition = playerOutcome(handTotals(player.hand), handTotals(dealer.hand))
            if handTotals(dealer.hand) > BLACKJACK:
                print('The dealer BUSTED. You win!')
                player.money += totalBet
                break
            if playerOutcomeCondition == 'PUSH':
                print('Push! No one wins')
                break
            elif playerOutcomeCondition == 'WIN':
                print('You WON!! Congrats')
                player.money += totalBet
                break
            else:
                print('You lost! The house always wins')
                player.money -= totalBet
                break
        break
