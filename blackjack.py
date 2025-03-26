from card import Card, createDeck
from random import shuffle #for shuffle() on the lists

def dealACard(player: list[Card], deck: list[Card]):
    player.append(deck.pop())

def playerTotals(player_hand: list[Card]) -> int:
    total = 0
    for card in player_hand:
        if card.number not in ('Ace', 'King', 'Queen', 'Jack'):
            total += int(card.number)
        elif card.number == 'Ace':
            total += 11
        elif card.number in ('King', 'Queen', 'Jack'):
            total += 10
    return total

def playBlackjack(num_seats: int, num_decks: int):
    players: list[list[Card]] = []
    playerTotal = 0
    dealerTotal = 0
    playerHand: list[Card] = []
    dealerHand: list[Card] = []
    while True:
        decks = createDeck(1)
        shuffle(decks)
        print('Dealing the cards...')
        for i in range(2):
            dealACard(playerHand, decks)
            dealACard(dealerHand, decks)
        playerTotal = playerTotals(playerHand)
        dealerTotal = playerTotals(dealerHand)
        if playerTotal == 21:
            print('You hit blackjack with a hand of ' + str(playerHand[0]) + ' and ' + str(playerHand[1]))
            break
        if dealerTotal == 21:
            print('The dealer hit blackjack with a hand of ' + str(playerHand[0]) + ' and ' + str(playerHand[1]) + '. Better luck next time')
            break
        print(f'The dealer has a hand total of {str(dealerTotal)} with a hand of {dealerHand[0]} and {dealerHand[1]}')
        print(f'You have a hand total of {str(playerTotal)} with a hand of {playerHand[0]} and {playerHand[1]}')


        break

playBlackjack(1, 1)
