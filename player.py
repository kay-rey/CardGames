from dataclasses import dataclass, field

from card import Card
from deck import Deck


@dataclass
class Player:
    """Represents a player in the Blackjack game."""
    name: str
    money: int = 0
    hand: list[Card] = field(default_factory=list)

    def __str__(self):
        return f'{self.name} has ${self.money}. With a hand of {self.hand}'

    def __repr__(self):
        return f'Player(name=\'{self.name}\', money={self.money}, hand={self.hand}'

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return (self.name, self.hand) == (other.name, other.hand)

    def addMoney(self, amount: int) -> None:
        if amount > 0:
            print('You won $' + str(amount))
            self.money += amount

    def subtractMoney(self, amount: int) -> None:
        if amount > 0:
            print('You lost $' + str(amount))
            self.money -= amount

    def clearHand(self):
        self.hand.clear()

    def getHandValue(self) -> int:
        """
        Calculates the total value of the player's hand, considering Aces.
        """
        blackjack = 21
        hand_total = 0
        num_aces = 0
        for card in self.hand:
            card_value = card.value()
            if card_value == '11': # deals with aces
                num_aces += 1
            hand_total += card_value

        while hand_total > blackjack and num_aces > 0: # implements soft totals with aces
            hand_total -= 10
            num_aces -= 1
        return hand_total


def handTotals(player: Player) -> int:
    total = 0
    for card in player.hand:
        if card.number not in ('Ace', 'King', 'Queen', 'Jack'):
            total += int(card.number)
        elif card.number == 'Ace':
            total += 11
        elif card.number in ('King', 'Queen', 'Jack'):
            total += 10
    return total


def clearHands(players: list[Player]):
    for player in players:
        player.clearHand()


def yesNoInput() -> bool:
    while True:
        playerInput = input()
        if isinstance(playerInput, str):
            playerInputLowered: str = playerInput.lower()
            if playerInputLowered == 'y':
                return True
            elif playerInputLowered == 'n':
                return False
        print('Input a valid option')


def dealACard(player_hand: list[Card], deck: Deck):
    player_hand.append(deck.popDeck())
