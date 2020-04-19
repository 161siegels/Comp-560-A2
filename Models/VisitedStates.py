from typing import List

from Models.StateShots import StateShots


class VisitedStates:

    def __init__(self):
        self.visited_states: List[StateShots] = []

    def incrememntAllStates(self):
        for s in self.visited_states:
            s.incrementShot()

    def __repr__(self):
        return "Visited States: " + str([str(x) for x in self.visited_states])
