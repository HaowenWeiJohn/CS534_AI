from Assignment2 import game2




if __name__ == '__main__':

    players = []
    players.append(game2.RandomPlayer("Foo"))
    players.append(game2.RolloutPlayer("Bar"))
    players.append(game2.GrabAndDuckPlayer("Baz"))
    Game = game2.Game(players)
    
    players_after = Game.play()




