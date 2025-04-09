from src.core.deck import Deck

def test_creating_deck():
    deck = Deck()
    assert len(deck) == 0

    #create standard deck
    deck.create_and_shuffle_deck(1, 'blackjack')
    assert len(deck) == 52

    #create multiple decks
    deck.create_and_shuffle_deck(2, 'blackjack')
    assert len(deck) == 104



def test_war_deck_creation():
    deck = Deck()
    assert len(deck) == 0

    # create standard deck
    deck.create_and_shuffle_deck(1, 'war')
    assert len(deck) == 52

    # create multiple decks
    deck.create_and_shuffle_deck(2, 'war')
    assert len(deck) == 104