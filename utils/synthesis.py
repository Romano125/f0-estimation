import os
import soundfile as sf
import pyworld as pw
import numpy as np

from .directories import create_synthesis_directories, create_plots_synthesis_directories, create_plots_directories
from .plotting import savefig
from constants.common import PROCESSED_WORDS_DIRECTORY, PROCESSED_SOUNDS_DIRECTORY, PLOTS_SYNTHESIS_WORDS_DIRECTORY, PLOTS_SOUNDS_DIRECTORY, SYNTHESIS_WORDS_DIRECTORY, SYNTHESIS_SOUNDS_DIRECTORY, VEPRAD_TXT_DIRECTORY, SOUNDS


def sound_synthesis(sound, sound_position, word, file_name):
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

        synthesized_sound = pw.synthesize(
            f0_mask, spectral_envelop, aperiodicity, samplerate, pw.default_frame_period)

        sf.write(
            f'{SYNTHESIS_SOUNDS_DIRECTORY}/{sound_position}/{file_name}_{word}_{sound}.wav', synthesized_sound, samplerate)
        savefig(
            f'{PLOTS_SOUNDS_DIRECTORY}/{sound_position}/synthesis_comparison/{file_name}_{word}_{sound}.png', [data, synthesized_sound], sound)


def process_sound(txt_words, sound, file_name):
    for word in txt_words:
        sound_synthesis(sound, 'begin', word, file_name)
        sound_synthesis(sound, 'middle', word, file_name)
        sound_synthesis(sound, 'end', word, file_name)


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


def synthesis():
    create_synthesis_directories()
    create_plots_synthesis_directories()
    create_plots_directories()

    txt_directory = os.listdir(VEPRAD_TXT_DIRECTORY)
    txt_directory.sort()

    for file in txt_directory:
        file_name, _ = file.split('.')
        txt_file = open(
            f'{VEPRAD_TXT_DIRECTORY}/{file}', 'r')
        txt_words = [line.split(' ') for line in txt_file.readlines()][0]

        for word in txt_words:
            word_synthesis(word, file_name)

        for sound in SOUNDS:
            process_sound(txt_words, sound, file_name)
