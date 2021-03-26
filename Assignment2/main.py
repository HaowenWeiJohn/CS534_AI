from Assignment2 import game

if __name__ == '__main__':

    playahs = []
    playahs.append(game.RandomPlayer("Foo"))
    playahs.append(game.GrabAndDuckPlayer("Bar"))
    playahs.append(game.RandomPlayer("Baz"))
    game = game.Game(playahs)
    
    game.play()
