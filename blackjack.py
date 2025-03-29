from random import shuffle  # for shuffle() on the lists

from card import Card
from player import Player, handTotals, dealACard

DEALER_STAND_NUMBER: int = 17
BLACKJACK: int = 21
TOTAL_BET: int = 0


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


def splitOrHitOrStand() -> str:
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


def playerOutcome(player_total: int, dealer_total: int) -> str:
    if dealer_total < player_total <= BLACKJACK:
        return 'WIN'
    elif player_total < dealer_total <= BLACKJACK:
        return 'LOSE'
    else:
        return 'PUSH'


# def playerAction(player: Player, deck: list[Card], curr_bet: int):
#     if player.hand[0].suit == player.hand[1].suit:
#         playerInput: str = splitOrHitOrStand()
#     else:
#         playerInput: str = hitOrStandPlayerInput()
#     print('You chose to ' + playerInput)
#     if playerInput == 'HIT':
#         dealACard(player, deck)
#         playerTotal = handTotals(player)
#         print(f'You were dealt a {player.hand[-1]}, your total is now {playerTotal}')
#         if playerTotal > BLACKJACK:
#             print('You busted! Bye Bye!!')
#             player.money -= curr_bet
#             break
#     elif playerInput == 'STAND':
#         player_turn = False
#     elif playerInput == 'DOUBLEDOWN':
#         totalBet = curr_bet * 2
#         dealACard(player, deck)
#         print(f'You were dealt a {player.hand[-1]}')
#         player_turn = False
#         if handTotals(player) > BLACKJACK:
#             print('You BUSTED. Better luck next time')
#             player.money -= totalBet
#             break
#     elif playerInput == 'SPLIT':
#         secondHand = Player('second hand', 0, [player.hand.pop()])
#
#         pass


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
            if 1 <= totalBet <= player.money:
                print(f'You bet {totalBet}')
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
        playerTotal = handTotals(player)
        dealerTotal = handTotals(dealer)
        if playerTotal == 21:
            winnings = int(totalBet * 1.5)
            print('You hit blackjack with a hand of ' + str(player.hand[0]) + ' and ' + str(player.hand[1]))
            print(f'You won ${str(winnings)}')
            break
        if dealerTotal == 21:
            print('The dealer hit blackjack with a hand of ' + str(dealer.hand[0]) + ' and ' + str(
                dealer.hand[1]) + '. Better luck next time')
            player.money -= totalBet
            print(f'You lost ${totalBet}')
            break
        print(f'The dealer revealed a {dealer.hand[0]}')
        print(f'You have a hand total of {str(playerTotal)} with a hand of {player.hand[0]} and {player.hand[1]}')
        while player_turn:
            if player.hand[0].number == player.hand[1].number:
                playerInput: str = splitOrHitOrStand()
            else:
                playerInput: str = hitOrStandPlayerInput()
            print('You chose to ' + playerInput)
            if playerInput == 'HIT':
                dealACard(player.hand, decks)
                playerTotal = handTotals(player)
                print(f'You were dealt a {player.hand[-1]}, your total is now {playerTotal}')
                if playerTotal > BLACKJACK:
                    print('You busted! Bye Bye!!')
                    player.money -= totalBet
                    break
            elif playerInput == 'STAND':
                player_turn = False
            elif playerInput == 'DOUBLEDOWN':
                totalBet = initialBet * 2
                dealACard(player.hand, decks)
                print(f'You were dealt a {player.hand[-1]}')
                if handTotals(player) > BLACKJACK:
                    print('You BUSTED. Better luck next time')
                    player.money -= totalBet
                    break
                player_turn = False
            elif playerInput == 'SPLIT':
                secondHand = Player('second hand', 0, [player.hand.pop()])

                pass
        while not player_turn:
            print(
                f'The dealer reveals their second card: {dealer.hand[-1]}. Their hand total is {handTotals(dealer)}')
            while handTotals(dealer) < 17:
                dealACard(dealer.hand, decks)
                print(f'The dealer drew a {dealer.hand[-1]}. Their total is now {handTotals(dealer)}')
            playerOutcomeCondition = playerOutcome(handTotals(player), handTotals(dealer))
            if handTotals(dealer) > BLACKJACK:
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
