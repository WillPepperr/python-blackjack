from card import * 

class Hand:
    def __init__(self, is_player_hand=True, hand_number=1, player_bet=0, player_balance=0):
        self.cards = []
        self.is_player_hand = is_player_hand
        self.can_split = False
        self.hand_number = hand_number
        self.num_aces = sum(1 for card in self.cards if card.face == 'A')
        self.has_doubled = False
        self.has_split = False # for flagging hand after splitting to deny an unwarrented Blackjack
        self.player_bet = player_bet
        self.player_balance = player_balance

    def add_card(self, card):
        self.cards.append(card)

    def get_hand_value(self):
        value = sum(card.value for card in self.cards)
        self.num_aces = sum(1 for card in self.cards if card.face == 'A')
        ace_with_value_eleven = self.num_aces
        while value > 21 and ace_with_value_eleven > 0:
            value -= 10
            ace_with_value_eleven -= 1
        return value

    def soft_seventeen(self):
        value = self.get_hand_value()
        if value == 17 and self.num_aces > 0:
            soft_seventeen_check = sum(card.value for card in self.cards if card.face != 'A')
            if soft_seventeen_check < 7:
                return True
        return False

    def update_split_ability(self):
        if len(self.cards) == 2 and (self.cards[0].value == self.cards[1].value and self.player_bet <= self.player_balance):
            self.can_split = True
        else:
            self.can_split = False

    def can_double(self):
        return len(self.cards) == 2 and self.player_bet <= self.player_balance

    def split_hand(self, split_hands):
        if not self.can_split:
            raise ValueError("Cannot split this hand")

        next_hand = Hand(is_player_hand=self.is_player_hand, hand_number=self.hand_number + split_hands)
        next_hand.add_card(self.cards.pop())
        next_hand.has_split = True
        self.has_split = True
        return next_hand

    def double_down(self):
        if not self.can_double():
            raise ValueError("Cannot double")
        self.has_doubled = True

    def __repr__(self):
        if self.is_player_hand:    
            hand_label = f"Player Hand {self.hand_number}: " if self.hand_number != 1 else "Player Hand:"
        else:
            hand_label = f""
        cards_str = " ".join(str(card) for card in self.cards)  
        return f"{hand_label} {cards_str} Value: {self.get_hand_value()}"
