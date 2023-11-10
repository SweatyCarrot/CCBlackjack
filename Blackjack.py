#Actions Enum Branch
import random

#Experimental Exception
class InvalidInput(Exception):
    pass

#GameState Class
class GameState():
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A"]
    #All players including the dealer
    players_all = []
    #All players NOT including the dealer
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
                
    def deal(self, dealer):
        for object in GameState.players_all:
            for i in range(2):
                object.update_hand([random.choice(GameState.deck)])
        print("Cards have been dealt!")
        print("The dealer is showing [?]" + str(dealer.get_hand_half()))
    
    def reveal(self):
        print("Results!")
        for player in GameState.players_all:
            print(player.name + " has " + str(player.get_hand()) + " with a value of " + str(player.get_hand_value()))
    
    def calculate_winner(self):
        score_list = []
        for p in GameState.players_all:
            score_list.append(p.get_hand_value())
        if sum(score_list)/ len(score_list) == score_list[0]:
            print("No winner! Returning bets!")
            for p in GameState.players:
                p.wallet += p.bet
        else:
            winner = ""
            score = 0
            for p in GameState.players_all:
                if p.bust == False and p.get_hand_value() > score:
                    score = p.get_hand_value()
                    winner = p
            if winner == "":
                print("No winner! Returning bets!")
                for p in GameState.players:
                    p.wallet += p.bet
            else:
                print(self.pot)
                if len(GameState.players) == 1:
                    self.pot += self.pot
                print(winner.name + " has won the round! They win " + str(self.pot))
                try:
                    winner.wallet += self.pot
                except AttributeError:
                    pass

    def clear_hands(self):
        self.pot = 0
        for p in GameState.players_all:
            p.bet = 0
            p.hand = []
            p.stand = False
            p.bust = False
    
    def check_outs(self):
        for p in GameState.players:
            if p.get_wallet() <= 0:
                p.out = True

#Person Class
class Person():
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bust = False
        self.stand = False
        GameState.players_all.append(self)

    def get_hand(self):
        return self.hand
    
    def update_hand(self, cards):
        for card in cards:
            self.hand.append(card)
    
    def get_hand_value(self):
        replaced_hand = [11 if card == 'A' else card for card in self.get_hand()]
        while sum(replaced_hand) > 21 and 11 in replaced_hand:
            replaced_hand.append(1)
            replaced_hand.remove(11)
        return sum(replaced_hand)
    
#Player Class - Inherits from Person
class Player(Person):

    def __init__(self, name, wallet):
        Person.__init__(self, name)
        self.wallet = wallet
        self.bet = 0
        self.out = False
        GameState.players.append(self)

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

#Dealer Class - Inherits from Person
class Dealer(Person):

    def __init__(self):
        Person.__init__(self, "Dealer")
        self.hand = []
    
    def get_hand_half(self):
        return self.hand[1:]

    def hit(self):
        self.update_hand([random.choice(GameState.deck)])
        print("Dealer hits.\nDealer's hand is now: " + str(self.get_hand()))

    def stay(self):
        print("Dealer stands on " + str(self.get_hand_value()) + ".")
        self.stand = True
    
    def turn_logic(self):
        print("Dealer's hand is: " + str(self.get_hand()))
        while self.get_hand_value() < 17:
            self.hit()
        if self.get_hand_value() <= 21:
            self.stay()
        else:
            print("Dealer busts!")
            self.bust = True

#Main
def main():
    gamestate = GameState()

    player_wallet = gamestate.initial_wallet()

    player = Player("Player1", player_wallet)
    dealer = Dealer()

    while player.out == False:
        player.take_bet()
        gamestate.collect_bets()
        gamestate.deal(dealer)
        player.get_hand_value()
        player.turn_logic()
        dealer.turn_logic()
        gamestate.reveal()
        gamestate.calculate_winner()
        gamestate.clear_hands()
        gamestate.check_outs()
main()