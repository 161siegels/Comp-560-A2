from Models.InitialModel import InitialModel
from Startup.FileReader import read_from_file
from Startup.GetFileName import get_file_name


def main():
    filename = get_file_name()
    shots = read_from_file(filename)
    initial_model = InitialModel(shots)
    print(initial_model)


if __name__ == '__main__':
    main()
