import os

from utils.data import speech_parametrization
from utils.estimation import estimation


def main():
    if os.path.isdir('plots') == False:
        os.mkdir('plots')

    speech_parametrization()
    estimation()


if __name__ == '__main__':
    main()
