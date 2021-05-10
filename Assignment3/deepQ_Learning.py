import tensorflow as tf

import numpy as np
import base64, io, time, gym
import IPython, functools
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from Assignment3 import tabel
# Download and import the MIT 6.S191 package

import mitdeeplearning as mdl


# Input Size:
# ZOMBIE_ARMY number of ZOMBIE_ARMY for player 1 2 3
# Unknown card: 0
# played card: 0.5
# card in hand: 1

# node: ZOMBIE_ARMY normalize: with 12 (3 node)
# node: card information: 18*3+6 node

# output: 18*3+6 get the possible output hand only

class Memory:
    def __init__(self):
        self.clear()

    # Resets/restarts the memory buffer
    def clear(self):
        self.observations = []
        self.actions = []
        self.rewards = []

    # # Add observations, actions, rewards to memory
    # def add_to_memory(self, new_observation, new_action, new_reward):
    #     self.observations.append(new_observation)
    #     self.actions.append(new_action)
    #     self.rewards.append(new_reward)


class Model:
    def __init__(self):
        self.model = None
        self.n_actions = 60
        self.learning_rate = 1e-5
        self.optimizer = tf.keras.optimizers.Adam(self.learning_rate)
        self.model = self.make_model()
        self.memory = Memory()

    def make_model(self):
        model = tf.keras.models.Sequential([


            tf.keras.layers.Dense(units=512, activation='relu'),
            tf.keras.layers.Dense(units=1024, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(units=1024, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(units=2048, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(units=2048, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(units=1024, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(units=512, activation='relu'),


            tf.keras.layers.Dense(units=self.n_actions, activation='softmax')

        ])
        return model


def train_step(model, optimizer, observations, actions, discounted_rewards):
    with tf.GradientTape() as tape:
        # Forward propagate through the agent network
        logits = model(observations)

        '''TODO: call the compute_loss function to compute the loss'''
        loss = compute_loss(logits, actions, discounted_rewards)  # TODO
        # loss = compute_loss('''TODO''', '''TODO''', '''TODO''')

    '''TODO: run backpropagation to minimize the loss using the tape.gradient method'''
    grads = tape.gradient(loss, model.trainable_variables)  # TODO
    # grads = tape.gradient('''TODO''', model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))


def compute_loss(logits, actions, rewards):
    '''TODO: complete the function call to compute the negative log probabilities'''
    neg_logprob = tf.nn.sparse_softmax_cross_entropy_with_logits(
        logits=logits, labels=actions)  # TODO
    # neg_logprob = tf.nn.sparse_softmax_cross_entropy_with_logits(
    #    logits='''TODO''', labels='''TODO''')

    '''TODO: scale the negative log probability by the rewards'''
    loss = tf.reduce_mean(neg_logprob * rewards)  # TODO
    # loss = tf.reduce_mean('''TODO''')
    return loss


def discount_rewards(rewards, gamma=0.35):
    discounted_rewards = np.zeros_like(rewards).astype(np.float32)
    R = 0
    for t in reversed(range(0, len(rewards))):
        # update the total discounted reward
        R = R * gamma + rewards[t]
        discounted_rewards[t] = R

    return normalize(discounted_rewards)


# Helper function that normalizes an np.array x
def normalize(x):
    x -= np.mean(x)
    x /= np.std(x)
    return x.astype(np.float32)


def choose_action(model, observation, possibleHands, single=True):
    # add batch dimension to the observation if only a single example was provided
    observation = np.expand_dims(observation, axis=0) if single else observation

    '''TODO: feed the observations through the model to predict the log probabilities of each possible action.'''
    logits = model.predict(observation)  # TODO
    # logits = model.predict('''TODO''')
    logits = logits.flatten()

    action = tabel.deck.index(possibleHands[0])
    for hand in possibleHands:
        if logits[tabel.deck.index(hand)] > logits[action]:
            action = tabel.deck.index(hand)

    # '''TODO: Choose an action from the categorical distribution defined by the log
    #   probabilities of each possible action.'''
    # action = tf.random.categorical(logits, num_samples=1)
    # # action = ['''TODO''']
    #
    # action = action.numpy().flatten()

    return action
