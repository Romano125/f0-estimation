import os
import pysptk
import numpy as np
import pyworld as pw
import soundfile as sf

from .directories import create_plots_directories
from .plotting import savefig, plot_f0, plot_f0_comparison
from constants.common import PROCESSED_SOUNDS_DIRECTORY, PLOTS_SOUNDS_DIRECTORY, PLOTS_SOUNDS_F0_COMPARISON_DIRECTORY, VEPRAD_TXT_DIRECTORY, SOUNDS


def arange(length, step):
    array = [0] * length
    for i in range(length):
        array[i] = i * step
    return array


def get_average_f0_by_sound_position(sound, sound_position):
    processed_sounds_directory = f'{PROCESSED_SOUNDS_DIRECTORY}/{sound_position}'

    if processed_sounds_directory == None:
        return 0

    f0_array = []
    for file_name in os.listdir(processed_sounds_directory):
        file = f'{processed_sounds_directory}/{file_name}'
        if file_name.endswith(f'_{sound}.wav') and os.path.exists(file):
            data, samplerate = sf.read(file)
            f0, _ = pw.harvest(data, samplerate)
            f0_array.append(np.max(f0))
    return sum(f0_array) / len(f0_array) if len(f0_array) else 0


def process_acoustic_parameters(sound, sound_position, word, file_name):
    file = f'{PROCESSED_SOUNDS_DIRECTORY}/{sound_position}/{file_name}_{word}_{sound}.wav'
    if os.path.exists(file):
        data, samplerate = sf.read(file)

        frame_period = 5  # ms
        hop_length = int(0.001 * samplerate * frame_period)

        f0_dio, timeaxis_dio = pw.dio(data, samplerate)
        f0, timeaxis = pw.harvest(
            data, samplerate, frame_period)
        f0_mask = pw.stonemask(data, f0, timeaxis, samplerate)
        spectral_envelop = pw.cheaptrick(data, f0_mask, timeaxis, samplerate)
        aperiodicity = pw.d4c(data, f0_mask, timeaxis, samplerate)

        f0_rapt = pysptk.sptk.rapt(
            data.astype(np.float32), samplerate, hop_length)

        f0_swipe = pysptk.sptk.swipe(
            data, samplerate, hop_length)

        plot_f0(sound,
                sound_position,
                [timeaxis, f0],
                [timeaxis_dio, f0_dio],
                [arange(len(f0_rapt), 0.005), f0_rapt],
                [arange(len(f0_swipe), 0.005), f0_swipe],
                f0_mask,
                f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/f0/{file_name}_{word}_{sound}.png')
        savefig(
            f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/spectral_envelop/{file_name}_{word}_{sound}.png', [spectral_envelop], sound)
        savefig(
            f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/aperiodicity/{file_name}_{word}_{sound}.png', [aperiodicity], sound, log=False)


def process_sound(txt_words, sound, file_name):
    for word in txt_words:
        process_acoustic_parameters(
            sound, 'begin', word, file_name)
        process_acoustic_parameters(
            sound, 'middle', word, file_name)
        process_acoustic_parameters(
            sound, 'end', word, file_name)


def compare_sounds_f0(sound):
    average_f0s = []
    sound_positions = ['begin', 'middle', 'end']

    for sound_position in sound_positions:
        average_f0s.append(
            get_average_f0_by_sound_position(sound, sound_position))

    plot_f0_comparison(sound, average_f0s[0], average_f0s[1], average_f0s[2],
                       f'{PLOTS_SOUNDS_F0_COMPARISON_DIRECTORY}/{sound}.png')


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
            compare_sounds_f0(sound)
