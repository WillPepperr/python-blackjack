from blackjack_game import * 
from card import *  
from config import * 


def display_startup_message():
    print(
        "\n" + "*" * 50 + "\n"
        "♦ ♠ ♥ ♣ WELCOME TO BLACKJACK!♣ ♥ ♠ ♦\n"
        "Basic Rules:\n"
        "- Try to get as close to 21 without going over\n"
        "- Dealer must hit on soft 17\n"
        "- Blackjack (A + 10/J/Q/K) pays 3:2\n"
        "- Dealer Peaks for BlackJack if holding (A or 10/J/Q/K)\n"
        "- Insurance is offered if the dealer shows an Ace and Pays out 2:1\n"
        "- You can hit, stand, double down, or split (if applicable)\n"
        "- Running out of money? Borrow from a friend! (you can add funds once you reach 0)\n\n"
        "Controls:\n"
        "- 'h' or 'hit' → Hit\n"
        "* Hitting adds one card to your hand\n\n"
        "- 's' or 'stand' → Stand\n"
        "* Standing ends your turn for your hand\n\n"
        "- 'd' or 'double' → Double Down (if allowed)\n"
        "* If you have not hit yet in the hand, you may double your bet (if you have the funds), add a card to your hand, and end the turn for your hand\n\n"
        "- 'p' or 'split' → Split (if allowed)\n"
        "* Split one hand into 2 hands if your hand has 2 cards of the same value (this includs any combination of 10/J/Q/K), a new card is added to each card to make 2 new playable hands\n\n"
        "- 'y' or 'yes' → accept insurance (if offered) \n"
        "- 'n' or 'no' → decline insurance (if offered) \n\n"
        "- 'quit' or 'exit' → Quit the game\n"
        + "*" * 75 + "\n"
    )

if __name__ == "__main__":
    display_startup_message()
    game = BlackjackGame(num_decks=8, game_burn_percentage=.80, initial_balance=1000)
