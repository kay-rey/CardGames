import sys

from blackjack import playBlackjack
from card import createDeck
from player import Player, clearHand


def main():
    player = Player('Kevin', 1000, [])
    dealer = Player('Dealer', 0, [])
    deck = createDeck(1)
    deckAmount = len(deck)
    while True:
        playBlackjack(player, dealer, deck)
        while True:
            playerInput = input('Would you like to play again? Y/N')
            if isinstance(playerInput, str):
                playerInputLowered: str = playerInput.lower()
                if playerInputLowered == 'y':
                    if len(deck) < int(
                            deckAmount // 2):  # create a new deck if there are less than half remaining in the deck
                        print('Shuffling deck...')
                        deck = createDeck(1)
                    clearHand([player, dealer])
                    break
                elif playerInputLowered == 'n':
                    print(f'You left with {player.money} in your pocket')
                    print('BYEEE!!')
                    sys.exit()
            print('Input a valid option')


if __name__ == '__main__':
    main()
