import person
import gamestate
import random
from time import sleep

class Dealer(person.Person):

    def __init__(self):
        person.Person.__init__(self, "Dealer")
        self.hand = []
        self.dealer = True
    
    def get_hand_half(self):
        return self.hand[1:]

    def hit(self):
        newline = '\n'
        sleep(1)
        self.update_hand([random.choice(gamestate.GameState.deck)])
        print(f"Dealer hits.{newline}Dealer's hand is now: {self.get_hand()}")
        if self.get_hand_value() > 21:
            print("Dealer busts!")
            self.bust = True
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
            beating_dealer = [player for player in gamestate.GameState.players if player.get_hand_value() <= 21 and player.get_hand_value() > self.get_hand_value()]
            if beating_dealer != []:
                self.hit()
            else:
                self.stay()
                break