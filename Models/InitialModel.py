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
        self.reward_df = self.visits_df.copy()
        self.utility = {}
        for origin in self.origins:
            self.utility[origin] = 0
        for destination in self.destinations:
            self.utility[destination] = 0
        # self.visits_df[destination][origin][aim]
        print(self.visits_df.sum(axis=1)['Fairway'].idxmin())
        #self.simulate()



    def simulate(self, explore_probability):
        cur_state = 'Fairway'
        while cur_state != 'In':
            # These are the options of shots given the current state
            action = ''
            if np.random.rand() > explore_probability:
                action = self.exploit(cur_state)
            else:
                action = self.explore(cur_state)


            options = [x for x in self.shots if x.origin == cur_state and x.aim=action]
            rand_number = np.random.rand()
            count = 0
            chosen_path = {}
            for shot in options:
                if rand_number + count > shot.true_probability:
                    count = count + shot.true_probability
                else:
                    chosen_path = shot
                    break
            

    def explore(self, cur_state):
        aim_options = [x.aim for x in self.shots if x.origin == cur_state]
        return self.visits_df.sum(axis=1)['Fairway'].idxmin()

    def exploit(self, cur_state):
        aim_options = [x.aim for x in self.shots if x.origin == cur_state]
        return [key for key in self.utility if all(self.utility[temp] <= self.utility[key] for temp in self.utility)]

    def __repr__(self):
        return "hello"
        #return "Unique origins:\n\t" + str(self.origins) + "\nUnique Destinations:\n\t" + str(self.destinations) + \
         #      "\nUnique aims:\n\t" + str(self.aims) + "\nShots:\n" + str(self.shots)
