from Assignment3 import game2
import numpy as np
import matplotlib.pyplot as plt
from Assignment3.deepQ_Learning import *
from Assignment3.QPlayer import QPlayer
from Assignment3 import tabel
import pickle
import copy
# def analysis():
#     thinking_times = [1.5]
#     # thinking_times = [0.01, 0.1] #0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
#
#     RandomPlayer = []
#     RolloutAI = []
#     GrabAndDuckPlayer = []
#     for thinking_time in thinking_times:
#         first = 0
#         second = 0
#         third = 0
#         for i in range(0, 20):
#             players = []
#             players.append(game2.GrabAndDuckPlayer("GrabAndDuckPlayer"))
#             players.append(game2.RolloutPlayer("RolloutAI", time_limit=thinking_time))
#             players.append(game2.RandomPlayer("RandomPlayer"))
#             ThisGame = game2.Game(players)
#             players_after = ThisGame.play()
#             if players_after[0].score >= 200: first += 1
#             if players_after[1].score >= 200: second += 1
#             if players_after[2].score >= 200: third += 1
#         RandomPlayer.append(first)
#         RolloutAI.append(second)
#         GrabAndDuckPlayer.append(third)
#
#     plt.plot(thinking_times, RandomPlayer, '-*')
#     plt.plot(thinking_times, RolloutAI, '-*')
#     plt.plot(thinking_times, GrabAndDuckPlayer, '-*')
#     plt.legend(['GrabAndDuckPlayer', 'RolloutAI', 'RandomPlayer'])
#     plt.xlabel('thinking time')
#     plt.ylabel('Wining round')
#     plt.grid()
#     plt.show()
#
#
# ##### The state contains




if __name__ == '__main__':
    q_model = Model()
    # q_model.model.load_weights('q_model_weights_Random_new.index')

    for i in range(15):
        players = []
        players.append(game2.RandomPlayer("RandomPlayer"))
        # players.append(QPlayer("RolloutAI", time_limit=0.1))
        players.append(QPlayer("QPlayer", time_limit=0.5))
        players.append(game2.RandomPlayer("RandomPlayer"))
        Game = game2.Game(players)

        players_after = Game.play(q_model)
    # analysis()
    Input = tabel.reward_history
    splits = 10

    # Finding average of each consecutive segment
    Output = [sum(Input[i:i + splits]) / splits
              for i in range(len(Input) - splits + 1)]

    plt.plot(Output)
    plt.show()


    q_model.model.save('q_model_save_test_long')
    pickle.dump(tabel.reward_history, open("q_model_save_test_long_history", "wb"))
