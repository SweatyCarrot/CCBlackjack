import gamestate
import person
import player_actions
import random
from time import sleep

#Player Class - Inherits from Person
class Player(person.Person):

    def __init__(self, name, wallet):
        person.Person.__init__(self, name)
        self.wallet = wallet
        self.bet = 0
        self.out = False
        gamestate.GameState.players.append(self)

    def get_wallet(self):
        return self.wallet

    def update_wallet(self, value, increase = True):
        if increase == True:
            self.wallet += value
        else:
            self.wallet -= value

    def get_bet(self):
        return self.bet

    def update_bet(self, value):
        self.bet += value

    def take_bet(self):
        print(f"Your current wallet is ${self.get_wallet()}.")
        while True:
                bet_amount = input("Please enter your bet: $")
                if bet_amount.isnumeric():
                    bet_amount = int(bet_amount)
                    if bet_amount <= self.get_wallet() and bet_amount > 0:
                        self.update_bet(bet_amount)
                        self.update_wallet(bet_amount, False)
                        break
                    else:
                        print("Bet amount must be greater than 0 and no greater than your total wallet.")
                else:
                    print("Please enter a whole number.")

    def hit(self):
        sleep(0.5)
        self.update_hand([random.choice(gamestate.GameState.deck)])
        print(f"Your hand is now: {self.get_hand()}. Hand value: {self.get_hand_value()}")
        sleep(0.5)

    def stay(self):
        sleep(0.5)
        print(f"You stand on {self.get_hand_value()}.")
        self.stand = True
        sleep(0.5)
    
    def turn_logic(self):
        if self.get_hand_value == 21:
                print(f"Your hand is {self.get_hand()}.")
                print("Blackjack!")
                sleep(0.5)
        else:
            newline = '\n'
            sleep(0.5)
            print(f"Your current hand is {self.get_hand()}. Hand value: {self.get_hand_value()} {newline}Would you like to Hit or Stand?")
            while self.get_hand_value() <= 21 and self.bust == False and self.stand == False:
                if self.get_hand_value() == 21:
                    print("Blackjack!")
                    sleep(0.5)
                    self.stay()
                else:
                    action = input("Hit or Stand: ").upper()
                    if action == player_actions.Player_Actions(0).name:
                        self.hit()
                        if self.get_hand_value() <= 21:
                            continue
                        else:
                            print("You bust!")
                            self.bust = True
                    elif action == player_actions.Player_Actions(1).name:
                        self.stay()
                    else:
                        print("Invalid Input. Please choose Hit or Stand")