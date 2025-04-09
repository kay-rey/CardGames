from unittest.mock import patch

import pytest

from src.core.card import WarCard
from src.core.player import Player
from src.games.war import War, does_player_have_enough_cards


@pytest.fixture
def war_game():
    player = Player("Test Player", 1000)
    return War(player)


def test_war_initialization(war_game):
    assert isinstance(war_game.player, Player)
    assert isinstance(war_game.dealer, Player)
    assert war_game.dealer.name == "Dealer"
    assert len(war_game.player_list) == 2
    assert war_game.deck is not None


def test_check_hand_count_and_replenish(war_game):
    # Test when hands are empty
    assert war_game._check_hand_count_and_replenish() == False

    # Test when player needs to replenish
    war_game.player.hand.clear()
    war_game.player.add_to_winnings([WarCard("2", "Heart")])
    war_game.dealer.hand.clear()
    war_game.dealer.add_to_winnings([WarCard("3", "Heart")])
    assert war_game._check_hand_count_and_replenish() == True
    assert len(war_game.player.hand) == 1

    # Test when player has no cards at all
    war_game.player.hand.clear()
    war_game.player.winnings_pile.clear()
    assert war_game._check_hand_count_and_replenish() == False


def test_does_player_have_enough_cards():
    player = Player("Test", 1000)

    # Test with no cards
    assert does_player_have_enough_cards(player) == False

    # Test with 2 cards (not enough for war)
    player.add_card(WarCard("2", "Heart"))
    player.add_card(WarCard("3", "Heart"))
    assert does_player_have_enough_cards(player) == False

    # Test with 3 cards (minimum for war)
    player.add_card(WarCard("4", "Heart"))
    assert does_player_have_enough_cards(player) == True

    # Test with cards in winnings pile
    player.hand.clear()
    player.add_to_winnings([WarCard("2", "Heart"), WarCard("3", "Heart"), WarCard("4", "Heart")])
    assert does_player_have_enough_cards(player) == True


def test_evaluate_outcome(war_game):
    # Test player wins
    with patch('builtins.print'):
        war_game._evaluate_outcome(
            WarCard("King", "Heart"),  # Value 13
            WarCard("Queen", "Spade")  # Value 12
        )
    assert len(war_game.player.winnings_pile) == 2
    assert len(war_game.dealer.winnings_pile) == 0

    # Reset winnings
    war_game.player.winnings_pile.clear()
    war_game.dealer.winnings_pile.clear()

    # Test dealer wins
    with patch('builtins.print'):
        war_game._evaluate_outcome(
            WarCard("Jack", "Heart"),  # Value 11
            WarCard("Queen", "Spade")  # Value 12
        )
    assert len(war_game.dealer.winnings_pile) == 2
    assert len(war_game.player.winnings_pile) == 0


@patch('builtins.print')
def test_war_option(mock_print, war_game):
    # Setup initial war scenario
    played_cards = [WarCard("Queen", "Heart"), WarCard("Queen", "Spade")]

    # Test when player doesn't have enough cards
    war_game.player.hand.clear()
    war_game.player.add_card(WarCard("2", "Heart"))  # Only one card
    war_game._war_option(played_cards)
    assert len(war_game.dealer.winnings_pile) > 0
    assert len(war_game.player.hand) == 0

    # Reset for next test
    war_game.dealer.winnings_pile.clear()

    # Test when dealer doesn't have enough cards
    war_game.player.hand.clear()
    war_game.dealer.hand.clear()
    # Give player enough cards
    for _ in range(4):
        war_game.player.add_card(WarCard("2", "Heart"))
    # Give dealer only one card
    war_game.dealer.add_card(WarCard("3", "Spade"))

    war_game._war_option(played_cards)
    assert len(war_game.player.winnings_pile) > 0
    assert len(war_game.dealer.hand) == 0


@patch('builtins.print')
@patch('builtins.input')
def test_play_war(mock_input, mock_print, war_game):
    # Mock bet amount
    mock_input.return_value = "100"

    # Clear and setup specific hands for testing
    war_game.player.hand.clear()
    war_game.dealer.hand.clear()

    # Give all cards to player (win condition)
    for _ in range(war_game.DECK_LENGTH):
        war_game.player.add_card(WarCard("2", "Heart"))

    # Play game
    war_game.play_war()

    # Verify game ended correctly
    assert len(war_game.player.hand) == 0  # Hands should be cleared after game
    assert len(war_game.dealer.hand) == 0
    assert len(war_game.player.winnings_pile) == 0
    assert len(war_game.dealer.winnings_pile) == 0


def test_war_deck_setup(war_game):
    # Test initial deck setup
    assert war_game.NUM_DECKS == 1
    assert war_game.DECK_LENGTH == 52

    # Reset and deal cards
    war_game.player.hand.clear()
    war_game.dealer.hand.clear()
    war_game.deck.create_and_shuffle_deck(war_game.NUM_DECKS, 'war')

    # Deal cards
    for _ in range(len(war_game.deck) // 2):
        war_game.player.add_card(war_game.deck.pop_deck())
        war_game.dealer.add_card(war_game.deck.pop_deck())

    # Verify equal distribution
    assert len(war_game.player.hand) == 26
    assert len(war_game.dealer.hand) == 26
    assert len(war_game.deck) == 0
