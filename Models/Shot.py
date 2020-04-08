class Shot:

    def __init__(self, new_shot):
        self.origin = new_shot["origin"]
        self.aim = new_shot["aim"]
        self.destination = new_shot["destination"]
        self.true_probability = new_shot["true_probability"]

    def __repr__(self):
        return "Shot: \n\torigin = " + str(self.origin) + "\n\taim = " + str(self.aim) + "\n\tdestination = " +\
               str(self.destination) + "\n\ttrue probability = " + str(self.true_probability) + "\n"
