from blackjack_game import BlackjackGame

def display_startup_message():
    print("\n" + "*" * 50)
    print("♦ ♠ ❤️♣ WELCOME TO BLACKJACK!♣ ❤️♠ ♦ ")
    print("Basic Rules:")
    print("- Try to get as close to 21 without going over")
    print("- Dealer must hit on soft 17")
    print("- Blackjack (A + 10/J/Q/K) pays 3:2")
    print("- Dealer Peaks for BlackJack if holding (A or 10/J/Q/K)")
    print("- Insurance is offered if the dealer shows an Ace and Pays out 2:1")
    print("- You can hit, stand, double down, or split (if applicable)")
    print("- Running out of money? Borrow from a friend! (you can add funds once you reach 0)")
    
    print("\nControls:")
    print("- 'h' or 'hit' → Hit")
    print(f"* Hitting adds one card to your hand\n")

    print("- 's' or 'stand' → Stand")
    print(f"* Standing ends your turn for your hand\n")

    print("- 'd' or 'double' → Double Down (if allowed)")
    print(f"* If you have not hit yet in the hand, you may double your bet (if you have the funds), add a card to your hand, and end the turn for your hand\n")
    
    print("- 'p' or 'split' → Split (if allowed)")
    print(f"* Split one hand into 2 hands if your hand has 2 cards of the same value (this includs any combination of 10/J/Q/K), a new card is added to each card to make 2 new playable hands\n")

    print("- 'y' or 'yes' → accept insurance (if offered) ")
    print("- 'n' or 'no' → decline insurance (if offered) ")


    print("")
    print("- 'quit' or 'exit' → Quit the game")
    print("*" * 75 + "\n")


if __name__ == "__main__":
    display_startup_message()
    game = BlackjackGame(num_decks=8, game_burn_percentage=.80, initial_balance=1000)
