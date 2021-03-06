from typing import List

from Models.Shot import Shot
import pandas as pd
import numpy as np
import itertools


class InitialModel:

    def __init__(self, shots: List[Shot]):
        self.shots = shots
        self.origins = set([x.origin for x in shots])
        self.destinations = set([x.destination for x in shots])
        self.aims = set([x.aim for x in shots])

        origin_list = list(itertools.chain.from_iterable(itertools.repeat(x, len(self.aims)) for x in list(self.origins)))
        tuples = (zip(origin_list, np.array(list(self.aims)*len(self.origins))))

        self.visits_df = pd.DataFrame(data = np.tile(np.array(0),(36,6)), index = pd.MultiIndex.from_tuples(tuples, names=['origins', 'aims']), columns=self.destinations)
        self.reward = {}
        self.utility = {}
        for origin in self.origins:
            self.utility[origin] = 0
            self.reward[origin]=1
        for destination in self.destinations:
            self.utility[destination] = 0
            if destination == 'In' :
                self.reward[destination] = 0
            else:
                self.reward[destination] = 1

        self.model_based(self.utility.copy(), 1, 0.95, 0.001,0)

    # threshold is the convergence threshold for utility. If a state's utility changes by more than this then keep learning
    # iterations checks how many iterations in a row the utility has changed by less than threshold. Need 3 for us
    # to deem convergence
    def model_based(self,prev_utility,explore_probability,discount_value,threshold,iterations):
        new_utility = self.simulate(explore_probability,discount_value)
        rerun = False
        for state in prev_utility:
            if (np.abs(prev_utility[state]-new_utility[state]) > threshold):
                rerun = True
                iterations = 0
                break
        if not rerun:
            iterations+=1
        # Want to run the simulation at least 10 times
        # Decrease explore probability by 1% each time
        if rerun or iterations<3 or explore_probability>(.99**10):
            self.model_based(new_utility.copy(), explore_probability*.99, discount_value, threshold,iterations)


    def simulate(self, explore_probability, discount_value):
        cur_state = 'Fairway'
        while cur_state != 'In':
            action = ''
            if np.random.rand() >= explore_probability:
                action = self.exploit(cur_state)[0]
            else:
                action = self.explore(cur_state)
            shot_outcomes = [x for x in self.shots if x.origin == cur_state and x.aim == action]
            rand_number = np.random.rand()
            count = 0
            chosen_path = {}
            for shot in shot_outcomes:
                if rand_number >= count+float(shot.true_probability):
                    count = count + float(shot.true_probability)
                else:
                    chosen_path = shot
                    break
            self.visits_df.at[(cur_state,chosen_path.aim),chosen_path.destination] += 1
            self.utility[cur_state] = self.reward[cur_state] + discount_value*self.exploit(cur_state)[1]
            cur_state = chosen_path.destination
        return self.utility

    def explore(self, cur_state):
        aim_options = np.unique([x.aim for x in self.shots if x.origin == cur_state])
        min_visited = self.visits_df.sum(axis=1)[cur_state][aim_options].min()
        rand_index = np.random.choice([i for i, j in enumerate(self.visits_df.sum(axis=1)[cur_state][aim_options]) if j == min_visited])
        return str(self.visits_df.sum(axis=1)[cur_state][aim_options].index[rand_index])
        # return str(self.visits_df.sum(axis=1)[cur_state][aim_options].idxmin())

    def exploit(self, cur_state):
        aim_options = np.unique([x.aim for x in self.shots if x.origin == cur_state])

        # stores the best aim option and the value associated with it
        best_option = ('', np.inf)
        for aim in aim_options:
            possible_destinations = np.unique([x.destination for x in self.shots if x.origin == cur_state and x.aim==aim])
            aim_value = 0
            for destination in possible_destinations:
                if self.visits_df.sum(axis=1)[cur_state][aim] == 0:
                    aim_value += 0
                else:
                    aim_value += (self.visits_df[destination][cur_state][aim]/self.visits_df.sum(axis=1)[cur_state][aim])*self.utility[destination]
            if aim_value < best_option[1]:
                best_option = (aim, aim_value)
        return best_option

    def policy(self):
        print(self.utility)
        policyString=''
        for state in self.utility:
            if state != 'In':
                policyString += 'In state: ' + state + " the recommended shot type is: " + self.exploit(state)[0] +'\n'
        policyString += 'Here is the probability transition table ' \
                        '(the left side indicates the origin and aim, column shows destination):\n'
        return policyString + self.visits_df.div(self.visits_df.sum(axis=1), axis=0).dropna().to_string()
    def __repr__(self):
        return self.policy()
        #return "Unique origins:\n\t" + str(self.origins) + "\nUnique Destinations:\n\t" + str(self.destinations) + \
        #       "\nUnique aims:\n\t" + str(self.aims) + "\nShots:\n" + str(self.shots)
