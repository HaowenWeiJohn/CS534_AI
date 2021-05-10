from Assignment3.game2 import *
from Assignment3 import tabel



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
        self.create_observation_dict()

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

        gain_list = list(np.zeros(len(allPossibleHands)))

        print("-", self.name + "(" + str(self.score) + ")(Z" + str(self.zombie_count) + ")", "sees", trick)

        self.dummy_p_idx = dummy_p_idx
        self.dummy_players = dummy_players
        self.simulate_players = copy.deepcopy(dummy_players)
        self.undealed = undealed
        self.trick = trick
        self.lead_player = lead_player
        self.playerHasNo = playerHasNo
        allUnknownHnads = self.getAllUnknownHands()

        self.observation_dict = self.observation_dict.fromkeys(self.observation_dict, 0) # this will be the played hand value

        for hand in self.hand:
            self.observation_dict[hand] = 0.5

        for possibleHand in allPossibleHands:
            self.observation_dict[possibleHand] = 0.7

        for unknownHand in allUnknownHnads:
            self.observation_dict[unknownHand] = 0.2

        for seetrick in trick:
            self.observation_dict[seetrick] = 1



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
        action = choose_action(model=q_model.model, possibleHands=allPossibleHands,observation=observation)
        hand_to_play = tabel.deck[action]
        q_model.memory.observations.append(observation)
        q_model.memory.actions.append(action)

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
