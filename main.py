from Models.InitialModel import InitialModel
from Models.ModelFree import ModelFree
from Startup.FileReader import read_from_file
from Startup.GetFileName import get_file_name


filename = get_file_name()
shots = read_from_file(filename)


def main():
    print("Model Free:")
    runModelFree()
    print("Model Based:")
    runModelBased()


def runModelBased():
    initial_model = InitialModel(shots)
    print(initial_model)


def runModelFree():
    model_free = ModelFree(shots)
    output = model_free.learn()
    print(output)


if __name__ == '__main__':
    main()
