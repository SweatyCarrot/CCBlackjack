import gamestate
import dealer
from time import sleep

#Main
def main():
    game = gamestate.GameState()
    game.add_player()
    dealerMan = dealer.Dealer()
    game.check_solo_game()

    while not game.game_over():
        for player in game.players:
            player.take_bet()
        game.collect_bets()
        game.deal(dealerMan)
        sleep(0.5)
        for player in game.players:
            player.get_hand_value()
            player.turn_logic()
        dealerMan.turn_logic()
        game.reveal()
        game.calculate_winner()
        game.clear_hands()
        game.check_outs()
        game.check_solo_game()
main()