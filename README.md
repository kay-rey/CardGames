# DeckPy 🃏

A polished Python implementation of classic card games featuring clean architecture, comprehensive testing, and maintainable code quality.

## 🎯 Project Overview

This repository demonstrates solid Python development practices through the implementation of multiple card games. Built with modular architecture principles, DeckPy showcases object-oriented design, error handling, and maintainable code structure.

## ✨ Key Features

### 🏗️ **Architecture & Design**

- **Modular Design**: Clean separation of concerns between core components and game logic
- **Object-Oriented**: Well-structured classes with clear responsibilities
- **Type Hints**: Python type annotation support for better code quality
- **Dataclasses**: Modern Python features for clean, maintainable code

### 🎮 **Game Implementations**

- **Blackjack**: Casino-style implementation with core features
  - Split hands, double down
  - Multi-deck support with automatic reshuffling
  - Standard dealer rules
- **War**: Classic two-player card game with complete rule implementation
  - Handles "War" scenarios with tied cards
  - Automatic hand replenishment from winnings pile
  - Edge case handling for insufficient cards

### 🧪 **Quality Assurance**

- **Testing Framework**: pytest-based test suite for core components
- **Test Coverage**: Tests for card logic, deck operations, and player actions
- **Input Validation**: User input handling and error checking
- **Code Structure**: Consistent formatting and organization

### 🚀 **Technical Features**

- **Standard Library Only**: Pure Python implementation using built-in modules
- **Efficient Design**: Clean algorithms and data structures
- **Memory Management**: Proper cleanup and resource handling
- **Cross-Platform**: Works on Python 3.13+ environments

## 🏗️ System Architecture

```
src/
├── core/           # Core game components
│   ├── card.py     # Card classes with game-specific value logic
│   ├── deck.py     # Deck management with multi-deck support
│   └── player.py   # Player state and game actions
├── games/          # Game implementations
│   ├── blackjack.py # Blackjack game engine
│   └── war.py      # War game implementation
└── __init__.py     # Package initialization

tests/              # Test suite
├── core/           # Core component tests
└── games/          # Game logic tests
```

## 🛠️ Technical Requirements

- **Python**: 3.13 or higher
- **Testing**: pytest framework (optional)
- **Dependencies**: None (pure Python standard library)

## 📦 Installation & Setup

### Prerequisites

```bash
# Ensure Python 3.13+ is installed
python --version
```

### Clone & Install

```bash
# Clone the repository
git clone https://github.com/kay-rey/DeckPy.git
cd DeckPy

# Install testing dependencies (optional)
pip install -r requirements-test.txt
```

## 🎮 Usage

### Quick Start

```bash
# Run the main game interface
python main.py
```

### Game Selection

The application provides a command-line interface:

1. **Blackjack**: Casino-style card game with betting
2. **War**: Classic two-player card game
3. **Exit**: Program termination

### Game Features

#### Blackjack

- **Betting System**: Money management with win/loss tracking
- **Player Actions**: Hit, Stand, Double Down, Split
- **Dealer Logic**: Standard casino dealer behavior
- **Multi-Hand Support**: Handle split hands independently
- **Deck Management**: Automatic reshuffling

#### War

- **Complete Rules**: Full implementation including "War" scenarios
- **State Management**: Hand depletion and replenishment handling
- **Betting Integration**: Integrated with the betting system

## 🧪 Testing & Quality

### Run Test Suite

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/core/test_card.py
pytest tests/games/test_blackjack.py
```

### Test Coverage

- **Core Components**: Tests for card, deck, and player logic
- **Game Logic**: Testing of game rules and scenarios
- **Integration**: Game flow testing

## 🔧 Development Practices

### Code Quality Standards

- **Type Safety**: Type annotation throughout codebase
- **Documentation**: Docstrings and inline comments
- **Error Handling**: Input validation and error checking
- **Structure**: Clean, organized code layout

### Design Patterns

- **Card Factory**: Dynamic card creation based on game type
- **Strategy Pattern**: Game-specific card value calculations
- **State Management**: Game state handling and updates

## 📊 Project Characteristics

- **Memory Efficient**: Proper cleanup and resource management
- **Execution**: Smooth gameplay with optimized logic
- **Extensible**: Modular design allows adding new games
- **Maintainable**: Clean code structure for easy updates

## 🚀 Future Enhancements

### Potential Features

- **Additional Games**: Poker, Solitaire, Hearts
- **Network Play**: Multiplayer capabilities
- **AI Opponents**: Computer player improvements
- **Web Interface**: Modern UI options
- **Statistics**: Player tracking and leaderboards

### Architecture Improvements

- **Plugin System**: Dynamic game loading
- **Event System**: Decoupled state management
- **Configuration**: External game rule settings
- **Logging**: Enhanced debugging capabilities

## 🤝 Contributing

We welcome contributions that maintain the project's code quality and architectural standards.

### Contribution Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/Improvement`)
3. **Implement** with attention to code quality and testing
4. **Test** thoroughly with the existing test suite
5. **Submit** a pull request with detailed description

### Development Standards

- **Test Coverage**: Maintain existing test coverage
- **Code Style**: Follow PEP 8 and project conventions
- **Documentation**: Update docstrings and README as needed
- **Quality**: Consider performance and maintainability

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**kay-rey** - Python Developer

- **GitHub**: [@kay-rey](https://github.com/kay-rey)
- **Focus**: Clean code, game development, Python architecture

## 🌟 Project Highlights

### **Technical Strengths**

- **Clean Architecture**: Well-structured, maintainable codebase
- **Modular Design**: Easy to extend with new games and features
- **Quality Focus**: Comprehensive testing and error handling
- **Performance**: Efficient algorithms and data structures

### **Code Quality**

- **Zero Dependencies**: Pure Python standard library implementation
- **Type Safety**: Full type annotation support
- **Documentation**: Clear docstrings and code comments
- **Testing**: Robust test suite for all components

---

⭐ **Star this repository** if you appreciate clean, well-structured Python development with DeckPy!

_Last updated: 2025-04-05 | Built with ❤️ and Python 3.13_
