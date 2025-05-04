import sys
from hand import * 
from shoe import *  
from player import * 


def safe_input(prompt):
    user_input = input(prompt).strip().lower()
    if user_input in ["quit", "exit"]:
        print("Exiting Game, Goodbye!")
        sys.exit()
    return user_input

class BlackjackGame:
    def __init__(self, num_decks, game_burn_percentage, initial_balance=10000):
        self.shoe = Shoe(num_decks, game_burn_percentage)
        self.player = Player(initial_balance=initial_balance)
        self.player_hands = []
        self.dealer_hand = Hand(is_player_hand=False) 
        self.split_hand_index = 0  #For properly assining hand numbers for split hands
        self.bet_amount = 0
        self.game_loop()

    def deal_initial_cards(self):
        self.player_hands = [Hand(is_player_hand=True, player_bet=self.bet_amount, player_balance=self.player.balance)]
        self.dealer_hand = Hand(is_player_hand=False)
        for hand in self.player_hands:
            hand.add_card(self.shoe.deal())
            hand.add_card(self.shoe.deal())
        self.dealer_hand.add_card(self.shoe.deal())
        self.dealer_hand.add_card(self.shoe.deal())
        
        print(f"\nDealer's card: {self.dealer_hand.cards[0]} Value: {self.dealer_hand.cards[0].value}")
        print(f"Dealer's card: [Hidden]")
        insurance_placed = False
        if self.dealer_hand.cards[0].face == "A":  # Check for isnsurance
            print(f"\nRunning Count:{self.shoe.update_running_count()}        True Count:{self.shoe.update_true_count()}\n")
            for hand in self.player_hands:
                 print(hand)
            while True:
                take_insurance = safe_input("Take insurance? [y] [n]\n").strip().lower()
                if take_insurance == "y" or take_insurance == "yes":
                    if self.player.balance >= self.bet_amount:
                        self.player.place_bet(self.bet_amount)
                        insurance_placed = True
                        break
                    else:
                        print("Not enough funds for insurance bet")
                        break
                elif take_insurance == "n" or take_insurance == "no":
                    break
                else: 
                    print("Please enter a valid action [y]  [n])")

        if self.check_blackjack(self.dealer_hand):
            if insurance_placed:
                print(f"Insurance bet Wins +${self.bet_amount * 2}")
                self.player.win_bet(self.bet_amount, 3)
            self.dealer_blackjack()
        else:
            if self.dealer_hand.cards[0].face == "A" and not insurance_placed:
                print("No Dealer Blackjack")
            if insurance_placed:
                print(f"No Dealer Blackjack -${self.bet_amount}")
            all_player_blackjacks = [self.check_blackjack(hand) for hand in self.player_hands]
            if any(all_player_blackjacks):
                self.player_blackjack()

    def check_blackjack(self, hand):
        return hand.get_hand_value() == 21 and (len(hand.cards) == 2 and hand.has_split is False)

    def dealer_blackjack(self):
        print(f"Dealer {self.dealer_hand}")
        print(f"Player {', '.join(str(hand) for hand in self.player_hands)}")
        print("Dealer has Blackjack!")
        for hand in self.player_hands:
            if self.check_blackjack(hand):
                print("Push: Player also has Blackjack")
                self.player.win_bet(self.bet_amount, 1)  # Return the bet amount
            else:
                print(f"Player loses -${self.bet_amount}")
        print(f"\n{'*' * 100}")
    def player_blackjack(self):
        print(f"Dealer {self.dealer_hand}")
        print(f"Player {', '.join(str(hand) for hand in self.player_hands)}")
        print("Player has Blackjack!")
        for hand in self.player_hands:
            if self.check_blackjack(hand):
                print(f"Player Wins +${self.bet_amount * 1.5}")
                self.player.win_bet(self.bet_amount, 2.5)  # 1.5x winnings for Blackjack
        print(f"\n{'*' * 100}")
    def player_turn(self):
        for hand in self.player_hands:
            if not self.check_blackjack(hand):  # Skip player turn if they have Blackjack
                print(f"\nRunning Count: {self.shoe.update_running_count()} \t True Count:{self.shoe.update_true_count()}\n")
                while True:
                    hand.update_split_ability()
                    available_actions = ["hit [h]", "stand [s]"]

                    if hand.can_double():  
                        available_actions.append("double [d]")
                    if hand.can_split:  
                        available_actions.append("split [p]")
                
                    action = safe_input(f"{hand}\n{'  '.join(available_actions)}: ").strip().lower() 
                    if action == 'hit' or action == 'h':
                        hand.add_card(self.shoe.deal())
                        hand.get_hand_value()
                        if hand.get_hand_value() > 21:
                            print(hand)
                            print("Hand busts!")
                            break
                    elif action == 'stand' or action == 's':
                        self.split_hand_index -= 1
                        break
                    elif action == 'double' or action == 'd':
                        if hand.can_double():
                            self.split_hand_index -= 1
                            hand.double_down()
                            hand.has_doubled = True
                            hand.add_card(self.shoe.deal())
                            Player.place_bet(self.player, self.bet_amount)
                            print(hand)
                            hand.get_hand_value()
                            if hand.get_hand_value() > 21:
                                print("Hand busts!")
                            break
                        else:
                            print("Cannot double down")
                    elif action == 'split' or action == 'p':
                        if hand.can_split:
                            self.split_hand_index += 1
                            new_hand = hand.split_hand(self.split_hand_index)
                            new_hand.add_card(self.shoe.deal())
                            hand.add_card(self.shoe.deal())
                            self.player_hands.append(new_hand)
                            Player.place_bet(self.player, self.bet_amount)
                            print(f"\nHand is now Split!: {hand} {new_hand} \n")
                        else:
                            print("Cannot split")
                    else:
                        print("Invalid action")

    def dealer_turn(self):
        print(f"\nDealer's card: {self.dealer_hand.cards[0]}")
        print(f"Dealer's card: {self.dealer_hand.cards[1]}")
        if self.dealer_hand.get_hand_value() == 17 and self.dealer_hand.soft_seventeen():
            self.dealer_hand.add_card(self.shoe.deal())
            print(f"Dealer Draws: {self.dealer_hand}")
            self.dealer_hand.get_hand_value()
        while self.dealer_hand.get_hand_value() < 17:
            self.dealer_hand.add_card(self.shoe.deal())
            print(f"Dealer Draws: {self.dealer_hand}")
            if self.dealer_hand.get_hand_value() > 21:
                print("Dealer busts!")
                break

    def determine_winner(self):
        dealer_value = self.dealer_hand.get_hand_value()
        results = [] # Stores Printed Result
        for i, hand in enumerate(self.player_hands):
            player_value = hand.get_hand_value()
            if player_value > 21:
                if hand.has_doubled is True:
                    result = f"Hand {i + 1} busted -${self.bet_amount * 2}"
                else:
                    result = f"Hand {i + 1} busted -${self.bet_amount}"
            elif dealer_value > 21 or player_value > dealer_value:
                if hand.has_doubled is True:
                    result = f"Hand {i + 1} wins +${self.bet_amount * 2}"
                else:
                    result = f"Hand {i + 1} wins +${self.bet_amount}"
                self.player.win_bet(self.bet_amount, 2)  # Double the bet amount if the player wins
                if hand.has_doubled is True:
                    self.player.win_bet(self.bet_amount, 2)
            elif player_value < dealer_value:
                if hand.has_doubled is True:
                    result = f"Hand {i + 1} loses -${self.bet_amount * 2}"
                else:
                    result = f"Hand {i + 1} loses -${self.bet_amount}"
            else:
                result = f"Hand {i + 1} is a push"
                self.player.win_bet(self.bet_amount, 1)  # Return the bet amount if it's a tie
                if hand.has_doubled is True:
                    self.player.win_bet(self.bet_amount, 1)
            results.append(result)
            self.split_hand_index = 0
        return results

    def game_loop(self):
        while True:
            print(f"\nCurrent balance: ${self.player.balance} \nRunning Count:{self.shoe.update_running_count()}    True Count:{self.shoe.update_true_count()}")
            while True:
                try:
                    user_input = safe_input("Place your bet: ")

                    self.bet_amount = int(user_input)  
                    if self.bet_amount <= 0:
                        print("Bet must be a positive number.")
                        continue 

                    break  
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            try:
                self.player.place_bet(self.bet_amount)
                self.deal_initial_cards()
                if not self.check_blackjack(self.dealer_hand) and all(not self.check_blackjack(hand) for hand in self.player_hands):
                    self.shoe.remove_hidden_count()  # for card counting
                    self.player_turn()
                    if any(hand.get_hand_value() <= 21 for hand in self.player_hands):  # Dealer only has a turn if player has not busted all hands
                        self.dealer_turn()
                    else:
                        print(f"Dealer Had: {self.dealer_hand.cards[0]} {self.dealer_hand.cards[1]}") 
                    results = self.determine_winner()
                    for result in results:
                        print(result)
                    print(f"\n{'*' * 100}")
                    self.shoe.count_hidden_card()  # Add hidden card to burned cards
                    if self.shoe.percentage_burned() > self.shoe.burn_percentage:
                        self.shoe.shoe_cards.clear()
                        self.shoe.burned_cards.clear()
                        self.shoe.create_shoe()
                        print("Deck shuffled!")
                    while self.player.balance == 0:
                        try:
                            added_balance = safe_input("Funds missing, please add funds: $")
                            added_balance = int(added_balance)
                            if added_balance <= 0:
                                print("Enter a valid number")
                                continue
                            self.player.balance += added_balance
                        except ValueError:
                            print("Please imput a valid number.")

            except ValueError as e:
                print(e)
