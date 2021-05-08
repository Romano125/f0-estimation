import os
import soundfile as sf

from .directories import create_processed_directories
from constants.common import VEPRAD_LAB_DIRECTORY, VEPRAD_TXT_DIRECTORY, VEPRAD_WAV_DIRECTORY, PROCESSED_WORDS_DIRECTORY, PROCESSED_SOUNDS_BEGIN_DIRECTORY, PROCESSED_SOUNDS_MIDDLE_DIRECTORY, PROCESSED_SOUNDS_END_DIRECTORY, SOUNDS


def find(lab_line, index):
    lab_line_parsed = lab_line[index].split(' ')
    return lab_line_parsed[0], lab_line_parsed[1]


def save_cutted_piece(start_time, end_time, wav_file, file_path):
    data, samplerate = sf.read(wav_file)

    # cut word from original .wav file and save it into new one
    if start_time and end_time:
        cut_start = int(start_time) * 0.0016
        cut_end = int(end_time) * 0.0016
        new_data = data[int(cut_start): int(cut_end)]
        sf.write(file_path, new_data, samplerate)


def cut_sounds(sound, lab, txt_words, wav_file, file_name):
    lab_file_position = 1
    is_begin_sound_found = False
    is_middle_sound_found = False
    is_end_sound_found = False
    time = {}
    '''
    TODO
    {
        autocesta: {
            a: {
                begin: {t1: 45, t2: 50}
                end:
            }
        },
        auto: {
            a: {
                begin:
                middle:
                end:
            }
        },
    }
    '''

    # u petlji pronalazim početak i završetak zvučnog glasa pomičući se istovremeno kroz .lab (sadrži trajanje glasa) i .txt_words datoteku
    for word in txt_words:
        if is_begin_sound_found == True and is_middle_sound_found == True and is_end_sound_found == True:
            break

        word_length = len(word)
        if word_length > 1:
            for i, letter in enumerate(word):
                sound_start, sound_end = find(lab, lab_file_position)
                if letter == sound and i == 0 and is_begin_sound_found == False:
                    time.update({f'{sound}_begin_start_time': sound_start})
                    time.update({f'{sound}_begin_end_time': sound_end})
                    is_begin_sound_found = True
                elif letter == sound and (i > 0 and i < word_length - 1) and is_middle_sound_found == False:
                    time.update({f'{sound}_middle_start_time': sound_start})
                    time.update({f'{sound}_middle_end_time': sound_end})
                    is_middle_sound_found = True
                elif letter == sound and i >= word_length - 1 and is_end_sound_found == False:
                    time.update({f'{sound}_end_start_time': sound_start})
                    time.update({f'{sound}_end_end_time': sound_end})
                    is_end_sound_found = True
                lab_file_position += 1
        else:
            lab_file_position += 1

    save_cutted_piece(time.get(f'{sound}_begin_start_time'), time.get(f'{sound}_begin_end_time'), wav_file,
                      f'{PROCESSED_SOUNDS_BEGIN_DIRECTORY}/{file_name}_{sound}.wav')
    save_cutted_piece(time.get(f'{sound}_middle_start_time'), time.get(f'{sound}_middle_end_time'), wav_file,
                      f'{PROCESSED_SOUNDS_MIDDLE_DIRECTORY}/{file_name}_{sound}.wav')
    save_cutted_piece(time.get(f'{sound}_end_start_time'), time.get(f'{sound}_end_end_time'), wav_file,
                      f'{PROCESSED_SOUNDS_END_DIRECTORY}/{file_name}_{sound}.wav')


def cut_word(lab_lines, word_first_index, word_last_index, wav_file, word, file_name):
    word_start_t = lab_lines[word_first_index].split(' ')[0]
    word_end_t = lab_lines[word_last_index].split(' ')[1]

    save_cutted_piece(word_start_t, word_end_t, wav_file,
                      f'{PROCESSED_WORDS_DIRECTORY}/{file_name}_{word}.wav')


def speech_parametrization():
    create_processed_directories()

    lab_directory = os.listdir(VEPRAD_LAB_DIRECTORY)
    txt_directory = os.listdir(VEPRAD_TXT_DIRECTORY)
    wav_directory = os.listdir(VEPRAD_WAV_DIRECTORY)

    lab_directory.sort()
    txt_directory.sort()
    wav_directory.sort()

    # passes through the veprad directories in parallel and cut sounds by position in the word (begin, middle, end)
    for file in lab_directory:
        file_name = file.split('.')[0]
        lab_file = open(
            f'{VEPRAD_LAB_DIRECTORY}/{file_name}.lab', 'r')
        txt_file = open(
            f'{VEPRAD_TXT_DIRECTORY}/{file_name}.txt', 'r')
        wav_file_path = f'{VEPRAD_WAV_DIRECTORY}/{file_name}.wav'

        lab_lines = lab_file.read().splitlines()
        txt_words = [line.split(' ') for line in txt_file.readlines()][0]

        lab_file_position = 1  # because we skip first line in .lab file
        for word in txt_words:
            word_length = len(word)
            cut_word(lab_lines, lab_file_position, lab_file_position +
                     word_length, wav_file_path, word, file_name)

        for sound in SOUNDS:
            cut_sounds(sound, lab_lines, txt_words,
                       wav_file_path, file_name)

        lab_file.close()
        txt_file.close()
