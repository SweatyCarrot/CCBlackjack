import random

class GameState():
    deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "A"]
    def __init__(self, pot = 0):
        self.pot = pot

class Player():
    def __init__(self, wallet):
        self.wallet = wallet
        self.hand = []
        self.bet = 0
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
        for card in self.hand:
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
                bet_amount = int(input("Please enter your bet: "))
                if bet_amount <= self.get_wallet():
                    self.update_bet(bet_amount)
                    self.update_wallet(bet_amount, False)
                    break
                else:
                    raise TypeError
            except TypeError:
                print("Invalid input.")
                continue

  
player = Player(100)

player.take_bet()