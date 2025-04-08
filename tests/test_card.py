from card import Card, WarCard


def test_card_creation():
    card = Card('Ace', 'Heart')
    assert card.number == 'Ace'
    assert card.suit == 'Heart'
    assert str(card) == 'Ace of Hearts'


def test_card_value():
    # Test number cards
    card = Card("2", "Heart")
    assert card.value() == 2
    card = Card("10", "Spade")
    assert card.value() == 10

    # Test face cards
    card = Card("Jack", "Club")
    assert card.value() == 10
    card = Card("Queen", "Diamond")
    assert card.value() == 10
    card = Card("King", "Heart")
    assert card.value() == 10

    # Test Ace
    card = Card("Ace", "Spade")
    assert card.value() == 11


def test_war_card_values():
    # Test number cards
    card = WarCard("2", "Heart")
    assert card.value() == 2
    card = WarCard("10", "Spade")
    assert card.value() == 10

    # Test face cards
    card = WarCard("Jack", "Club")
    assert card.value() == 11
    card = WarCard("Queen", "Diamond")
    assert card.value() == 12
    card = WarCard("King", "Heart")
    assert card.value() == 13

    # Test Ace
    card = WarCard("Ace", "Spade")
    assert card.value() == 14