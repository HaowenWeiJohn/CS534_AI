import numpy as np
import  matplotlib.pyplot as plt

string = ''
for i in range(1, 194):
    print('"',str(i),'"', ',')


thinking_times = [0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 1]
RandomPlayer = [0,0,0,0,0, 0, 0]
GrabAndDuckPlayer = [16, 16, 7, 7, 7, 6, 4]
RolloutAI = [4, 4, 13, 13, 13, 14, 16]
plt.plot(thinking_times, RandomPlayer, '-*')
plt.plot(thinking_times, RolloutAI, '-*')
plt.plot(thinking_times, GrabAndDuckPlayer, '-*')
plt.legend(['RandomPlayer', 'RolloutAI', 'GrabAndDuckPlayer'])
plt.xlabel('thinking time')
plt.ylabel('Wining round')
plt.grid()
plt.show()

# thinking_times = [0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 1]
# RandomPlayer = [0,0,0,0,0]
# GrabAndDuckPlayer = [16, 16, 7, 7, 7, 6, 0]
# RolloutAI = [4, 4, 13, 13, 13, 14, 20]
# plt.plot(thinking_times, RandomPlayer, '-*')
# plt.plot(thinking_times, RolloutAI, '-*')
# plt.plot(thinking_times, GrabAndDuckPlayer, '-*')
# plt.legend(['RandomPlayer', 'RolloutAI', 'GrabAndDuckPlayer'])
# plt.xlabel('thinking time')
# plt.ylabel('Wining round')
# plt.grid()
# plt.show()

x = np.linspace(1,18,18)
print(x)
rollout_num = [1157, 1313, 1408, 1558, 1555, 1925, 2101, 2124, 2271, 2749, 3001, 3454, 3421, 3646, 4543, 4882, 4515, 5357]

rollout_num.reverse()
plt.plot(x, rollout_num)
plt.legend()
plt.xlabel('remaind hand')
plt.ylabel('rollout num')
plt.grid()
plt.show()


x = np.linspace(0.1,1.8,18)
print(x)
x = -x
run_time = 2.267969* np.exp(x)
print(run_time)

