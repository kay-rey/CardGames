# Blackjack Game

This project implements a simple Blackjack game in Python.

## Author

- [@kay-rey](https://github.com/kay-rey)

## GitHub Repository

- [CardGames](https://github.com/kay-rey/CardGames)

## Files

- `main.py`: Contains the main entry point and game loop.
- `blackjack.py`: Contains the main game logic, including functions for handling player input, gameplay, and determining
  the outcome of the game.
- `card.py`: Defines the `Card` and `Deck` classes for representing playing cards and decks.
- `player.py`: Defines the `Player` class for representing players (including the dealer) and functions for dealing
  cards and calculating hand totals.

## Dependencies

- Python 3.6+

## How to Run

1. Ensure you have Python installed.
2. Clone the repository: `git clone https://github.com/kay-rey/CardGames.git`
3. Navigate to the project directory: `cd CardGames`
4. Run the game by executing: `python main.py`

## Game Logic

The game follows standard Blackjack rules, with the following features:

- **Betting:** Players can place bets before each round.
- **Dealing:** The player and dealer are dealt two cards each.
- **Player's Turn:**
    -      Players can choose to "Hit" (take another card), "Stand" (end their turn), "Double Down" (double their bet and take one more card), or "Split" (if they have two cards of the same value).
- **Dealer's Turn:**
    -      The dealer reveals their hidden card and hits until their hand total is 17 or more.
- **Outcome:**
    -      The player wins if their hand total is closer to 21 than the dealer's, without exceeding 21.
    -      The player loses if their hand total exceeds 21 or is less than the dealer's total.
    - A push occurs if both player and dealer have the same hand total.
- **Splitting Hands:** If the player has two cards of the same value, they have the option to split their hand into two
  separate hands, each with its own bet.
- **Doubling Down:** The player can double their initial bet, and then gets dealt only one more card.
- **Blackjack:** If a player or dealer gets 21 with their initial two cards, it's a blackjack. Player blackjack pays 1.5
  times the bet.
- **Game Restart:** The game prompts the player to play again after each round.
- **Deck Reshuffle:** The deck is reshuffled when it's depleted to half its original size.

## Code Overview

### `main.py`

- `main()`: The main function that initializes the game, handles the game loop, and manages game state.

### `blackjack.py`

- `hitOrStandPlayerInput()`: Prompts the player to choose to hit or stand.
- `splitOrHitOrStand()`: Prompts the player to choose to hit, stand, double down, or split.
- `splitGameplay()`: Handles the logic for split hands.
- `playerOutcome()`: Determines the outcome of the hand.
- `playBlackjack()`: The main game function that handles the gameplay loop.

### `card.py`

- `Card` class: Represents a playing card with a number and suit.
- `Deck` class: Represents a deck of cards with methods for dealing and shuffling.
    - `createDeck()`: creates a deck with the specified number of standard 52 card decks.
    - `shuffleDeck()`: shuffles the deck.
    - `popDeck()`: removes and returns the top card of the deck.

### `player.py`

- `Player` class: Represents a player with a hand, money, and methods for adding/subtracting money.
    - `addMoney()`: Adds money to the player's balance.
    - `subtractMoney()`: Subtracts money from the player's balance.
    - `clearHand()`: clears all cards from the players hand.
- `handTotals()`: Calculates the total value of a hand.
- `clearHands()`: clears the hands of a list of players.
- `yesNoInput()`: gets a yes or no input from the user.
- `dealACard()`: Deals a card to a player's hand from the deck.

## Global Variables

- `DEALER_STAND_NUMBER`: The dealer's stand number (17).
- `BLACKJACK`: The value of a blackjack (21).
- `HANDS_IN_PLAY`: A dictionary to keep track of the hands in play and their bets.
- `SPLIT_HAND_COUNT`: A counter for split hands.
- `GAME_DECK`: The deck of cards used in the game.
- `PLAYER_TURN`: A boolean to track the player's turn.