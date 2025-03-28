from random import shuffle  # for shuffle() on the lists
from player import Player, handTotals
from card import Card, createDeck, dealACard

DEALER_STAND_NUMBER: int = 17
BLACKJACK: int = 21


# def dealACard(player: list[Card], deck: list[Card]):
#     player.append(deck.pop())


# def handTotals(player_hand: list[Card]) -> int:
#     total = 0
#     for card in player_hand:
#         if card.number not in ('Ace', 'King', 'Queen', 'Jack'):
#             total += int(card.number)
#         elif card.number == 'Ace':
#             total += 11
#         elif card.number in ('King', 'Queen', 'Jack'):
#             total += 10
#     return total


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
    player_turn, dealer_turn = True, False
    players: list[list[Card]] = []
    player = Player('Kevin', 1000, [])
    dealer = Player('Dealer', 0, [])
    playerTotal: int = 0
    dealerTotal: int = 0
    while True:
        try:
            initialBet = int(input('How much would you like to bet?'))
            if 1 <= initialBet <= player.money:
                print(f'You bet {initialBet}')
                player.money -= initialBet
            break
        except ValueError:
            print('Enter a valid number')
    while True:
        decks: list[Card] = createDeck(num_decks)
        shuffle(decks)
        print('Dealing the cards...')
        for i in range(2):
            dealACard(player.hand, decks)
            dealACard(dealer.hand, decks)
        playerTotal = handTotals(player.hand)
        dealerTotal = handTotals(dealer.hand)
        if playerTotal == 21:
            print('You hit blackjack with a hand of ' + str(player.hand[0]) + ' and ' + str(player.hand[1]))
            break
        if dealerTotal == 21:
            print('The dealer hit blackjack with a hand of ' + str(dealer.hand[0]) + ' and ' + str(
                dealer.hand[1]) + '. Better luck next time')
            break
        print(f'The dealer revealed a {dealer.hand[0]}')
        print(f'You have a hand total of {str(playerTotal)} with a hand of {player.hand[0]} and {player.hand[1]}')
        while player_turn:
            playerInput: str = getPlayerInput()
            print('You chose to ' + playerInput)
            if playerInput == 'STAND':
                player_turn = False
                dealer_turn = True
            elif playerInput == 'HIT':
                dealACard(player.hand, decks)
                playerTotal = handTotals(player.hand)
                print(f'You were dealt a {player.hand[-1]}, your total is now {playerTotal}')
                if playerTotal > BLACKJACK:
                    print('You busted! Bye Bye!!')
                    break
        while dealer_turn:
            print(
                f'The dealer reveals their second card: {dealer.hand[-1]}. Their hand total is {handTotals(dealer.hand)}')
            while handTotals(dealer.hand) < 17:
                dealACard(dealer.hand, decks)
                print(f'The dealer drew a {dealer.hand[-1]}. Their total is now {handTotals(dealer.hand)}')
            playerOutcomeCondition = playerOutcome(handTotals(player.hand), handTotals(dealer.hand))
            if handTotals(dealer.hand) > BLACKJACK:
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
