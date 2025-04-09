from unittest.mock import patch

import pytest

from src.games.blackjack import Blackjack
from src.core.card import Card
from src.core.player import Player


@pytest.fixture
def blackjack_game():
    player = Player("Test Player", 1000)
    return Blackjack(player)


def test_blackjack_initialization(blackjack_game):
    assert isinstance(blackjack_game.player, Player)
    assert isinstance(blackjack_game.dealer, Player)
    assert blackjack_game.dealer.name == "Dealer"
    assert len(blackjack_game.hands_in_play) == 0
    assert blackjack_game.split_hand_count == 0


@patch('builtins.input')
def test_blackjack_initial_deal(mock_input, blackjack_game):
    # Mock the input for bet amount
    mock_input.return_value = "100"

    # Mock the game action input (2 for "STAND")
    mock_input.side_effect = ["100", "2"]

    # Simulate a game start
    blackjack_game.deck.create_and_shuffle_deck(1, 'blackjack')
    initial_deck_size = len(blackjack_game.deck)

    # Start a game (but don't actually play through it)
    with patch('builtins.print'):  # Suppress print statements
        blackjack_game._check_and_shuffle_deck()
        blackjack_game.player.get_bet_amount()
        # Deal initial cards
        for _ in range(blackjack_game.INITIAL_HAND_SIZE):
            blackjack_game.dealer.add_card(blackjack_game.deck.pop_deck())
            blackjack_game.player.add_card(blackjack_game.deck.pop_deck())

    # Verify initial deal
    assert len(blackjack_game.player.hand) == 2
    assert len(blackjack_game.dealer.hand) == 2
    assert len(blackjack_game.deck) == initial_deck_size - 4


def test_evaluate_outcome(blackjack_game):
    # Test player win
    assert blackjack_game._evaluate_outcome(20, 19) == 'WIN'

    # Test dealer win
    assert blackjack_game._evaluate_outcome(19, 20) == 'LOSE'

    # Test push
    assert blackjack_game._evaluate_outcome(20, 20) == 'PUSH'

    # Test bust
    assert blackjack_game._evaluate_outcome(22, 20) == 'LOSE'
    assert blackjack_game._evaluate_outcome(20, 22) == 'WIN'


@patch('builtins.input')
def test_get_player_action(mock_input, blackjack_game):
    # Test basic hit/stand options
    mock_input.return_value = "1"  # Hit
    action = blackjack_game._get_player_action(can_split=False, can_doubledown=False)
    assert action == "HIT"

    mock_input.return_value = "2"  # Stand
    action = blackjack_game._get_player_action(can_split=False, can_doubledown=False)
    assert action == "STAND"


@patch('builtins.input')
def test_handle_initial_blackjack(mock_input, blackjack_game):
    # Set up a player blackjack
    blackjack_game.player.hand.clear()
    blackjack_game.player.add_card(Card("Ace", "Spade"))
    blackjack_game.player.add_card(Card("King", "Heart"))

    # Set up dealer's non-blackjack hand
    blackjack_game.dealer.hand.clear()
    blackjack_game.dealer.add_card(Card("10", "Diamond"))
    blackjack_game.dealer.add_card(Card("9", "Club"))

    with patch('builtins.print'):  # Suppress print statements
        result = blackjack_game._handle_initial_blackjack(21, 19, 100)
    assert result == True  # Player has blackjack


@patch('builtins.input')
def test_handle_dealer_turn(mock_input, blackjack_game):
    # Clear and set up dealer's hand
    blackjack_game.dealer.hand.clear()
    blackjack_game.dealer.add_card(Card("6", "Heart"))
    blackjack_game.dealer.add_card(Card("10", "Spade"))

    # Create deck for dealer to draw from
    blackjack_game.deck.create_and_shuffle_deck(1, 'blackjack')

    # Add a hand in play
    test_player = Player("Test Split Hand", 0)
    blackjack_game.hands_in_play[test_player] = 100

    with patch('builtins.print'):  # Suppress print statements
        dealer_total = blackjack_game._handle_dealer_turn()

        if dealer_total is not None:
            # Dealer reached a valid standing total
            assert dealer_total >= blackjack_game.DEALER_STAND_NUMBER
        else:
            # Dealer must have busted
            assert blackjack_game.dealer.get_hand_value() > blackjack_game.BLACKJACK


@patch('builtins.input')
def test_dealer_bust_scenario(mock_input, blackjack_game):
    # Clear and set up dealer's hand that will bust
    blackjack_game.dealer.hand.clear()
    blackjack_game.dealer.add_card(Card("10", "Heart"))
    blackjack_game.dealer.add_card(Card("6", "Spade"))
    blackjack_game.dealer.add_card(Card("6", "Diamond"))  # Total: 22 (bust)

    # Add a hand in play
    test_player = Player("Test Player", 0)
    blackjack_game.hands_in_play[test_player] = 100

    with patch('builtins.print'):  # Suppress print statements
        result = blackjack_game._handle_dealer_turn()

    assert result is None  # Dealer busted
    assert blackjack_game.dealer.get_hand_value() > blackjack_game.BLACKJACK


@patch('builtins.input')
def test_dealer_stands_scenario(mock_input, blackjack_game):
    # Clear and set up dealer's hand that will stand
    blackjack_game.dealer.hand.clear()
    blackjack_game.dealer.add_card(Card("10", "Heart"))
    blackjack_game.dealer.add_card(Card("8", "Spade"))  # Total: 18 (should stand)

    # Add a hand in play
    test_player = Player("Test Player", 0)
    blackjack_game.hands_in_play[test_player] = 100

    with patch('builtins.print'):  # Suppress print statements
        result = blackjack_game._handle_dealer_turn()

    assert result == 18  # Dealer should stand on 18
    assert result >= blackjack_game.DEALER_STAND_NUMBER
