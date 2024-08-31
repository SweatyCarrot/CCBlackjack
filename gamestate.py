import random
from time import sleep
import player

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
        player.Player(player_name, player_wallet)
    
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
        sleep(0.5)
        print("||| Results |||")
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