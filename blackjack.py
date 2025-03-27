from random import shuffle  # for shuffle() on the lists

from card import Card, createDeck

DEALER_STAND_NUMBER: int = 17
PLAYER_TURN = True
DEALER_TURN = False
BLACKJACK: int = 21


def dealACard(player: list[Card], deck: list[Card]):
    player.append(deck.pop())


def handTotals(player_hand: list[Card]) -> int:
    total = 0
    for card in player_hand:
        if card.number not in ('Ace', 'King', 'Queen', 'Jack'):
            total += int(card.number)
        elif card.number == 'Ace':
            total += 11
        elif card.number in ('King', 'Queen', 'Jack'):
            total += 10
    return total


def getPlayerInput() -> str:
    playerInputLowered: str = ''
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
    if player_total > dealer_total:
        return 'WIN'
    elif player_total < dealer_total:
        return 'LOSE'
    else:
        return 'PUSH'


def playBlackjack(num_seats: int, num_decks: int):
    global PLAYER_TURN, DEALER_TURN
    players: list[list[Card]] = []
    playerTotal: int = 0
    dealerTotal: int = 0
    playerHand: list[Card] = []
    dealerHand: list[Card] = []
    while True:
        decks: list[Card] = createDeck(num_decks)
        shuffle(decks)
        print('Dealing the cards...')
        for i in range(2):
            dealACard(playerHand, decks)
            dealACard(dealerHand, decks)
        playerTotal = handTotals(playerHand)
        dealerTotal = handTotals(dealerHand)
        if playerTotal == 21:
            print('You hit blackjack with a hand of ' + str(playerHand[0]) + ' and ' + str(playerHand[1]))
            break
        if dealerTotal == 21:
            print('The dealer hit blackjack with a hand of ' + str(dealerHand[0]) + ' and ' + str(
                dealerHand[1]) + '. Better luck next time')
            break
        print(f'The dealer revealed a {dealerHand[0]}')
        print(f'You have a hand total of {str(playerTotal)} with a hand of {playerHand[0]} and {playerHand[1]}')
        while PLAYER_TURN:
            playerInput: str = getPlayerInput()
            print('You chose to ' + playerInput)
            if playerInput == 'STAND':
                PLAYER_TURN = False
                DEALER_TURN = True
            elif playerInput == 'HIT':
                dealACard(playerHand, decks)
                playerTotal = handTotals(playerHand)
                print(f'You were dealt a {playerHand[-1]}, your total is now {playerTotal}')
                if playerTotal > BLACKJACK:
                    print('You busted! Bye Bye!!')
                    break
        while DEALER_TURN:
            print(
                f'The dealer reveals their second card: {dealerHand[-1]}. Their hand total is {handTotals(dealerHand)}')
            while handTotals(dealerHand) < 17:
                dealACard(dealerHand, decks)
                print(f'The dealer drew a {dealerHand[-1]}. Their total is now {handTotals(dealerHand)}')
            playerOutcomeCondition = playerOutcome(handTotals(playerHand), handTotals(dealerHand))
            if handTotals(dealerHand) > BLACKJACK:
                print('The dealer BUSTED. You win!')
                break
            if playerOutcomeCondition == 'PUSH':
                print('Push! No one wins')
                break
            elif playerOutcomeCondition == 'WIN':
                print('You WON!! Congrats')
                break
            else:
                print('You lost! The house always wins')
                break
        break


playBlackjack(1, 1)
