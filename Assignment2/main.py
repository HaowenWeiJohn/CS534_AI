from Assignment2 import game

def analysis


if __name__ == '__main__':

    players = []
    players.append(game.RandomPlayer("Foo"))
    players.append(game.RolloutPlayer("Bar"))
    players.append(game.GrabAndDuckPlayer("Baz"))
    Game = game.Game(players)
    
    players_after = Game.play()




