from dataclasses import dataclass, field

from card import Card, Deck


@dataclass
class Player:
    name: str
    money: int = 0
    hand: list[Card] = field(default_factory=list)

    # def __str__(self):
    #     return f'{self.name} has ${self.money}. With a hand of {self.hand}'

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return (self.name, self.hand) == (other.name, other.hand)

    def addMoney(self, amount: int) -> None:
        print('You won $' + str(amount))
        self.money += amount

    def subtractMoney(self, amount: int) -> None:
        print('You lost $' + str(amount))
        self.money -= amount

    def clearHand(self):
        self.hand.clear()


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
