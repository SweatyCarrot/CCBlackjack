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

    def collect_bets(self):
        for p in GameState.players:
            self.pot += p.get_bet()
                
    def deal(self):
        for object in GameState.players:
            for i in range(2):
                object.update_hand([random.choice(GameState.deck)])
        print("Cards have been dealt!")
    
    def reveal(self):
        print("Let's reveal!")
        for player in GameState.players:
            print(player.name + " has " + str(player.get_hand()) + " with a value of " + str(player.get_hand_value()))
    
    def calculate_winner(self):
        winner = ""
        score = 0
        for p in GameState.players:
            if p.bust == False and p.get_hand_value() > score:
                score = p.get_hand_value()
                winner = p
        if winner == "":
            print("No winner! Returning bets!")
            for p in GameState.players:
                p.wallet += p.bet
        else:
            print(self.pot)
            if len(GameState.players) == 2:
                self.pot += self.pot
            print(winner.name + " has won the round! They win " + str(self.pot))
            winner.wallet += self.pot

    def clear_hands(self):
        self.pot = 0
        for p in GameState.players:
            p.bet = 0
            p.hand = []
            p.stand = False
            p.bust = False
    
    def check_outs(self):
        for p in GameState.players:
            if p.get_wallet() <= 0:
                p.out = True


class Player():

    def __init__(self, wallet):
        self.name = "Player1"
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

    def update_hand(self, cards):
        for card in cards:
            self.hand.append(card)
    
    def clear_hand(self):
        self.hand = []
        self.stand = False
        self.bust = False

    def get_bet(self):
        return self.bet

    def update_bet(self, value):
        self.bet += value
    
    def get_hand(self):
        return self.hand

    
    def get_hand_value(self):
        replaced_hand = [11 if card == 'A' else card for card in self.get_hand()]
        while sum(replaced_hand) > 21 and 11 in replaced_hand:
            replaced_hand.append(1)
            replaced_hand.remove(11)
        return sum(replaced_hand)


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
            except KeyboardInterrupt:
                print("Keyboard Interrupt")
                exit()
            except:
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
            print("Your current hand is " + str(self.get_hand()) + ". Hand value: " + str(self.get_hand_value()) + "\nWould you like to Hit or Stand?")
            while self.get_hand_value() <= 21 and self.bust == False and self.stand == False:
                if self.get_hand_value() == 21:
                    print("Blackjack!")
                    self.stay()
                else:
                    action = input("Hit or Stand: ").lower()
                    if action == "hit":
                        self.hit()
                        if self.get_hand_value() <= 21:
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
        self.name = "Dealer"
        self.wallet = 0
        self.hand = []
        self.bust = False
        self.stand = False
        GameState.players.append(self)
    
    def get_hand_half(self):
        return self.hand[1:]

    def get_hand(self):
        return self.hand

    def get_bet(self):
        return 0
    
    def get_wallet(self):
        return 1
    
    def get_hand_value(self):
        replaced_hand = [11 if card == 'A' else card for card in self.get_hand()]
        while sum(replaced_hand) > 21 and 11 in replaced_hand:
            replaced_hand.append(1)
            replaced_hand.remove(11)
        return sum(replaced_hand)
    
    def get_hand_half_value(self):
        replaced_hand = [11 if card == 'A' else card for card in self.get_hand_half()]
        while sum(replaced_hand) > 21 and 11 in replaced_hand:
            replaced_hand.append(1)
            replaced_hand.remove(11)
        return sum(replaced_hand)

    def update_hand(self, cards):
        for card in cards:
            self.hand.append(card)

    def hit(self):
        self.update_hand([random.choice(GameState.deck)])
        print("Dealer's hand is now: " + "[?]" + str(self.get_hand_half()))

    def stay(self):
        print("Dealer stands on " + str(self.get_hand_value()) + ".")
        self.stand = True
    
    def turn_logic(self):
        while self.get_hand_half_value() < 17:
            self.hit()
        if self.get_hand_half_value() <= 21:
            self.stay()
        else:
            print("Dealer busts!")
            self.bust = True

#    def check_bust(self):
#        if self.get_hand_value() > 21:
#            print("Dealer busts!")
#            self.bust = True


def main():
    gamestate = GameState()

    player_wallet = gamestate.initial_wallet()

    player = Player(player_wallet)
    dealer = Dealer()

    while player.out == False:
        player.take_bet()
        gamestate.collect_bets()
        gamestate.deal()
        print("The dealer is showing [?]" + str(dealer.get_hand_half()))
        player.get_hand_value()
        player.turn_logic()
        dealer.turn_logic()
        gamestate.reveal()
        gamestate.calculate_winner()
        ##DISTRIBUTE POT, CLEAR HANDS
        gamestate.clear_hands()
        gamestate.check_outs()
        #make clear_hand a GameState method
main()