"""
CardGames - A collection of card games implemented in Python
Created by kay-rey
"""

from datetime import datetime

# Package metadata
__version__ = '0.9.0'
__author__ = 'kay-rey'
__last_updated__ = '2025-04-09'

from .core import Card, Deck, Player
from .games import Blackjack, War

__all__ = [
    'Card',
    'Deck',
    'Player',
    'Blackjack',
    'War'
]


def get_package_info():
    return {
        'version': __version__,
        'author': __author__,
        'last_updated': __last_updated__,
        'current_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }
