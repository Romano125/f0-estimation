import os

from utils.acoustic_parameters import acoustic_parameters_analysis
from utils.data import speech_parametrization
from utils.synthesis import synthesis


def main():
    if os.path.isdir('plots') == False:
        os.mkdir('plots')

    speech_parametrization()
    acoustic_parameters_analysis()
    synthesis()


if __name__ == '__main__':
    main()
