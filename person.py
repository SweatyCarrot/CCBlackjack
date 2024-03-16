import gamestate

#Person Class
class Person():
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bust = False
        self.stand = False
        self.dealer = False
        gamestate.GameState.players_all.append(self)

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