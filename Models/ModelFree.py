import random
from typing import List
from Models.Shot import Shot
import itertools

from Models.StateShots import StateShots
from Models.VisitedStates import VisitedStates


class ModelFree:

    def __init__(self, shots: List[Shot]):
        self.shots = shots
        self.origins = set([x.origin for x in shots])
        self.destinations = set([x.destination for x in shots])
        self.aims = set([x.aim for x in shots])

        self.state_action_pairs = []

        for origin in self.origins:
            for aim in self.aims:
                self.state_action_pairs.append({
                    "origin": origin,
                    "aim": aim,
                    "utility": -1
                })

        self.visited_states = VisitedStates()
        print(self.modelFree('Fairway'))

    def modelFree(self, starting_state):
        possible_aims = [x.aim for x in self.shots if x.origin == starting_state]
        chosen_aim = random.choice(possible_aims)
        possible_shots = [x for x in self.shots if x.origin == starting_state and x.aim == chosen_aim]
        destination_probabilities = list(itertools.accumulate([float(x.true_probability) for x in possible_shots]))
        # print(destination_probabilities)
        chosen_shot = random.choices(possible_shots, cum_weights=destination_probabilities)[0]
        self.visited_states.visited_states.append(StateShots(starting_state))
        self.visited_states.incrememntAllStates()

        if self.endingState(chosen_shot.destination):
            print(chosen_shot)
            return self.visited_states
        else:
            print(self.visited_states)
            self.modelFree(chosen_shot.destination)

    def endingState(self, state) -> bool:
        return True if state == 'In' else False

    def __repr__(self):
        return "Unique origins:\n\t" + str(self.origins) + "\nUnique Destinations:\n\t" + str(self.destinations) + \
              "\nUnique aims:\n\t" + str(self.aims) + "\nShots:\n" + str(self.shots)
