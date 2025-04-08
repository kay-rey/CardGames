from unittest.mock import patch

import pytest

from card import Card, WarCard
from player import Player, yes_no_input, clear_list_of_hands


@pytest.fixture
def player():
    return Player("Test Player", 1000)


def test_player_creation(player):
    assert player.name == "Test Player"
    assert player.money == 1000
    assert len(player.hand) == 0
    assert len(player.winnings_pile) == 0


def test_player_str_representation(player):
    assert str(player) == "Test Player has $1000. With a hand of []"
    player.add_card(Card("Ace", "Spade"))
    assert str(player) == "Test Player has $1000. With a hand of [Card(number='Ace', suit='Spade')]"


def test_player_equality(player):
    other_player = Player("Test Player", 2000)  # Different money, same name and empty hand
    assert player == other_player  # Should be equal based on name and hand

    other_player.add_card(Card("2", "Heart"))
    assert player != other_player  # Different hand


def test_player_length(player):
    assert len(player) == 0
    player.add_card(Card("Ace", "Spade"))
    assert len(player) == 1


def test_player_money_management(player):
    initial_money = player.money

    # Test adding money
    with patch('builtins.print'):
        player.add_money(500)
    assert player.money == initial_money + 500

    # Test subtracting money
    with patch('builtins.print'):
        player.subtract_money(200)
    assert player.money == initial_money + 300

    # Test with zero or negative amounts
    original_money = player.money
    player.add_money(0)
    player.add_money(-100)
    assert player.money == original_money  # Should not change


def test_player_hand_management(player):
    # Test adding cards
    card1 = Card("Ace", "Spade")
    card2 = Card("King", "Heart")

    player.add_card(card1)
    player.add_card(card2)
    assert len(player.hand) == 2

    # Test non-card objects
    player.add_card("not a card")
    assert len(player.hand) == 2  # Should not add non-Card objects

    # Test clearing hand
    player.clear_hand()
    assert len(player.hand) == 0
    assert len(player.winnings_pile) == 0


def test_player_shuffle_hand(player):
    # Add several cards
    cards = [
        Card("Ace", "Spade"),
        Card("King", "Heart"),
        Card("Queen", "Diamond"),
        Card("Jack", "Club")
    ]
    for card in cards:
        player.add_card(card)

    original_order = player.hand.copy()
    player.shuffle_hand()

    # Verify cards are the same but potentially in different order
    assert len(player.hand) == len(original_order)
    assert set(str(card) for card in player.hand) == set(str(card) for card in original_order)


def test_player_winnings_management(player):
    # Test adding to winnings pile
    winnings = [WarCard("2", "Heart"), WarCard("3", "Spade")]
    player.add_to_winnings(winnings)
    assert len(player.winnings_pile) == 2

    # Test adding winnings to hand
    with patch('builtins.print'):
        player.add_winnings_to_hand()
    assert len(player.hand) == 2
    assert len(player.winnings_pile) == 0


@patch('builtins.input')
def test_player_get_bet_amount(mock_input, player):
    # Test valid bet
    mock_input.return_value = "500"
    assert player.get_bet_amount() == 500

    # Test bet too high
    mock_input.side_effect = ["2000", "500"]
    assert player.get_bet_amount() == 500

    # Test invalid input then valid input
    mock_input.side_effect = ["abc", "500"]
    assert player.get_bet_amount() == 500


def test_clear_list_of_hands():
    players = [
        Player("Player1", 1000),
        Player("Player2", 1000)
    ]
    for player in players:
        player.add_card(Card("Ace", "Spade"))

    clear_list_of_hands(players)
    assert all(len(player.hand) == 0 for player in players)


@patch('builtins.input')
def test_yes_no_input(mock_input):
    # Test 'yes' inputs
    for yes in ['y', 'Y']:
        mock_input.return_value = yes
        assert yes_no_input() is True

    # Test 'no' inputs
    for no in ['n', 'N']:
        mock_input.return_value = no
        assert yes_no_input() is False

    # Test invalid then valid input
    mock_input.side_effect = ['invalid', 'y']
    assert yes_no_input() is True
