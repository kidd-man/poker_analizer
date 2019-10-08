class PokerError(Exception):
    """Poker error; """
    def __init__(self, message):
        self.message = message


class HandError(Exception):
    """Hand error"""
    def __init__(self, message):
        self.message = message


class DeckError(Exception):
    """Exception raised for errors in game.py:"""
    def __init__(self, message):
        self.message = message

