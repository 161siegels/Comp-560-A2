class StateShots:

    def __init__(self, state, aim):
        self.state = state
        self.aim = aim
        self.shots = 0

    def incrementShot(self):
        self.shots += 1

    def __repr__(self):
        return "State: " + self.state + ", aim: " + self.aim + ", shots: " + str(self.shots)
