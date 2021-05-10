import random
import copy
import numpy as np
import abc
import time
from Assignment3.deepQ_Learning import *
from Assignment3 import tabel


class Deck():
    def __init__(self):
        self.deck = []
        self.shuffle()

    def __str__(self):
        # Print the list without the brackets
        return str(self.deck).strip('[]')

    def shuffle(self):
        self.deck = []
        for suit in ['U', 'F', 'Z', 'T']:
            for i in range(15):
                self.deck.append((suit, i))
        random.shuffle(self.deck)

    def getCard(self):
        return self.deck.pop()


class Player(metaclass=abc.ABCMeta):  # This is an abstract base class.
    def __init__(self, name):
        self.name = name
        self.hand = []  # List of cards (tuples). I don't think this needs to be a class....
        self.score = 0
        self.zombie_count = 0

    def __repr__(self):  # If __str__ is not defined this will be used. Allows easy printing
        # of a list of these, e.g. "print(players)" below.
        return str(self.name) + ": " + str(self.hand) + "\n"

    @abc.abstractmethod
    def playCard(self, trick):
        pass

    def randomPlay(self, trick):
        random.shuffle(self.hand)
        # print("-", self.name + "(" + str(self.score) + ")(Z" + str(self.zombie_count) + ")", "sees", trick)
        if len(trick) != 0:
            # Figure out what was led and follow it if we can
            suit = trick[0][0]
            # print(self.name, ":", suit, "was led")
            # Get the first occurence of a matching suit in our hand
            # This 'next' thing below is a "generator expression"
            card_idx = next((i for i, c in enumerate(self.hand) if c[0] == suit), None)
            if card_idx != None:
                return self.hand.pop(card_idx)
        # If the trick is empty or if we can't follow suit, return anything
        return self.hand.pop()

    def directPlay(self, hand):
        self.hand.remove(hand)
        return hand


class RandomPlayer(Player):  # Inherit from Player
    def __init__(self, name):
        super().__init__(name)

    def playCard(self, trick):
        random.shuffle(self.hand)
        print("-", self.name + "(" + str(self.score) + ")(Z" + str(self.zombie_count) + ")", "sees", trick)
        if len(trick) != 0:
            # Figure out what was led and follow it if we can
            suit = trick[0][0]
            # print(self.name, ":", suit, "was led")
            # Get the first occurence of a matching suit in our hand
            # This 'next' thing below is a "generator expression"
            card_idx = next((i for i, c in enumerate(self.hand) if c[0] == suit), None)
            if card_idx != None:
                return self.hand.pop(card_idx)
        # If the trick is empty or if we can't follow suit, return anything
        return self.hand.pop()


class GrabAndDuckPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def getindex(self, suit, int):  # int = 1, return maxindex, int = 0,return minindex
        min = 0
        max = 0
        card_idx = 0
        card_judge = 0
        if int == 1:
            while card_judge != None:
                max = self.hand[card_idx][1]
                card_judge = next((i for i, c in enumerate(self.hand)
                                   if i > card_idx and c[0] == suit and c[1] > max), None)
                if card_judge != None:
                    card_idx = card_judge
            return card_idx

        else:

            while card_judge != None:
                min = self.hand[0][1]
                card_judge = next((i for i, c in enumerate(self.hand)
                                   if i > card_idx and c[0] == suit and c[1] < min), None)
                if card_judge != None:
                    card_idx = card_judge

        return card_idx

    def playCard(self, trick):
        random.shuffle(self.hand)
        print("-", self.name + "(" + str(self.score) + ")(Z" + str(self.zombie_count) + ")", "sees", trick)
        min = 0
        max = 0
        card_judge = 0
        if len(trick) != 0:
            suit = trick[0][0]
            value = trick[0][1]
            if suit == 'U':
                card_idx = next((i for i, c in enumerate(self.hand) if c[0] == suit), None)
                if card_idx != None:
                    card_idx = next((i for i, c in enumerate(self.hand) if c[0] == suit and c[1] > value), None)
                    if card_idx != None:
                        card_judge = card_idx
                        while card_judge != None:
                            min = self.hand[card_idx][1]
                            card_judge = next((i for i, c in enumerate(self.hand)
                                               if i > card_idx and c[0] == suit and c[1] > value and c[1] < min), None)
                            if card_judge != None:
                                card_idx = card_judge

                    else:
                        card_idx = self.getindex(suit, 0)
                else:
                    card_idx = next((i for i, c in enumerate(self.hand) if c[0] == 'T'), None)
                    if card_idx != None:
                        card_idx = self.getindex('T', 0)
                    elif next((i for i, c in enumerate(self.hand) if c[0] == 'Z'), None) != None:
                        card_idx = self.getindex('Z', 1)
                    else:
                        card_idx = self.getindex('F', 0)

                return self.hand.pop(card_idx)

            if suit == 'F':
                card_idx = next((i for i, c in enumerate(self.hand) if c[0] == suit), None)
                if card_idx != None:
                    card_idx = next((i for i, c in enumerate(self.hand) if c[0] == suit and c[1] > value), None)
                    if card_idx != None:
                        while card_judge != None:
                            min = self.hand[card_idx][1]
                            card_judge = next((i for i, c in enumerate(self.hand)
                                               if i > card_idx and c[0] == suit and c[1] > value and c[1] < min), None)
                            if card_judge != None:
                                card_idx = card_judge
                    else:
                        card_idx = self.getindex(suit, 0)
                else:
                    card_idx = next((i for i, c in enumerate(self.hand) if c[0] == 'Z'), None)
                    if card_idx != None:
                        card_idx = self.getindex('Z', 1)
                    elif next((i for i, c in enumerate(self.hand) if c[0] == 'T'), None) != None:
                        card_idx = self.getindex('T', 0)
                    else:
                        card_idx = self.getindex('U', 0)

                return self.hand.pop(card_idx)

            if suit == 'Z':
                card_idx = next((i for i, c in enumerate(self.hand) if c[0] == suit), None)
                if card_idx != None:
                    card_idx = next((i for i, c in enumerate(self.hand) if c[0] == suit and c[1] < value), None)
                    if card_idx != None:

                        while card_judge != None:
                            max = self.hand[card_idx][1]
                            card_judge = next((i for i, c in enumerate(self.hand)
                                               if i > card_idx and c[0] == suit and c[1] < value and c[1] > max), None)
                            if card_judge != None:
                                card_idx = card_judge

                    else:
                        card_idx = self.getindex(suit, 1)
                else:
                    card_idx = next((i for i, c in enumerate(self.hand) if c[0] == 'T'), None)
                    if card_idx != None:
                        card_idx = self.getindex('T', 0)
                    elif next((i for i, c in enumerate(self.hand) if c[0] == 'F'), None) != None:
                        card_idx = self.getindex('F', 0)
                    else:
                        card_idx = self.getindex('U', 0)

                return self.hand.pop(card_idx)

            if suit == 'T':
                card_idx = next((i for i, c in enumerate(self.hand) if c[0] == suit), None)
                if card_idx != None:
                    card_idx = next((i for i, c in enumerate(self.hand) if c[0] == suit and c[1] > value), None)
                    if card_idx != None:
                        while card_judge != None:
                            min = self.hand[card_idx][1]
                            card_judge = next((i for i, c in enumerate(self.hand)
                                               if i > card_idx and c[0] == suit and c[1] > value and c[1] < min), None)
                            if card_judge != None:
                                card_idx = card_judge

                    else:
                        card_idx = self.getindex(suit, 0)
                else:
                    card_idx = next((i for i, c in enumerate(self.hand) if c[0] == 'Z'), None)
                    if card_idx != None:
                        card_idx = self.getindex('Z', 1)
                    elif next((i for i, c in enumerate(self.hand) if c[0] == 'F'), None) != None:
                        card_idx = self.getindex('F', 0)
                    else:
                        card_idx = self.getindex('U', 0)

                return self.hand.pop(card_idx)

        else:
            card_idx = next((i for i, c in enumerate(self.hand) if c[0] == 'T'), None)
            if card_idx != None:
                card_idx = self.getindex('T', 0)
            elif next((i for i, c in enumerate(self.hand) if c[0] == 'Z'), None) != None:
                card_idx = self.getindex('Z', 0)
            elif next((i for i, c in enumerate(self.hand) if c[0] == 'F'), None) != None:
                card_idx = self.getindex('F', 1)
            else:
                card_idx = self.getindex('U', 1)
            return self.hand.pop(card_idx)


class RolloutPlayer(Player):
    def __init__(self, name, total_playerNum=3, time_limit=1):
        super().__init__(name)

        self.trick = None
        self.time_limit = time_limit
        self.dummy_players = None
        self.dummy_p_idx = None
        self.undealed = None
        self.lead_player = None

        self.simulate_players = None
        self.simulated_undealed = None

        self.unknownHands = None

    def playCard(self, trick, dummy_players, dummy_p_idx, undealed, lead_player, playerHasNo):
        allPossibleHands = self.allPossibleHands(trick)

        gain_list = list(np.zeros(len(allPossibleHands)))

        print("-", self.name + "(" + str(self.score) + ")(Z" + str(self.zombie_count) + ")", "sees", trick)

        self.dummy_p_idx = dummy_p_idx
        self.dummy_players = dummy_players
        self.simulate_players = copy.deepcopy(dummy_players)
        self.undealed = undealed
        self.trick = trick
        self.lead_player = lead_player
        self.playerHasNo = playerHasNo
        self.getAllUnknownHands()

        start_time = time.time()
        time_cost = 0
        while time_cost < self.time_limit:
            for i in range(0, len(allPossibleHands)):
                this_gain = self.oneRound(startingTrick=allPossibleHands[i])
                gain_list[i] += this_gain

            time_cost = time.time() - start_time

        max_index = gain_list.index(max(gain_list))
        hand_to_play = allPossibleHands[max_index]
        self.hand.remove(hand_to_play)
        return hand_to_play

        # pop the one with highest gain

        # pass  # This is just a placeholder, remove when real code goes here

    def oneRound(self, startingTrick):
        gain = 0
        self.create_simulation_players()
        oneRound = Game(self.simulate_players)
        oneRound.deck.deck = self.simulated_undealed
        scoreDifference = oneRound.playOneRound(trick=copy.copy(self.trick),
                                                lead_player=copy.copy(self.lead_player),
                                                trickstartingTrick=copy.copy(startingTrick))

        for i in range(0, len(self.dummy_players)):
            if i != self.dummy_p_idx:
                gain += (scoreDifference[self.dummy_p_idx] - scoreDifference[i])
        # return simulate_players

        return gain

    # create simulated players and undealed hand
    def create_simulation_players(self):
        unknownHands = copy.copy(self.unknownHands)
        random.shuffle(unknownHands)
        for i in range(0, len(self.dummy_players)):
            self.simulate_players[i].name = copy.copy(self.dummy_players[i].name)
            self.simulate_players[i].hand = copy.copy(self.dummy_players[i].hand)
            self.simulate_players[i].score = copy.copy(self.dummy_players[i].score)
            self.simulate_players[i].zombie_count = copy.copy(self.dummy_players[i].zombie_count)
            # test = copy.deepcopy(self.dummy_players)
        # self.simulate_players = test
        # for i in range(0, len(self.dummy_players)):
        j = 0
        while j < len(self.dummy_players):
            if j != self.dummy_p_idx:
                # length = len(self.dummy_players[i].hand)
                # a = unknownHands[0:length]
                # self.simulate_players[i].hand = a
                # unknownHands = unknownHands[length:]

                length = len(self.dummy_players[j].hand)
                self.simulate_players[j].hand.clear()
                count = 0
                while self.playerHasNo[j][unknownHands[0][0]] and length > 0:
                    count = count + 1
                    if count > len(unknownHands):
                        unknownHands = copy.copy(self.unknownHands)
                        break
                    unknownHands.append(unknownHands.pop(0))
                if count > len(unknownHands):
                    j = 0
                    continue
                a = unknownHands[0:length]
                self.simulate_players[j].hand = a
                unknownHands = unknownHands[length:]
                random.shuffle(unknownHands)
            j = j + 1

        self.simulated_undealed = unknownHands

    def getAllUnknownHands(self):
        unknownHands = []
        # all unknown cards
        for i in range(0, len(self.dummy_players)):
            if i != self.dummy_p_idx:
                unknownHands.append(self.dummy_players[i].hand)
        unknownHands.append(self.undealed)
        unknownHands = sum(unknownHands, [])

        # shuffle unknown hands
        random.shuffle(unknownHands)
        self.unknownHands = unknownHands

    def allPossibleHands(self, trick):
        allPossibleHands = []
        if not trick:
            allPossibleHands = self.hand
        else:
            # find all the card that matches with the first one
            allPossibleHands = [hand for hand in self.hand if hand[0] == trick[0][0]]
        if not allPossibleHands:
            allPossibleHands = self.hand

        return allPossibleHands


class MctsPlayer(Player):
    def __init__(self, name, total_playerNum=3, time_limit=1):
        super().__init__(name)

        self.trick = None
        self.time_limit = time_limit
        self.dummy_players = None
        self.dummy_p_idx = None
        self.undealed = None
        self.lead_player = None

        self.simulate_players = None
        self.simulated_undealed = None

        self.unknownHands = None

    def oneRound(self, startingTrick):
        gain = 0
        self.create_simulation_players()
        oneRound = Game(self.simulate_players)
        oneRound.deck.deck = self.simulated_undealed
        scoreDifference = oneRound.playOneRound(trick=copy.copy(self.trick),
                                                lead_player=copy.copy(self.lead_player),
                                                trickstartingTrick=copy.copy(startingTrick))

        # for i in range(0, len(self.dummy_players)):
        #    if i != self.dummy_p_idx:
        #        gain += (scoreDifference[self.dummy_p_idx] - scoreDifference[i])
        ## return simulate_players
        a = scoreDifference[self.dummy_p_idx]
        scoreDifference.pop(self.dummy_p_idx)
        b = max(scoreDifference)
        gain = a - b
        return gain

    # create simulated players and undealed hand
    def create_simulation_players(self):
        unknownHands = copy.copy(self.unknownHands)
        random.shuffle(unknownHands)
        for i in range(0, len(self.dummy_players)):
            self.simulate_players[i].name = copy.copy(self.dummy_players[i].name)
            self.simulate_players[i].hand = copy.copy(self.dummy_players[i].hand)
            self.simulate_players[i].score = copy.copy(self.dummy_players[i].score)
            self.simulate_players[i].zombie_count = copy.copy(self.dummy_players[i].zombie_count)
            # test = copy.deepcopy(self.dummy_players)
        # self.simulate_players = test
        # for i in range(0, len(self.dummy_players)):
        j = 0
        while j < len(self.dummy_players):
            if j != self.dummy_p_idx:
                # length = len(self.dummy_players[i].hand)
                # a = unknownHands[0:length]
                # self.simulate_players[i].hand = a
                # unknownHands = unknownHands[length:]

                length = len(self.dummy_players[j].hand)
                self.simulate_players[j].hand.clear()
                count = 0
                while self.playerHasNo[j][unknownHands[0][0]] and length > 0:
                    count = count + 1
                    if count > len(unknownHands):
                        unknownHands = copy.copy(self.unknownHands)
                        break
                    unknownHands.append(unknownHands.pop(0))
                if count > len(unknownHands):
                    j = 0
                    continue
                a = unknownHands[0:length]
                self.simulate_players[j].hand = a
                unknownHands = unknownHands[length:]
                random.shuffle(unknownHands)
            j = j + 1

        self.simulated_undealed = unknownHands

    def getAllUnknownHands(self):
        unknownHands = []
        # all unknown cards
        for i in range(0, len(self.dummy_players)):
            if i != self.dummy_p_idx:
                unknownHands.append(self.dummy_players[i].hand)
        unknownHands.append(self.undealed)
        unknownHands = sum(unknownHands, [])

        # shuffle unknown hands
        random.shuffle(unknownHands)
        self.unknownHands = unknownHands

    def allPossibleHands(self, trick):
        allPossibleHands = []
        if not trick:
            allPossibleHands = self.hand
        else:
            # find all the card that matches with the first one
            allPossibleHands = [hand for hand in self.hand if hand[0] == trick[0][0]]
        if not allPossibleHands:
            allPossibleHands = self.hand

        return allPossibleHands

    def playCard(self, trick, dummy_players, dummy_p_idx, undealed, lead_player, playerHasNo):

        print("-", self.name + "(" + str(self.score) + ")(Z" + str(self.zombie_count) + ")", "sees", trick)
        self.dummy_p_idx = dummy_p_idx
        self.dummy_players = dummy_players
        self.simulate_players = copy.deepcopy(dummy_players)
        self.undealed = undealed
        self.trick = trick
        self.lead_player = lead_player
        self.playerHasNo = playerHasNo
        self.getAllUnknownHands()

        self.rootNode = MctsNode(None)
        start_time = time.time()
        time_cost = 0
        while time_cost < self.time_limit:
            leafNode = self.selection()
            selectedNode = self.expansion(leafNode)
            value = self.simulation(selectedNode)
            self.backPropagation(selectedNode, value)
            time_cost = time.time() - start_time

        maxInvestigate = 0
        hand_to_play = self.rootNode.child[0].hand
        for i in range(len(self.rootNode.child)):
            if self.rootNode.child[i].investigate > maxInvestigate:
                maxInvestigate = self.rootNode.child[i].investigate
                hand_to_play = self.rootNode.child[i].hand
        if maxInvestigate >= 10:
            print('Reuse Occurs')
        self.hand.remove(hand_to_play)
        return hand_to_play

    def selection(self):
        currentNode = self.rootNode
        if len(currentNode.child) == 0:
            return currentNode
        else:
            maxUCB = currentNode.child[0].UCB
            next_idx = 0
            for i in range(len(currentNode.child)):
                if currentNode.child[i].UCB == None:
                    return currentNode.child[i]
                elif currentNode.child[i].UCB > maxUCB:
                    maxUCB = currentNode.child[i].UCB
                    next_idx = i
            return currentNode.child[next_idx]

    def expansion(self, node):
        if node == self.rootNode:
            allPossibleHands = self.allPossibleHands(self.trick)
            for hand in allPossibleHands:
                node.child.append(MctsNode(hand, node))
            return node.child[0]
        else:
            return node

    def simulation(self, node):
        value = self.oneRound(startingTrick=node.hand)
        return value

    def backPropagation(self, node, value):
        self.rootNode.investigate = self.rootNode.investigate + 1
        self.rootNode.value = self.rootNode.value + value
        self.rootNode.updateUCB(self.rootNode.investigate)
        while node.father != None:
            node.investigate = node.investigate + 1
            node.value = node.value + value
            node.updateUCB(self.rootNode.investigate)
            node = node.father


class MctsNode():
    def __init__(self, hand, father=None):
        self.hand = hand
        self.investigate = 0
        self.value = 0
        self.hand = hand
        self.father = father
        self.child = []

        self.UCB = None

    def updateUCB(self, totalInvestigate):
        if self.investigate == 0:
            self.UCB = None
        else:
            self.UCB = self.value / self.investigate + 2 * np.sqrt(np.log(totalInvestigate) / self.investigate)


class Game():  # Main class
    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.dummy_players = copy.deepcopy(players)
        self.played_cards = []  # List of already played cards

        # some constants
        self.HAND_SIZE = 18
        self.ZOMBIE_ARMY = 12
        self.ZOMBIE_ARMY_PENALTY = 20
        self.WIN_SCORE = 200

    def deal(self):
        self.deck.shuffle()
        self.played_cards = []
        for i in range(self.HAND_SIZE):
            for p in self.players:
                p.hand.append(self.deck.getCard())

    def scoreTrick(self, trick):
        # Score the trick and add the score to the winning player
        # Get the suit led
        suit = trick[0][0]
        value = trick[0][1]
        winner = 0
        score = 0
        # Determine who won (trick position not player!)
        for i in range(len(trick) - 1):
            if trick[i + 1][0] == suit and trick[i + 1][1] > value:
                winner = i + 1
                value = trick[i + 1][1]
        # Determine the score
        # Separate the suit and value tuples
        suits_list = list(zip(*trick))[0]
        if suits_list.count('T') == 0:
            # No Trolls, go ahead and score the unicorns
            score += suits_list.count('U') * 3
        score += suits_list.count('F') * 2
        n_zomb = suits_list.count('Z')
        score -= n_zomb
        return winner, score, n_zomb  # Index of winning card

    def play(self, q_model):
        lead_player = 0
        playerHasNo = []

        while True:  # Keep looping on hands until we have a winner
            self.deal()
            playerHasNo.clear()
            for _ in range(len(self.players)):
                playerHasNo.append({'U': False, 'F': False, 'T': False, 'Z': False})
            while len(self.players[0].hand) > 0:
                trick = []

                # Form the trick, get a card from each player. Score the trick.
                for i in range(len(self.players)):
                    p_idx = (lead_player + i) % len(self.players)
                    # print(type(self.players[p_idx]).__name__)
                    if type(self.players[p_idx]).__name__ in ('RandomPlayer', 'GrabAndDuckPlayer'):
                        trick.append(self.players[p_idx].playCard(trick))
                    else:  # run AI assignment
                        # copy the current player list to local variable
                        # dummy_players = copy.deepcopy(self.players)
                        for i in range(0, len(self.dummy_players)):
                            self.dummy_players[i].name = copy.copy(self.players[i].name)
                            self.dummy_players[i].hand = copy.copy(self.players[i].hand)
                            self.dummy_players[i].score = copy.copy(self.players[i].score)
                            self.dummy_players[i].zombie_count = copy.copy(self.players[i].zombie_count)
                        dummy_p_idx = copy.deepcopy(p_idx)
                        undeald = copy.deepcopy(self.deck.deck)
                        dummy_lead_player = copy.deepcopy(lead_player)
                        played_trick = self.players[p_idx].playCard(trick, self.dummy_players, dummy_p_idx, undeald,
                                                                    dummy_lead_player, playerHasNo, q_model)
                        trick.append(played_trick)
                    if trick[-1][0] != trick[0][0]:
                        playerHasNo[p_idx][trick[0][0]] = True
                        print(self.players[p_idx].name, "run out of", trick[0][0])
                print(self.players[lead_player].name, "led:", trick)
                win_idx, score, n_zomb = self.scoreTrick(trick)

                # Convert winning trick index into new lead player index
                lead_player = (lead_player + win_idx) % len(self.players)
                print(self.players[lead_player].name, "won trick", score, "points")

                # get reward for Q learning AI:
                if self.players[lead_player].name == 'QPlayer':
                    q_model.memory.rewards.append(score)
                elif score < 0:
                    q_model.memory.rewards.append(score/2)
                else:
                    q_model.memory.rewards.append(-score/2)

                # Check for zombie army
                self.players[lead_player].zombie_count += n_zomb
                if self.players[lead_player].zombie_count >= self.ZOMBIE_ARMY:  # Uh-oh here comes the Zombie army!
                    self.players[lead_player].zombie_count = 0
                    print("***** ZOMBIE ARMY *****")
                    # Subtract 20 points from each opponent
                    for i in range(len(self.players) - 1):
                        self.players[(lead_player + 1 + i) % len(self.players)].score -= self.ZOMBIE_ARMY_PENALTY

                # Update score & check if won
                self.players[lead_player].score += score
                if self.players[lead_player].score >= self.WIN_SCORE:
                    print(self.players[lead_player].name, "won with", self.players[lead_player].score, "points!")
                    q_model.memory.clear()
                    return self.players

                    # Keep track of the cards played
                self.played_cards.extend(trick)

            # Score the kitty (undealt cards)

            # train the Model with memory in this round the Memory was initialized in

            # Train the model with all the memory and clear the memory for this round

            # initiate training - remember we don't know anything about how the
            #   agent is doing until it has crashed!
            print(np.sum(q_model.memory.rewards))
            tabel.reward_history.append(np.sum(q_model.memory.rewards))
            train_step(model=q_model.model, optimizer=q_model.optimizer,
                       observations=np.vstack(q_model.memory.observations),
                       actions=np.array(q_model.memory.actions),
                       discounted_rewards=discount_rewards(q_model.memory.rewards))



            # reset the memory
            q_model.memory.clear()

            print(self.deck)
            win_idx, score, n_zomb = self.scoreTrick(self.deck.deck)
            print(self.players[lead_player].name, "gets", score, "points from the kitty")
            self.players[lead_player].score += score

            # Check for zombie army
            if self.players[lead_player].zombie_count + n_zomb >= self.ZOMBIE_ARMY:
                print("***** ZOMBIE ARMY *****")
                # Subtract 20 points from each opponent
                for i in range(len(self.players) - 1):
                    self.players[(lead_player + 1 + i) % len(self.players)].score -= self.ZOMBIE_ARMY_PENALTY

            # Check for winner
            if self.players[lead_player].score >= self.WIN_SCORE:
                print(self.players[lead_player].name, "won with", self.players[lead_player].score, "points!")
                return self.players

            print("\n* Deal a new hand! *\n")
            # reset the zombie count
            for p in self.players:
                p.zombie_count = 0

    def playOneRound(self, trick, lead_player, trickstartingTrick):
        intitial_score = []
        end_score = []
        difference = []
        trick = trick
        for player in self.players:
            intitial_score.append(player.score)

        while len(self.players[lead_player].hand) > 0:

            # Form the trick, get a card from each player. Score the trick.
            index_offset = 0
            for i in range(len(self.players) - len(trick)):
                if i == 0 and len(self.players) - len(
                        trick) != len(self.players):  # in this case we are running the first play in round
                    index_offset = len(trick)
                    p_idx = (lead_player + i + index_offset) % len(self.players)
                    trick.append(self.players[p_idx].directPlay(trickstartingTrick))
                else:
                    p_idx = (lead_player + i + index_offset) % len(self.players)
                    trick.append(self.players[p_idx].randomPlay(trick))
            index_offset = 0

            # print(self.players[lead_player].name, "led:", trick)
            win_idx, score, n_zomb = self.scoreTrick(trick)

            # Convert winning trick index into new lead player index
            lead_player = (lead_player + win_idx) % len(self.players)
            # print(self.players[lead_player].name, "won trick", score, "points")

            # Check for zombie army
            self.players[lead_player].zombie_count += n_zomb
            if self.players[lead_player].zombie_count >= self.ZOMBIE_ARMY:  # Uh-oh here comes the Zombie army!
                self.players[lead_player].zombie_count = 0
                # print("***** ZOMBIE ARMY *****")
                # Subtract 20 points from each opponent
                for i in range(len(self.players) - 1):
                    self.players[(lead_player + 1 + i) % len(self.players)].score -= self.ZOMBIE_ARMY_PENALTY

            # Update score & check if won
            self.players[lead_player].score += score
            # if self.players[lead_player].score >= self.WIN_SCORE:
            #     print(self.players[lead_player].name, "won with", self.players[lead_player].score, "points!")
            #     return

            # Keep track of the cards played
            self.played_cards.extend(trick)
            trick = []

        # Score the kitty (undealt cards)
        # print(self.deck)
        win_idx, score, n_zomb = self.scoreTrick(self.deck.deck)
        # print(self.players[lead_player].name, "gets", score, "points from the kitty")
        self.players[lead_player].score += score

        # Check for zombie army
        if self.players[lead_player].zombie_count + n_zomb >= self.ZOMBIE_ARMY:
            # print("***** ZOMBIE ARMY *****")
            # Subtract 20 points from each opponent
            for i in range(len(self.players) - 1):
                self.players[(lead_player + 1 + i) % len(self.players)].score -= self.ZOMBIE_ARMY_PENALTY

        for player in self.players:
            end_score.append(player.score)

        zip_object = zip(end_score, intitial_score)
        for list1_i, list2_i in zip_object:
            difference.append(list1_i - list2_i)

        return difference
        # # Check for winner
        # if self.players[lead_player].score >= self.WIN_SCORE:
        #     print(self.players[lead_player].name, "won with", self.players[lead_player].score, "points!")
        #     return

        # print("\n* Deal a new hand! *\n")
        # # reset the zombie count
        # for p in self.players:
        #     p.zombie_count = 0


class QPlayer(Player):  # Inherit from Player

    def __init__(self, name, total_playerNum=3, time_limit=1):
        super().__init__(name)

        self.trick = None
        self.time_limit = time_limit
        self.dummy_players = None
        self.dummy_p_idx = None
        self.undealed = None
        self.lead_player = None

        self.simulate_players = None
        self.simulated_undealed = None

        self.unknownHands = None

    def create_observation_dict(self):
        self.deck = []
        for suit in ['U', 'F', 'Z', 'T']:
            for i in range(15):
                self.deck.append((suit, i))

        self.observation_dict = {}
        for card in self.deck:
            self.observation_dict[card] = 0

        # self.observation_dict['zombie_count1'] = 0
        # self.observation_dict['zombie_count2'] = 0
        # self.observation_dict['zombie_count3'] = 0
        # self.observation_dict['lead_player'] = 0

    def getAllUnknownHands(self):
        unknownHands = []
        # all unknown cards
        for i in range(0, len(self.dummy_players)):
            if i != self.dummy_p_idx:
                unknownHands.append(self.dummy_players[i].hand)
        unknownHands.append(self.undealed)
        unknownHands = sum(unknownHands, [])

        # shuffle unknown hands
        random.shuffle(unknownHands)
        self.unknownHands = unknownHands
        return unknownHands

    def allPossibleHands(self, trick):
        allPossibleHands = []
        if not trick:
            allPossibleHands = self.hand
        else:
            # find all the card that matches with the first one
            allPossibleHands = [hand for hand in self.hand if hand[0] == trick[0][0]]
        if not allPossibleHands:
            allPossibleHands = self.hand

        return allPossibleHands

    def playCard(self, trick, dummy_players, dummy_p_idx, undealed, lead_player, playerHasNo, q_model):
        allPossibleHands = self.allPossibleHands(trick)
        allUnknownHnads = self.getAllUnknownHands()

        for possibleHand in allPossibleHands:
            self.observation_dict[possibleHand] = 2

        for hand in self.hand:
            self.observation_dict[hand] = 1

        for unknownHand in allUnknownHnads:
            self.observation_dict[unknownHand] = 0

        # print("-", self.name + "(" + str(self.score) + ")(Z" + str(self.zombie_count) + ")", "sees", trick)
        #
        # self.dummy_p_idx = dummy_p_idx
        # self.dummy_players = dummy_players
        # self.simulate_players = copy.deepcopy(dummy_players)
        # self.undealed = undealed
        # self.trick = trick
        # self.lead_player = lead_player
        # self.playerHasNo = playerHasNo
        # self.getAllUnknownHands()

        # self.observation_dict['zombie_count1'] = dummy_players[0].zombie_count / 12
        # self.observation_dict['zombie_count2'] = dummy_players[1].zombie_count / 12
        # self.observation_dict['zombie_count3'] = dummy_players[2].zombie_count / 12
        #
        # self.observation_dict['lead_player'] = lead_player

        observation = self.observation_dict.values()
        observation = list(observation)

        # make prediction:
        action = choose_action(model=q_model.model, observation=observation)
        hand_to_play = tabel.deck[action]

        # TODO: observation for prediction

        self.hand.remove(hand_to_play)
        return hand_to_play

        # pop the one with highest gain

        # pass  # This is just a placeholder, remove when real code goes here

    # def oneRound(self, startingTrick):
    #     gain = 0
    #     self.create_simulation_players()
    #     oneRound = Game(self.simulate_players)
    #     oneRound.deck.deck = self.simulated_undealed
    #     scoreDifference = oneRound.playOneRound(trick=copy.copy(self.trick),
    #                                             lead_player=copy.copy(self.lead_player),
    #                                             trickstartingTrick=copy.copy(startingTrick))
    #
    #     for i in range(0, len(self.dummy_players)):
    #         if i != self.dummy_p_idx:
    #             gain += (scoreDifference[self.dummy_p_idx] - scoreDifference[i])
    #     # return simulate_players
    #
    #     return gain

    # create simulated players and undealed hand
    # def create_simulation_players(self):
    #     unknownHands = copy.copy(self.unknownHands)
    #     random.shuffle(unknownHands)
    #     for i in range(0, len(self.dummy_players)):
    #         self.simulate_players[i].name = copy.copy(self.dummy_players[i].name)
    #         self.simulate_players[i].hand = copy.copy(self.dummy_players[i].hand)
    #         self.simulate_players[i].score = copy.copy(self.dummy_players[i].score)
    #         self.simulate_players[i].zombie_count = copy.copy(self.dummy_players[i].zombie_count)
    #         # test = copy.deepcopy(self.dummy_players)
    #     # self.simulate_players = test
    #     # for i in range(0, len(self.dummy_players)):
    #     j = 0
    #     while j < len(self.dummy_players):
    #         if j != self.dummy_p_idx:
    #             # length = len(self.dummy_players[i].hand)
    #             # a = unknownHands[0:length]
    #             # self.simulate_players[i].hand = a
    #             # unknownHands = unknownHands[length:]
    #
    #             length = len(self.dummy_players[j].hand)
    #             self.simulate_players[j].hand.clear()
    #             count = 0
    #             while self.playerHasNo[j][unknownHands[0][0]] and length > 0:
    #                 count = count + 1
    #                 if count > len(unknownHands):
    #                     unknownHands = copy.copy(self.unknownHands)
    #                     break
    #                 unknownHands.append(unknownHands.pop(0))
    #             if count > len(unknownHands):
    #                 j = 0
    #                 continue
    #             a = unknownHands[0:length]
    #             self.simulate_players[j].hand = a
    #             unknownHands = unknownHands[length:]
    #             random.shuffle(unknownHands)
    #         j = j + 1
    #
    #     self.simulated_undealed = unknownHands
