import os
import soundfile as sf
import pyworld as pw
import numpy as np

from .directories import create_synthesis_directories, create_plots_synthesis_directories, create_plots_directories
from .plotting import savefig, plot_f0, plot_f0_comparison
from constants.common import PROCESSED_WORDS_DIRECTORY, PROCESSED_SOUNDS_DIRECTORY, PLOTS_SYNTHESIS_WORDS_DIRECTORY, PLOTS_SOUNDS_DIRECTORY, PLOTS_SOUNDS_F0_COMPARISON_DIRECTORY, SYNTHESIS_WORDS_DIRECTORY, SYNTHESIS_SOUNDS_DIRECTORY, VEPRAD_TXT_DIRECTORY, VEPRAD_WAV_DIRECTORY, SOUNDS


def process_acoustic_parameters(sound, sound_position, file_name):
    f0_max = 0
    is_processed = False
    file = f'{PROCESSED_SOUNDS_DIRECTORY}/{sound_position}/{file_name}_{sound}.wav'
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

        synthesized_sound = pw.synthesize(
            f0_mask, spectral_envelop, aperiodicity, samplerate, pw.default_frame_period)

        sf.write(
            f'{SYNTHESIS_SOUNDS_DIRECTORY}/{sound_position}/{file_name}_{sound}.wav', synthesized_sound, samplerate)

        plot_f0(sound, sound_position, timeaxis, f0, f0_mask,
                f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/f0/{file_name}_{sound}.png')
        savefig(
            f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/synthesis_comparison/{file_name}_{sound}.png', [data, synthesized_sound], sound)
        savefig(
            f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/spectral_envelop/{file_name}_{sound}.png', [spectral_envelop], sound)
        savefig(
            f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/aperiodicity/{file_name}_{sound}.png', [aperiodicity], sound, log=False)
        f0_max = np.max(f0)
        is_processed = True
    return f0_max, is_processed


def estimate(sound, file_name):
    is_f0_begin_found = False
    is_f0_middle_found = False
    is_f0_end_found = False
    f0_begin = 0
    f0_middle = 0
    f0_end = 0

    f0_begin, is_f0_begin_found = process_acoustic_parameters(
        sound, 'begin', file_name)
    f0_middle, is_f0_middle_found = process_acoustic_parameters(
        sound, 'middle', file_name)
    f0_end, is_f0_end_found = process_acoustic_parameters(
        sound, 'end', file_name)

    if is_f0_begin_found and is_f0_middle_found and is_f0_end_found:
        plot_f0_comparison(sound, f0_begin, f0_middle, f0_end,
                           f'{PLOTS_SOUNDS_F0_COMPARISON_DIRECTORY}/{file_name}_{sound}.png')


def word_synthesis(word, file_name):
    if os.path.exists(f'{PROCESSED_WORDS_DIRECTORY}/{file_name}_{word}.wav'):
        data, samplerate = sf.read(
            f'{PROCESSED_WORDS_DIRECTORY}/{file_name}_{word}.wav')

        f0, timeaxis = pw.harvest(data, samplerate)
        f0_mask = pw.stonemask(data, f0, timeaxis, samplerate)
        spectral_envelop = pw.cheaptrick(data, f0_mask, timeaxis, samplerate)
        aperiodicity = pw.d4c(data, f0_mask, timeaxis, samplerate)

        synthesized_word = pw.synthesize(
            f0_mask, spectral_envelop, aperiodicity, samplerate, pw.default_frame_period)

        sf.write(f'{SYNTHESIS_WORDS_DIRECTORY}/{file_name}_{word}_default.wav',
                 synthesized_word, samplerate)
        savefig(f'{PLOTS_SYNTHESIS_WORDS_DIRECTORY}/{file_name}_{word}_default.png',
                [data, synthesized_word], word)

        synthesized_word = pw.synthesize(
            f0_mask, spectral_envelop, aperiodicity, samplerate, 3.0)

        sf.write(f'{SYNTHESIS_WORDS_DIRECTORY}/{file_name}_{word}_3.wav',
                 synthesized_word, samplerate)
        savefig(f'{PLOTS_SYNTHESIS_WORDS_DIRECTORY}/{file_name}_{word}_3.png',
                [data, synthesized_word], word)

        synthesized_word = pw.synthesize(
            f0_mask, spectral_envelop, aperiodicity, samplerate, 20.0)

        sf.write(f'{SYNTHESIS_WORDS_DIRECTORY}/{file_name}_{word}_20.wav',
                 synthesized_word, samplerate)
        savefig(f'{PLOTS_SYNTHESIS_WORDS_DIRECTORY}/{file_name}_{word}_20.png',
                [data, synthesized_word], word)


def estimation():
    create_synthesis_directories()
    create_plots_synthesis_directories()
    create_plots_directories()

    txt_directory = os.listdir(VEPRAD_TXT_DIRECTORY)
    wav_directory = os.listdir(VEPRAD_WAV_DIRECTORY)

    txt_directory.sort()
    wav_directory.sort()

    current_index = 0
    for file in wav_directory:
        txt_file = open(
            f'{VEPRAD_TXT_DIRECTORY}/{txt_directory[current_index]}', 'r')
        txt_words = [line.split(' ') for line in txt_file.readlines()][0]

        file_name, _ = file.split('.')
        for word in txt_words:
            word_synthesis(word, file_name)

        for sound in SOUNDS:
            estimate(sound, file_name)
