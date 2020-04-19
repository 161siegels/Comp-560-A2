import random
from typing import List
from Models.Shot import Shot
import itertools
import statistics as stats

from Models.StateShots import StateShots
from Models.VisitedStates import VisitedStates


class ModelFree:

    def __init__(self, shots: List[Shot]):
        self.shots = shots
        self.origins = set([x.origin for x in shots])
        self.destinations = set([x.destination for x in shots])
        self.aims = set([x.aim for x in shots])
        self.state_aim_utilities = {}

    def controller(self):
        for i in range(100):
            empty_states = VisitedStates()
            visited_states = self.getStateUtilities(random.choice(list(self.origins)), empty_states)
            self.updateAvgUtilities(visited_states)
        print(self.state_aim_utilities)

    def getStateUtilities(self, starting_state, visited_states):
        possible_aims = [x.aim for x in self.shots if x.origin == starting_state]
        chosen_aim = random.choice(possible_aims)
        possible_shots = [x for x in self.shots if x.origin == starting_state and x.aim == chosen_aim]
        destination_probabilities = list(itertools.accumulate([float(x.true_probability) for x in possible_shots]))
        chosen_shot = random.choices(possible_shots, cum_weights=destination_probabilities)[0]

        visited_states.visited_states.append(StateShots(chosen_shot.origin, chosen_shot.aim))
        visited_states.incrememntAllStates()

        if self.endingState(chosen_shot.destination):
            return visited_states
        else:
            return self.getStateUtilities(chosen_shot.destination, visited_states=visited_states)

    def updateAvgUtilities(self, visited_states):
        for s in visited_states.visited_states:
            if (s.state, s.aim) not in self.state_aim_utilities.keys():
                self.state_aim_utilities[(s.state, s.aim)] = \
                    stats.mean([x.shots for x in visited_states.visited_states if x.state == s.state and x.aim == s.aim])

    def endingState(self, state) -> bool:
        return True if state == 'In' else False

    def __repr__(self):
        return "Unique origins:\n\t" + str(self.origins) + "\nUnique Destinations:\n\t" + str(self.destinations) + \
              "\nUnique aims:\n\t" + str(self.aims) + "\nShots:\n" + str(self.shots)
