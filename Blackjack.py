import random
from time import sleep
from enum import Enum


class Player_Actions(Enum):
    HIT = 0
    STAND = 1

#GameState Class
class GameState():
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A"]
    #All players including the dealer
    players_all = []
    #All players NOT including the dealer
    players = []

    def __init__(self):
        self.pot = 0
        self.solo_game = False

    def add_player(self):
        while True:
            player_name = input("Please enter your player name: ")
            if player_name.isalpha():
                break
            else:
                print("Player name must be alphabetic characters only!")
        player_wallet = self.initial_wallet()
        player = Player(player_name, player_wallet)
    
    def initial_wallet(self):
        while True:
            wallet = input("What would you like your wallet to be? (Cannot be larger than $1000): $")
            if wallet.isnumeric():
                wallet = int(wallet)
                if wallet > 0 and wallet <= 1000:
                    return wallet
                else:
                    print("Wallet must be greater than $0 and no larger than $1000")
            else:
                print("Please enter a whole number")

    def collect_bets(self):
        for p in GameState.players:
            self.pot += p.get_bet()
                
    def deal(self, dealer):
        for object in GameState.players_all:
            for i in range(2):
                object.update_hand([random.choice(GameState.deck)])
        print("Cards have been dealt!")
        sleep(0.5)
        print(f"The dealer is showing [?]{dealer.get_hand_half()}")
    
    def reveal(self):
        print("Results!")
        for player in GameState.players_all:
            print(f"{player.name} has {player.get_hand()} with a value of {player.get_hand_value()}")
            sleep(0.5)
    
    def return_bets(self, winners):
            try:
                #Handle solo players getting a fair amount
                if self.solo_game:
                    winners[0].wallet += (winners[0].get_bet() * 2)
                else:
                    for p in winners:
                        p.wallet += round(self.pot / len(winners))
            except AttributeError:
                pass
            except IndexError:
                pass
    
    def calculate_winner(self):
        #Build list of non-busted players including dealer
        non_busted_players_all = []
        for p in GameState.players_all:
            if p.bust == False:
                non_busted_players_all.append(p)
        #print("Non busted: " + str(non_busted_players_all))
        #Check if all busted. Void round if all busted
        if len(non_busted_players_all) == 0:
            print("All busted! Round voided and bets returned!")
            self.return_bets(GameState.players)
        #Check if only one player won
        elif len(non_busted_players_all) == 1:
            print(f"{non_busted_players_all[0].name} won the round! They win the pot!")
            self.return_bets(non_busted_players_all)
        #Handle one or more players winning
        else:
            winners = []
            score = 0
            for p in non_busted_players_all:
                if p.get_hand_value() > score:
                    winners = []
                    winners.append(p)
                    score = p.get_hand_value()
                elif p.get_hand_value() == score:
                    winners.append(p)
            winner_names = [p.name for p in winners]
            print(f"The following players won the round: {winner_names}. The pot will be split equally among them.")
            self.return_bets([player for player in winners if not player.dealer])

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
                GameState.players_all.remove(p)
                GameState.players.remove(p)
    
    def check_solo_game(self):
        if len(GameState.players) == 1:
            self.solo_game = True

    def game_over(self):
        if len(GameState.players) == 0:
            return True
        else:
            return False


#Person Class
class Person():
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bust = False
        self.stand = False
        self.dealer = False
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
        print(f"Your current wallet is {self.get_wallet()}.")
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
        self.update_hand([random.choice(GameState.deck)])
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
                    if action == Player_Actions(0).name:
                        self.hit()
                        if self.get_hand_value() <= 21:
                            continue
                        else:
                            print("You bust!")
                            self.bust = True
                    elif action == Player_Actions(1).name:
                        self.stay()
                    else:
                        print("Invalid Input. Please choose Hit or Stand")

#Dealer Class - Inherits from Person
class Dealer(Person):

    def __init__(self):
        Person.__init__(self, "Dealer")
        self.hand = []
        self.dealer = True
    
    def get_hand_half(self):
        return self.hand[1:]

    def hit(self):
        newline = '\n'
        sleep(1)
        self.update_hand([random.choice(GameState.deck)])
        print(f"Dealer hits.{newline}Dealer's hand is now: {self.get_hand()}")
        sleep(1)

    def stay(self):
        sleep(0.5)
        print(f"Dealer stands on {self.get_hand_value()}.")
        self.stand = True
        sleep(1)
    
    def turn_logic(self):
        print(f"Dealer's hand is: {self.get_hand()}")
        while not self.bust:
            #build list of players beating the dealer (but not busted!). If this list is NOT empty, then hit. If this list is empty, then stay and break out of loop.
            beating_dealer = [player for player in GameState.players if player.get_hand_value() <= 21 and player.get_hand_value() > self.get_hand_value() ]
            print(beating_dealer)
            if beating_dealer != []:
                self.hit()
            else:
                self.stay()
                break
        print("Dealer busts!")

#Main
def main():
    gamestate = GameState()
    gamestate.add_player()
    dealer = Dealer()
    gamestate.check_solo_game()

    while not gamestate.game_over():
        for player in GameState.players:
            player.take_bet()
        gamestate.collect_bets()
        gamestate.deal(dealer)
        sleep(0.5)
        for player in GameState.players:
            player.get_hand_value()
            player.turn_logic()
        dealer.turn_logic()
        gamestate.reveal()
        gamestate.calculate_winner()
        gamestate.clear_hands()
        gamestate.check_outs()
        gamestate.check_solo_game()
main()