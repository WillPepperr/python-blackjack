class Player:
    def __init__(self, initial_balance):
        self.balance = initial_balance

    def place_bet(self, bet_amount):
        bet_amount = int(bet_amount)
        if bet_amount > self.balance or bet_amount < 1:
            raise ValueError("Insufficient funds for this bet")
        self.balance -= bet_amount
        return bet_amount

    def win_bet(self, bet_amount, win_multiplier):
        self.balance += bet_amount * win_multiplier
