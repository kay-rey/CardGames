from card import Card
from dataclasses import dataclass

@dataclass
class Player:
    name: str
    money: int
    hand: list[Card]

    def __str__(self):
        return f'{self.name} has ${self.money}. With a hand of {self.hand}'

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