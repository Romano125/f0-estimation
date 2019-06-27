#  Zvučni su glasovi svi samoglasnici ( a, e, i, o, u), svi zvonačnici ( j, l, lj, m, n, nj, r, v) i neki šumnici (b, d, g, z, ž, dž, đ)
import os
import soundfile as sf
import argparse
from shutil import rmtree

parser = argparse.ArgumentParser()


def find(lab, pos):
    lab_arr = lab[pos].split(" ")
    return lab_arr[0], lab_arr[1]


def cut_word(lab, beg, end, wav_file, word):
    file = wav_file.split('.')
    name = file[0].split('/')

    word_beg = lab[beg].split(" ")
    t_beg = word_beg[0]
    word_end = lab[end].split(" ")
    t_end = word_end[1]

    new, fs = sf.read(wav_file)

    # režem riječ iz originalnog .wav file-a i spremam ju u .wav datoteku
    if t_beg and t_end:
        start = int(t_beg) * 0.0016
        ending = int(t_end) * 0.0016
        new_arr = new[int(start): int(ending)]
        sf.write(f"rijeci_wav/{word}_{name[1]}.wav", new_arr, fs)


def get_values(letter, lab, txt, wav_file):
    i = 0
    j = 1
    time = {}
    fb = 0
    fm = 0
    fe = 0

    file = wav_file.split('.')
    name = file[0].split('/')

    # u petlji pronalazim početak i završetak zvučnog glasa pomičući se istovremeno kroz .lab (sadrži trajanje glasa) i .txt datoteku
    while i != len(txt):
        pos = 0
        if fb == 1 and fm == 1 and fe == 1:
            break

        if len(txt[i]) > 1:
            for k in txt[i]:
                st, en = find(lab, j)  # find funkcija mi vraća početak i završetak glasa
                if k == letter and pos == 0 and fb == 0:
                    time.update({f'{letter}_beg_start': st})
                    time.update({f'{letter}_beg_end': en})
                    fb = 1
                elif k == letter and (pos > 0 and pos < len(txt[i]) - 1) and fm == 0:
                    time.update({f'{letter}_mid_start': st})
                    time.update({f'{letter}_mid_end': en})
                    fm = 1
                elif k == letter and pos >= len(txt[i]) - 1 and fe == 0:
                    time.update({f'{letter}_end_start': st})
                    time.update({f'{letter}_end_end': en})
                    fe = 1
                pos += 1
                j += 1
        else:
            j += 1

        i += 1

    print("{} na početku => {} {}".format(letter, time.get(f'{letter}_beg_start'), time.get(f'{letter}_beg_end')))
    print("{} u sredini => {} {}".format(letter, time.get(f'{letter}_mid_start'), time.get(f'{letter}_mid_end')))
    print("{} na kraju => {} {}".format(letter, time.get(f'{letter}_end_start'), time.get(f'{letter}_end_end')))

    new, fs = sf.read(wav_file)

    # režem zvučne glasove iz originalnog .wav file-a i spremam ih u .wav datoteke
    if time.get(f'{letter}_beg_start') and time.get(f'{letter}_beg_end'):
        start_beg = int(time.get(f'{letter}_beg_start')) * 0.0016
        end_beg = int(time.get(f'{letter}_beg_end')) * 0.0016
        new_arr_beg = new[int(start_beg): int(end_beg)]
        sf.write(f"zvucni_glasovi_wav/novi_{letter}_beg_{name[1]}.wav", new_arr_beg, fs)
    if time.get(f'{letter}_mid_start') and time.get(f'{letter}_mid_end'):
        start_mid = int(time.get(f'{letter}_mid_start')) * 0.0016
        end_mid = int(time.get(f'{letter}_mid_end')) * 0.0016
        new_arr_mid = new[int(start_mid): int(end_mid)]
        sf.write(f"zvucni_glasovi_wav/novi_{letter}_mid_{name[1]}.wav", new_arr_mid, fs)
    if time.get(f'{letter}_end_start') and time.get(f'{letter}_end_end'):
        start_end = int(time.get(f'{letter}_end_start')) * 0.0016
        end_end = int(time.get(f'{letter}_end_end')) * 0.0016
        new_arr_end = new[int(start_end): int(end_end)]
        sf.write(f"zvucni_glasovi_wav/novi_{letter}_end_{name[1]}.wav", new_arr_end, fs)


def main(args):
    if os.path.isdir('zvucni_glasovi_wav'):
        rmtree('zvucni_glasovi_wav')
    os.mkdir('zvucni_glasovi_wav')

    if os.path.isdir('rijeci_wav'):
        rmtree('rijeci_wav')
    os.mkdir('rijeci_wav')

    dir_lab = os.listdir('lab')
    dir_txt = os.listdir('txt')
    dir_wav = os.listdir('wav')
    num_files = 0

    # prolazim kroz sve datoteke i iz njih režem samo zvučne glasove na početku, u sredini i na kraju riječi
    while num_files != len(dir_lab):
        lab = open(f'lab/{dir_lab[num_files]}', "r")
        txt = open(f'txt/{dir_txt[num_files]}', "r")
        str_wav = f'wav/{dir_wav[num_files]}'

        lab_lines = lab.read().splitlines()
        txt_lines = txt.readlines()

        for i in range(len(txt_lines)):
            txt_arr = txt_lines[i].split(" ")

        i = 0
        j = 1
        while i != len(txt_arr) - 1:
            cut_word(lab_lines, j, j + len(txt_arr[i]), str_wav, txt_arr[i])  # funkcija u kojoj rezem rijec iz recenice
            j += len(txt_arr[i])
            i += 1

        letters = ['a', 'e', 'i', 'o', 'u', 'j', 'l', 'm', 'n', 'r', 'v', 'b', 'd', 'g', 'z']
        for let in letters:
            get_values(let, lab_lines, txt_arr, str_wav)

        num_files += 1


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
