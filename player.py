from dataclasses import dataclass, field

from card import Card


@dataclass
class Player:
    name: str
    money: int = 0
    hand: list[Card] = field(default_factory=list)

    def __str__(self):
        return f'{self.name} has ${self.money}. With a hand of {self.hand}'


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


def clearHand(players: list[Player]):
    for player in players:
        player.hand.clear()


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


def dealACard(player: Player, deck: list[Card]):
    player.hand.append(deck.pop())
