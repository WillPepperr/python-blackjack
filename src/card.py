class Card:
    values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
        '7': 7, '8': 8, '9': 9, 
        '10': 10, 'J': 10, 'Q': 10, 'K': 10, 
        'A': 11
    }
    suits = ['♥', '♦', '♣', '♠'] 

    def __init__(self, suit, value):
        self.suit = suit
        self.face = value
        self.value = Card.values[value]

    def __repr__(self):
        return f"{self.face}{self.suit}"
