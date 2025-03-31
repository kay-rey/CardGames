from card import Card, Deck
from player import Player, handTotals, dealACard

DEALER_STAND_NUMBER: int = 17
BLACKJACK: int = 21
TOTAL_BET: int = 0
GAME_DECK: list[Card]
PLAYER_TURN: bool


def hitOrStandPlayerInput() -> str:
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


def splitGameplay(hand: list[Card], bank: int):
    pass


def playerOutcome(player_total: int, dealer_total: int) -> str:
    if dealer_total < player_total <= BLACKJACK:
        return 'WIN'
    elif player_total < dealer_total <= BLACKJACK:
        return 'LOSE'
    else:
        return 'PUSH'


def playBlackjack(player: Player, dealer: Player, decks: Deck):
    global GAME_DECK
    global PLAYER_TURN
    playerTotal: int
    dealerTotal: int
    initialBet: int
    totalBet: int
    splitHandCount: int = 0
    GAME_DECK = decks
    PLAYER_TURN = True
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
        print('Dealing the cards...')
        for i in range(2):
            dealACard(player.hand, GAME_DECK)
            dealACard(dealer.hand, GAME_DECK)
        playerTotal = handTotals(player)
        dealerTotal = handTotals(dealer)
        if playerTotal == 21:
            winnings = int(totalBet * 1.5)
            print('You hit blackjack with a hand of ' + str(player.hand[0]) + ' and ' + str(player.hand[1]))
            print(f'You won ${str(winnings)}')
            player.addMoney(winnings)
            break
        if dealerTotal == 21:
            print('The dealer hit blackjack with a hand of ' + str(dealer.hand[0]) + ' and ' + str(
                dealer.hand[1]) + '. Better luck next time')
            player.subtractMoney(totalBet)
            break
        print(f'The dealer revealed a {dealer.hand[0]}')
        print(f'You have a hand total of {str(playerTotal)} with a hand of {player.hand[0]} and {player.hand[1]}')
        while PLAYER_TURN:
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
                    player.subtractMoney(totalBet)
                    break
            elif playerInput == 'STAND':
                PLAYER_TURN = False
            elif playerInput == 'DOUBLEDOWN':
                totalBet = initialBet * 2
                dealACard(player.hand, GAME_DECK)
                print(f'You were dealt a {player.hand[-1]}')
                if handTotals(player) > BLACKJACK:
                    print('You BUSTED. Better luck next time')
                    player.subtractMoney(totalBet)
                    break
                PLAYER_TURN = False
            elif playerInput == 'SPLIT':
                splitHandCount += 1
                extraHand = Player('split hand : ' + splitHandCount, 0, [player.hand.pop()])
                splitGameplay(extraHand.hand, player.money)
                splitGameplay(player.hand, player.money)

                pass
        while not PLAYER_TURN:
            print(
                f'The dealer reveals their second card: {dealer.hand[-1]}. Their hand total is {handTotals(dealer)}')
            while handTotals(dealer) < 17:
                dealACard(dealer.hand, GAME_DECK)
                print(f'The dealer drew a {dealer.hand[-1]}. Their total is now {handTotals(dealer)}')
            playerOutcomeCondition = playerOutcome(handTotals(player), handTotals(dealer))
            if handTotals(dealer) > BLACKJACK:
                print('The dealer BUSTED. You win!')
                player.addMoney(totalBet)
                break
            if playerOutcomeCondition == 'PUSH':
                print('Push! No one wins')
                break
            elif playerOutcomeCondition == 'WIN':
                print('You WON!! Congrats')
                player.addMoney(totalBet)
                break
            else:
                print('You lost! The house always wins')
                player.subtractMoney(totalBet)
                break
        break
