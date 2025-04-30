import random
from card import * 

class Shoe:
    def __init__(self, num_decks, burn_percentage):
        self.all_cards = num_decks * 52
        self.decks = num_decks
        self.burned_cards = []
        self.shoe_cards = []
        self.dealer_hidden_card = []
        self.burn_percentage = burn_percentage
        self.create_shoe()
        self.running_count = 0
        self.true_count = 0

    def create_shoe(self):
        self.shoe_cards = [Card(s, v) for _ in range(self.decks) for s in Card.suits for v in Card.values]
        self.shuffle_shoe()

    def shuffle_shoe(self):
        random.shuffle(self.shoe_cards)

    def deal(self):
        if len(self.shoe_cards) > 0:    
            card = self.shoe_cards.pop()
            self.burned_cards.append(card)
        else:
            print("Shoe ran out of cards! Adding burned cards to shoe")
            random.shuffle(self.burned_cards)
            self.shoe_cards.extend(self.burned_cards)
            self.burned_cards.clear()
            
            card = self.shoe_cards.pop()
            self.burned_cards.append(card)
        return card

    def percentage_burned(self):
        return len(self.burned_cards) / self.all_cards

    def update_running_count(self):
        running = self.running_count
        for card in self.burned_cards:
            if card.value < 7:
                running += 1
            if card.value > 9:
                running -= 1
        return running

    def update_true_count(self):
        rounded_cards = max(round((len(self.shoe_cards) / 52)), 1)
        true_count= round(self.update_running_count() / rounded_cards)
        return true_count


    def remove_hidden_count(self):
        hidden_card = self.burned_cards.pop()
        self.dealer_hidden_card.append(hidden_card)

    def count_hidden_card(self):
        hidden_card = self.dealer_hidden_card.pop()
        self.burned_cards.append(hidden_card)
