
def nerd_font_check():
    import config  # Import here to modify the actual module
    if config.nerd_font is None:
        answer = input("Are you using Nerd font? Changes how card suits are displayed (y/N) ").strip().lower()
        config.nerd_font = answer in ['y', 'yes', 'yeah']

def get_suits():
    import config
    return ['❤️', '♦', '♣', '♠'] if config.nerd_font else ['♥', '♦', '♣', '♠']

class Card:
    values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
        '7': 7, '8': 8, '9': 9, 
        '10': 10, 'J': 10, 'Q': 10, 'K': 10, 
        'A': 11
    }
    suits = [] 

    def __init__(self, suit, value):
        self.suit = suit
        self.face = value
        self.value = Card.values[value]

    def __repr__(self):
        return f"{self.face}{self.suit}"
