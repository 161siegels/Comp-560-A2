from Models.Shot import Shot


def read_from_file(file_name: str):

    file = open(file_name, mode="r")
    shots = []

    shot_types = [
        "origin", "aim", "destination", "true_probability"
    ]

    for line in file:
        
        shot_types_iterator = iter(shot_types)
        new_shot = {}

        sections = line.rstrip().split(sep="/")

        for element in sections:
            new_shot[next(shot_types_iterator)] = element

        shots.append(Shot(new_shot))

    return shots
