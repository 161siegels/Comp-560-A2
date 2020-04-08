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

        current_line = line.rstrip()
        sections = current_line.split(sep="/")

        for element in sections:
            new_shot[next(shot_types_iterator)] = element

        shots.append(Shot(new_shot))

    return shots
    # input_type = list(inputs.keys())
    # type_iterator = iter(input_type)
    # current = next(type_iterator)
    #
    # for line in file:
    #
    #     if line.rstrip() == '':
    #         current = next(type_iterator)
    #         continue
    #
    #     inputs[current].append(line.rstrip())
    #
    # file.close()
    # return inputs
