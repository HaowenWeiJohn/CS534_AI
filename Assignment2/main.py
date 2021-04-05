from Assignment2 import game
import numpy as np
import matplotlib.pyplot as plt

def analysis():
    thinking_times = [1.5]
    # thinking_times = [0.01, 0.1] #0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]

    RandomPlayer = []
    RolloutAI = []
    GrabAndDuckPlayer = []
    for thinking_time in thinking_times:
        first = 0
        second = 0
        third = 0
        for i in range(0,20):
            players = []
            players.append(game.GrabAndDuckPlayer("GrabAndDuckPlayer"))
            players.append(game.RolloutPlayer("RolloutAI", time_limit=thinking_time))
            players.append(game.RandomPlayer("RandomPlayer"))
            ThisGame = game.Game(players)
            players_after = ThisGame.play()
            if players_after[0].score >= 200: first += 1
            if players_after[1].score >= 200: second += 1
            if players_after[2].score >= 200: third += 1
        RandomPlayer.append(first)
        RolloutAI.append(second)
        GrabAndDuckPlayer.append(third)

    plt.plot(thinking_times, RandomPlayer, '-*')
    plt.plot(thinking_times, RolloutAI, '-*')
    plt.plot(thinking_times, GrabAndDuckPlayer, '-*')
    plt.legend(['GrabAndDuckPlayer', 'RolloutAI', 'RandomPlayer'])
    plt.xlabel('thinking time')
    plt.ylabel('Wining round')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    # players = []
    # players.append(game.RandomPlayer("RandomPlayer"))
    # players.append(game.RolloutPlayer("RolloutAI", time_limit=0.1))
    # players.append(game.GrabAndDuckPlayer("GrabAndDuckPlayer"))
    # Game = game.Game(players)
    #
    # players_after = Game.play()
    analysis()