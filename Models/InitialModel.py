from typing import List

from Models.Shot import Shot


class InitialModel:

    def __init__(self, shots: List[Shot]):
        self.shots = shots
        self.origins = set([x.origin for x in shots])
        self.destinations = set([x.destination for x in shots])
        self.aims = set([x.aim for x in shots])

    def __repr__(self):
        return "Unique origins:\n\t" + str(self.origins) + "\nUnique Destinations:\n\t" + str(self.destinations) + \
               "\nUnique aims:\n\t" + str(self.aims) + "\nShots:\n" + str(self.shots)
