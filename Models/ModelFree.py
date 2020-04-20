import random
from typing import List
from Models.Shot import Shot
import itertools
import statistics as stats
from Models.StateShots import StateShots
from Models.VisitedStates import VisitedStates

CHANGE_THRESHOLD = 0.001
STARTING_STATE = 'Fairway'


class ModelFree:

    def __init__(self, shots: List[Shot]):
        self.shots = shots
        self.origins = set([x.origin for x in shots])
        self.destinations = set([x.destination for x in shots])
        self.aims = set([x.aim for x in shots])
        self.state_aim_utilities = {}
        self.explore_probability = 1.0

    def learn(self):
        results = []
        i = 0
        while True:
            og_state_aim_utilities = self.state_aim_utilities.copy()
            empty_states = VisitedStates()

            # Start at Fairway if it's the first run, start somewhere random if not
            starting_state = STARTING_STATE if i == 0 else random.choice(list(self.origins))
            visited_states = self.getStateUtilities(starting_state, empty_states)

            # Add results to cumulative list of state utilities
            results += visited_states.states

            # Update state utilities
            self.updateAvgUtilities(results)

            # Check which states are still unknown
            unknown_aims = [(x.origin, x.aim) for x in self.shots if
                            (x.origin, x.aim) not in self.state_aim_utilities.keys()]
            i += 1

            if not self.metChangeThreshold(og_state_aim_utilities, i):
                break

        print("State/Action pairs:")

        for utility in {k: v for k, v in sorted(self.state_aim_utilities.items(), key=lambda item: item[1], reverse=True)}:
            print("\t" + str(utility[0]) + " / " + str(utility[1]) + ": " + str(self.state_aim_utilities[utility]))

        print("Still unknown: " + str(unknown_aims))
        print(str(i) + " runs")

    def metChangeThreshold(self, original_state_aim_utilities, iterations):
        og_utilities = list(original_state_aim_utilities.values())
        new_values = list(self.state_aim_utilities.values())
        unknown_aims = [(x.origin, x.aim) for x in self.shots if \
                        (x.origin, x.aim) not in self.state_aim_utilities.keys()]

        # Continues if there is a newly discovered state,
        # or the change threshold was surpassed,
        # or there are still discovered states
        return len(original_state_aim_utilities) != len(self.state_aim_utilities) or \
               abs(sum([x[0] - x[1] for x in zip(new_values, og_utilities)])) >= CHANGE_THRESHOLD or \
               len(unknown_aims) > 0

    def getStateUtilities(self, starting_state, visited_states):
        possible_aims = [x.aim for x in self.shots if x.origin == starting_state]
        known_aim_utilities = [x for x in self.state_aim_utilities.keys() if x[0] == starting_state]
        chosen_aim = None

        # if we random number less than explore probability
        if random.random() < self.explore_probability or len(known_aim_utilities) == 0:
            # get a list of options that have not been discovered
            unknown_aims = list(set([x for x in possible_aims if x not in [y[1] for y in known_aim_utilities]]))

            # if there are still undiscovered states, choose a random state from the undiscovered ones
            chosen_aim = random.choice(unknown_aims) if len(unknown_aims) > 0 else random.choice(possible_aims)
            self.explore_probability -= 0.01

        # If we are exploiting, we choose the aim with the lowest utility at the state
        else:
            best_utility = 100000
            for aim in known_aim_utilities:
                if self.state_aim_utilities[aim] < best_utility:
                    best_utility = self.state_aim_utilities[aim]
                    chosen_aim = aim[1]

        possible_shots = [x for x in self.shots if x.origin == starting_state and x.aim == chosen_aim]
        destination_probabilities = list(itertools.accumulate([float(x.true_probability) for x in possible_shots]))
        chosen_shot = random.choices(possible_shots, cum_weights=destination_probabilities)[0]

        visited_states.states.append(StateShots(chosen_shot.origin, chosen_shot.aim))
        visited_states.incrememntAllStates()

        # Stop if we've reached "In", keep going if not
        return visited_states if self.endingState(chosen_shot.destination) \
            else self.getStateUtilities(chosen_shot.destination, visited_states=visited_states)

    def updateAvgUtilities(self, visited_states):
        for s in visited_states:
            self.state_aim_utilities[(s.state, s.aim)] = \
                stats.mean([x.shots for x in visited_states if x.state == s.state and x.aim == s.aim])

    def endingState(self, state):
        return state == 'In'

    def __repr__(self):
        return "Unique origins:\n\t" + str(self.origins) + "\nUnique Destinations:\n\t" + str(self.destinations) + \
               "\nUnique aims:\n\t" + str(self.aims) + "\nShots:\n" + str(self.shots)
