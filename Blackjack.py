import random

class InvalidInput(Exception):
    pass

class GameState():
    deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "A"]

    def __init__(self, pot = 0):
        self.pot = pot


class Player():

    def __init__(self, wallet):
        self.wallet = wallet
        self.hand = []
        self.bet = 0
        self.stand = False
        self.bust = False
        self.out = False
  
    def get_wallet(self):
        return self.wallet

    def update_wallet(self, value, increase = True):
        if increase == True:
            self.wallet += value
        else:
            self.wallet -= value

    def get_hand(self):
        return self.hand

    def update_hand(self, cards):
        for card in cards:
            self.hand.append(card)

    def get_bet(self):
        return self.bet

    def update_bet(self, value):
        self.bet += value
    
    def get_hand_value(self):
        hand_value = 0
        for card in self.get_hand():
            if card == "A":
                if hand_value + 11 > 21:
                    hand_value += 1
                else:
                    hand_value += 11
            else:
                hand_value += card
        return hand_value

    def take_bet(self):
        print("Your current wallet is " + str(self.get_wallet()) + ".")
        while True:
            try:
                bet_amount = input("Please enter your bet: ")
                bet_amount = int(bet_amount)
                if bet_amount <= self.get_wallet():
                    self.update_bet(bet_amount)
                    self.update_wallet(bet_amount, False)
                    break
                else:
                    raise InvalidInput
            except:
                print("Invalid input.")
                continue

    def hit(self):
        self.update_hand([random.choice(gamestate.deck)])
        print("Your hand is now: " + str(self.get_hand()))
    
    def stay(self):
        print("You stand on " + str(self.get_hand_value()) + ".")
        self.stand = True
    
    def turn_logic(self):
        #CHECK FOR BLACKJACK BEFORE STARTING
        print("Your current hand is " + str(self.get_hand()) + "\n Would you like to Hit or Stand?")
        while self.get_hand_value() <= 21 and self.bust == False and self.stand == False:
            if self.get_hand_value() == 21:
                print("Blackjack!")
                self.stay()
            else:
                action = input("Hit or Stand: ").lower()
                if action == "hit":
                    self.hit()
                    if self.get_hand_value() < 21:
                        continue
                    else:
                        print("You bust!")
                        self.bust = True
                elif action == "stand":
                    self.stay()
                else:
                    print("Invalid Input")

class Dealer():

    def __init__(self):
        self.hand = []
        self.bust = False
    
    def get_hand_half(self):
        return self.hand[1:]

    def get_hand_full(self):
        return self.hand

    def update_hand(self, cards):
        for card in cards:
            self.hand.append(card)

    def hit(self):
        self.update_hand([random.choice(gamestate.deck)])
        print("Dealer's hand is now: " + str(self.get_hand()))

    def stay(self):
        print("Dealer stands on " + str(self.get_hand_value()) + ".")



gamestate = GameState()

player = Player(100)

player.take_bet()
player.turn_logic()