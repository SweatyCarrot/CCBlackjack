import random
from time import sleep
from enum import Enum

DECK = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A"]

class Player_Actions(Enum):
    HIT
    STAND

#GameState Class
class GameState():
    def __init__(self):
        self.pot = 0
        self.players_all = [Dealer()] # All players including the dealer
        self.players = [] # All players NOT including the dealer

    def add_player(self, name):
        player_wallet = gamestate.get_initial_wallet()
        player = Player(name, player_wallet)

        self.players_all.append(player)
        self.players.append(player)

    def get_initial_wallet(self):
        while True:
            user_input = input("What would you like your wallet to be? (Must be lower than $1000): $")
            if not is_digit(user_input):
                print("Input must be a number!", file=sys.stderr)
                continue

            wallet = int(user_input)
            if wallet <= 0 or wallet >= 1000:
                print("Amount must be between 1 and 999!", file=sys.stderr)
                continue

            return wallet

    def collect_bets(self):
        for player in self.players:
            self.pot += player.get_bet()
                
    def deal(self, dealer):
        for player in self.players_all:
            for i in range(2):
                player.add_card_to_hand(random.choice(DECK))
        print("Cards have been dealt!")
        sleep(0.5)
        print(f"The dealer is showing [?]{dealer.get_hand_half()}")
    
    def reveal(self):
        print("Results!")
        for player in self.players_all:
            print(f"{player.name} has {player.get_hand()} with a value of {player.get_hand_value()}")
            sleep(0.5)
    
    def return_bets(self, winners):
            if len(winners) == 1 and len(self.players) == 1:
                winner = winners[0]
                winner.wallet += winner.get_bet() * 2
            else:
                for player in winners:
                    player.wallet += round(self.pot / len(winners))
    
    def calculate_winner(self):
        #Build list of non-busted players including dealer
        non_busted_players_all = filter(lambda player: not player.bust, self.players_all)

        if len(non_busted_players_all) == 0:
            #Check if all busted. Void round if all busted
            print("All busted! Round voided and bets returned!")
            self.return_bets(self.players)
        elif len(non_busted_players_all) == 1:
            #Check if only one player won
            print(f"{non_busted_players_all[0].name} won the round! They win the pot!")
            self.return_bets(non_busted_players_all)
        else:
            #Handle one or more players winning
            highest_score = max(map(lambda player: player.get_hand_value(), non_busted_player_all))
            winners = filter(lambda player: player.get_hand_value() == highest_score, non_busted_players_all)
            winner_names = [player.name for player in winners]
            print(f"The following players won the round: {winner_names}. The pot will be split equally among them.")
            self.return_bets(winners)
            

    def clear_hands(self):
        self.pot = 0
        for player in self.players_all:
            player.bet = 0
            player.hand = []
            player.stand = False
            player.bust = False
    
    def check_outs(self):
        for player in self.players:
            if player.get_wallet() <= 0:
                player.is_out = True

#Person Class
class Person():
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bust = False
        self.stand = False

    def get_hand(self):
        return self.hand
    
    def add_card_to_hand(self, card):
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
        super().__init__(self, name)
        self.wallet = wallet
        self.bet = 0
        self.is_out = False

    def get_wallet(self):
        return self.wallet

    def update_wallet(self, value):
        self.wallet += value

    def get_bet(self):
        return self.bet

    def update_bet(self, value):
        self.bet += value

    def take_bet(self):
        print(f"Your current wallet is {self.get_wallet()}.")
        while True:
            bet_input = input("Please enter your bet: ")
            if not is_digit(bet_input):
                print("Must enter a number!", file=sys.stderr)
                continue

            bet_amount = int(bet_input)
            if bet_amount > self.get_wallet() or bet_amount <= 0:
                print("Amount must be more than 0 and less than your wallet balance!", file=sys.stderr)
                continue

            self.update_bet(bet_amount)
            self.update_wallet(-bet_amount)
            return

    def hit(self):
        sleep(0.5)
        self.add_card_to_hand(random.choice(DECK))
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
            sleep(0.5)
            print(f"Your current hand is {self.get_hand()}. Hand value: {self.get_hand_value()}\nWould you like to Hit or Stand?")
            while self.get_hand_value() <= 21 and not self.bust and not self.stand:
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
        super().__init__(self, "Dealer")
        self.hand = []
    
    def get_hand_half(self):
        return self.hand[1:]

    def hit(self):
        sleep(1)
        self.add_card_to_hand(random.choice(DECK))
        print(f"Dealer hits.\nDealer's hand is now: {self.get_hand()}")
        sleep(1)

    def stay(self):
        sleep(0.5)
        print(f"Dealer stands on {self.get_hand_value()}.")
        self.stand = True
        sleep(1)
    
    def turn_logic(self):
        print(f"Dealer's hand is: {self.get_hand()}")
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
    gamestate.add_player("Player1")

    while not player.is_out:
        player.take_bet()
        gamestate.collect_bets()
        gamestate.deal(dealer)
        sleep(0.5)
        player.get_hand_value()
        player.turn_logic()
        dealer.turn_logic()
        gamestate.reveal()
        gamestate.calculate_winner()
        gamestate.clear_hands()
        gamestate.check_outs()
main()
