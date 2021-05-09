import os
import soundfile as sf
import pyworld as pw
import numpy as np

from .directories import create_plots_directories
from .plotting import savefig, plot_f0, plot_f0_comparison
from constants.common import PROCESSED_SOUNDS_DIRECTORY, PLOTS_SOUNDS_DIRECTORY, PLOTS_SOUNDS_F0_COMPARISON_DIRECTORY, VEPRAD_TXT_DIRECTORY, SOUNDS


def process_acoustic_parameters(sound, sound_position, word, file_name):
    f0_max = 0
    is_processed = False
    file = f'{PROCESSED_SOUNDS_DIRECTORY}/{sound_position}/{file_name}_{word}_{sound}.wav'
    if os.path.exists(file):
        data, samplerate = sf.read(file)

        """
        f0_dio, timeaxis_dio = pw.dio(beg, samplerate, f0_floor=70.0, f0_ceil=800.0, channels_in_octave=3.0,
                                      frame_period=args.frame_period,
                                      speed=args.speed)
        """
        f0, timeaxis = pw.harvest(data, samplerate)
        f0_mask = pw.stonemask(data, f0, timeaxis, samplerate)
        spectral_envelop = pw.cheaptrick(data, f0_mask, timeaxis, samplerate)
        aperiodicity = pw.d4c(data, f0_mask, timeaxis, samplerate)

        plot_f0(sound, sound_position, timeaxis, f0, f0_mask,
                f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/f0/{file_name}_{word}_{sound}.png')
        savefig(
            f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/spectral_envelop/{file_name}_{word}_{sound}.png', [spectral_envelop], sound)
        savefig(
            f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/aperiodicity/{file_name}_{word}_{sound}.png', [aperiodicity], sound, log=False)
        f0_max = np.max(f0)
        is_processed = True
    return f0_max, is_processed


def process_sound(txt_words, sound, file_name):
    is_f0_begin_found = False
    is_f0_middle_found = False
    is_f0_end_found = False
    f0_begin = 0
    f0_middle = 0
    f0_end = 0

    for word in txt_words:
        f0_begin, is_f0_begin_found = process_acoustic_parameters(
            sound, 'begin', word, file_name)
        f0_middle, is_f0_middle_found = process_acoustic_parameters(
            sound, 'middle', word, file_name)
        f0_end, is_f0_end_found = process_acoustic_parameters(
            sound, 'end', word, file_name)

        # TODO: compare sounds from different words not the same
        if is_f0_begin_found and is_f0_middle_found and is_f0_end_found:
            plot_f0_comparison(sound, f0_begin, f0_middle, f0_end,
                               f'{PLOTS_SOUNDS_F0_COMPARISON_DIRECTORY}/{file_name}_{word}_{sound}.png')


def acoustic_parameters_analysis():
    create_plots_directories()

    txt_directory = os.listdir(VEPRAD_TXT_DIRECTORY)
    txt_directory.sort()

    for file in txt_directory:
        file_name, _ = file.split('.')
        txt_file = open(
            f'{VEPRAD_TXT_DIRECTORY}/{file}', 'r')
        txt_words = [line.split(' ') for line in txt_file.readlines()][0]

        for sound in SOUNDS:
            process_sound(txt_words, sound, file_name)
