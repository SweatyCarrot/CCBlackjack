import random

class InvalidInput(Exception):
    pass

class GameState():
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A"]
    players = []

    def __init__(self, pot = 0):
        self.pot = pot
    
    def initial_wallet(self):
        while True:
            try:
                wallet = int(input("What would you like your wallet to be? (Must be lower than $1000): $"))
                if wallet > 0 and wallet < 1000:
                    return wallet
                else:
                    raise InvalidInput
            except InvalidInput:
                print("Invalid Input")
            except:
                print("Invalid Input")
                
    def deal(self):
        for object in GameState.players:
            for i in range(2):
                object.update_hand([random.choice(GameState.deck)])
        print("Cards have been dealt!")

class Player():

    def __init__(self, wallet):
        self.wallet = wallet
        self.hand = []
        self.bet = 0
        self.stand = False
        self.bust = False
        self.out = False
        GameState.players.append(self)

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
        #SORT THIS LIST
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
                if bet_amount <= self.get_wallet() and bet_amount > 0:
                    self.update_bet(bet_amount)
                    self.update_wallet(bet_amount, False)
                    break
                else:
                    raise InvalidInput
            except InvalidInput:
                print("Invalid input.")
                continue

    def hit(self):
        self.update_hand([random.choice(GameState.deck)])
        print("Your hand is now: " + str(self.get_hand()) + ". Hand value: " + str(self.get_hand_value()))

    
    def stay(self):
        print("You stand on " + str(self.get_hand_value()) + ".")
        self.stand = True
    
    def turn_logic(self):
        if self.get_hand_value == 21:
                print("Your hand is " + str(self.get_hand()))
                print("Blackjack!")
        else:
            print("Your current hand is " + str(self.get_hand()) + "\nWould you like to Hit or Stand?")
            while self.get_hand_value() <= 21 and self.bust == False and self.stand == False:
                if self.get_hand_value() == 21:
                    print("Your hand is " + str(self.get_hand()))
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
    risk = 0.25

    def __init__(self):
        self.hand = []
        self.bust = False
        GameState.players.append(self)
    
    def get_hand_half(self):
        return self.hand[1:]

    def get_hand_full(self):
        return self.hand

    def update_hand(self, cards):
        for card in cards:
            self.hand.append(card)

    def hit(self):
        self.update_hand([random.choice(GameState.deck)])
        print("Dealer's hand is now: " + str(self.get_hand()))

    def stay(self):
        print("Dealer stands on " + str(self.get_hand_value()) + ".")
    
    def turn_logic(self):
        pass


def main():
    gamestate = GameState()

    player_wallet = gamestate.initial_wallet()

    player = Player(player_wallet)
    dealer = Dealer()

    while player.out == False:
        player.take_bet()
        gamestate.deal()
        print("The dealer is showing [?]" + str(dealer.get_hand_half()))
        player.turn_logic()
        ##DEALER TURN LOGIC HERE
        ##REVEAL HANDS
        ##CHECK WINNER
        ##DISTRIBUTE POT, CLEAR HANDS
        
main()