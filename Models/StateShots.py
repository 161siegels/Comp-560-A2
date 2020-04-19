class StateShots:

    def __init__(self, state):
        self.state = state
        self.shots = 0

    def incrementShot(self):
        self.shots += 1

    def __repr__(self):
        return "State: " + self.state + ", shots: " + str(self.shots)