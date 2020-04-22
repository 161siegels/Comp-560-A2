from typing import List

from Models.StateShots import StateShots


class VisitedStates:

    def __init__(self):
        self.states: List[StateShots] = []

    def incrementAllStates(self):
        for s in self.states:
            s.incrementShot()

    def __repr__(self):
        return "Visited States: " + str([str(x) for x in self.states])
