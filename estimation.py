import os
import soundfile as sf
import pyworld as pw
import matplotlib.pyplot as plt
import numpy as np
import argparse
from shutil import rmtree

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--frame_period", type=float, default=5)
parser.add_argument("-s", "--speed", type=int, default=1)

EPSILON = 1e-8


def create_dirs():
    if os.path.isdir('slike_f0_usporedbe'):
        rmtree('slike_f0_usporedbe')
    os.mkdir('slike_f0_usporedbe')

    if os.path.isdir('slike_sp_usporedbe'):
        rmtree('slike_sp_usporedbe')
    os.mkdir('slike_sp_usporedbe')

    if os.path.isdir('slike_ap_usporedbe'):
        rmtree('slike_ap_usporedbe')
    os.mkdir('slike_ap_usporedbe')

    if os.path.isdir('slike_before_after_sint_usporedbe'):
        rmtree('slike_before_after_sint_usporedbe')
    os.mkdir('slike_before_after_sint_usporedbe')

    if os.path.isdir('zvucni_glasovi_after_sint'):
        rmtree('zvucni_glasovi_after_sint')
    os.mkdir('zvucni_glasovi_after_sint')

    if os.path.isdir('rijeci_after_sint'):
        rmtree('rijeci_after_sint')
    os.mkdir('rijeci_after_sint')

    if os.path.isdir('slike_rijeci_after_sint'):
        rmtree('slike_rijeci_after_sint')
    os.mkdir('slike_rijeci_after_sint')


def savefig(filename, figlist, letter, log=True):
    # h = 10
    n = len(figlist)
    # peek into instances
    f = figlist[0]
    if len(f.shape) == 1:
        plt.figure()
        for i, f in enumerate(figlist):
            plt.subplot(n, 1, i + 1)
            if len(f.shape) == 1:
                if i == 0:
                    plt.plot(f, color='lightblue', label=f'signal glasa {letter} prije sinteze')
                else:
                    plt.plot(f, color='lightgreen', label=f'signal glasa {letter} poslije sinteze')
                plt.xlim([0, len(f)])
                plt.legend()

            plt.legend()
    elif len(f.shape) == 2:
        Nsmp, dim = figlist[0].shape
        # figsize=(h * float(Nsmp) / dim, len(figlist) * h)
        # plt.figure(figsize=figsize)
        plt.figure()
        for i, f in enumerate(figlist):
            plt.subplot(n, 1, i + 1)
            if log:
                x = np.log(f + EPSILON)
            else:
                x = f + EPSILON
            plt.imshow(x.T, origin='lower', interpolation='none', aspect='auto', extent=(0, x.shape[0], 0, x.shape[1]))
    else:
        raise ValueError('Input dimension must < 3.')

    plt.savefig(filename)
    plt.close()


def estimate_word(word, name):
    if os.path.exists(f'rijeci_wav/{word}_{name}.wav'):
        f_bef, fs = sf.read(f'rijeci_wav/{word}_{name}.wav')

        f0, timeaxis = pw.harvest(f_bef, fs)
        f0_mask = pw.stonemask(f_bef, f0, timeaxis, fs)
        sp = pw.cheaptrick(f_bef, f0_mask, timeaxis, fs)
        ap = pw.d4c(f_bef, f0_mask, timeaxis, fs)
        y = pw.synthesize(f0_mask, sp, ap, fs, pw.default_frame_period)

        sf.write(f'rijeci_after_sint/{word}_after_sint_{name}-def.wav', y, fs)
        savefig(f'slike_rijeci_after_sint/{word}_after_sint_{name}-def.png', [f_bef, y], word)

        y = pw.synthesize(f0_mask, sp, ap, fs, 3.0)

        sf.write(f'rijeci_after_sint/{word}_after_sint_{name}.wav', y, fs)
        savefig(f'slike_rijeci_after_sint/{word}_after_sint_{name}.png', [f_bef, y], word)

        y = pw.synthesize(f0_mask, sp, ap, fs, 20.0)

        sf.write(f'rijeci_after_sint/{word}_after_sint_{name}-20.wav', y, fs)
        savefig(f'slike_rijeci_after_sint/{word}_after_sint_{name}-20.png', [f_bef, y], word)


def estimate(letter, name):
    fb = 0
    fm = 0
    fe = 0
    max_beg = 0
    max_mid = 0
    max_end = 0

    if os.path.exists(f'zvucni_glasovi_wav/novi_{letter}_beg_{name}.wav'):
        beg, fs = sf.read(f'zvucni_glasovi_wav/novi_{letter}_beg_{name}.wav')

        """
        f0_dio, timeaxis_dio = pw.dio(beg, fs, f0_floor=70.0, f0_ceil=800.0, channels_in_octave=3.0,
                                      frame_period=args.frame_period,
                                      speed=args.speed)
        """
        f0, timeaxis = pw.harvest(beg, fs)
        f0_mask = pw.stonemask(beg, f0, timeaxis, fs)
        sp = pw.cheaptrick(beg, f0_mask, timeaxis, fs)
        ap = pw.d4c(beg, f0_mask, timeaxis, fs)
        y = pw.synthesize(f0_mask, sp, ap, fs, pw.default_frame_period)

        sf.write(f'zvucni_glasovi_after_sint/{letter}_beg_{name}_after_sint.wav', y, fs)

        plt.figure()
        plt.title(f'Glas {letter} na početku riječi')
        plt.plot(timeaxis, f0, 'r', label='Procjenjena f0 pomoću harvest() funkcije')
        # plt.plot(timeaxis_dio, f0_dio, 'y', label='Procjenjena f0 pomoću DIO() funkcije')
        plt.plot(timeaxis, f0_mask, 'g--', label='Pročišćena f0 pomoću stonemaska')

        plt.ylabel('frekvencija (Hz)')
        plt.xlabel('vrijeme (s)')
        plt.legend()
        plt.savefig(f'slike_f0_usporedbe/f0_{letter}_{name}_beg.png')
        savefig(f'slike_before_after_sint_usporedbe/before_after_synt_{letter}_{name}_beg.png', [beg, y], letter + '_beg')
        savefig(f'slike_sp_usporedbe/sp_{letter}_{name}_beg.png', [sp], letter)
        savefig(f'slike_ap_usporedbe/ap_{letter}_{name}_beg.png', [ap], letter, log=False)
        plt.close()
        max_beg = np.max(f0)
        fb = 1

    if os.path.exists(f'zvucni_glasovi_wav/novi_{letter}_mid_{name}.wav'):
        mid, fs = sf.read(f'zvucni_glasovi_wav/novi_{letter}_mid_{name}.wav')
        """
        f0_dio, timeaxis_dio = pw.dio(mid, fs, f0_floor=70.0, f0_ceil=800.0, channels_in_octave=2.0,
                                      frame_period=args.frame_period,
                                      speed=args.speed)
        """
        f0, timeaxis = pw.harvest(mid, fs)
        f0_mask = pw.stonemask(mid, f0, timeaxis, fs)
        sp = pw.cheaptrick(mid, f0_mask, timeaxis, fs)
        ap = pw.d4c(mid, f0_mask, timeaxis, fs)
        y = pw.synthesize(f0_mask, sp, ap, fs, pw.default_frame_period)

        sf.write(f'zvucni_glasovi_after_sint/{letter}_mid_{name}_after_sint.wav', y, fs)

        plt.figure()
        plt.title(f'Glas {letter} u sredini riječi')
        plt.plot(timeaxis, f0, 'r', label='Procjenjena f0 pomoću harvest() funkcije')
        # plt.plot(timeaxis_dio, f0_dio, 'y', label='Procjenjena f0 pomoću DIO() funkcije')
        plt.plot(timeaxis, f0_mask, 'g--', label='Pročišćena f0 pomoću stonemaska')

        plt.ylabel('frekvencija (Hz)')
        plt.xlabel('vrijeme (s)')
        plt.legend()
        plt.savefig(f'slike_f0_usporedbe/f0_{letter}_{name}_mid.png')
        savefig(f'slike_before_after_sint_usporedbe/before_after_synt_{letter}_{name}_mid.png', [mid, y], letter + '_mid')
        savefig(f'slike_sp_usporedbe/sp_{letter}_{name}_mid.png', [sp], letter)
        savefig(f'slike_ap_usporedbe/ap_{letter}_{name}_mid.png', [ap], letter, log=False)
        plt.close()
        max_mid = np.max(f0)
        fm = 1

    if os.path.exists(f'zvucni_glasovi_wav/novi_{letter}_end_{name}.wav'):
        end, fs = sf.read(f'zvucni_glasovi_wav/novi_{letter}_end_{name}.wav')
        """
        f0_dio, timeaxis_dio = pw.dio(end, fs, f0_floor=70.0, f0_ceil=800.0, channels_in_octave=2.0,
                                      frame_period=args.frame_period,
                                      speed=args.speed)
        """
        f0, timeaxis = pw.harvest(end, fs)
        f0_mask = pw.stonemask(end, f0, timeaxis, fs)
        sp = pw.cheaptrick(end, f0_mask, timeaxis, fs)
        ap = pw.d4c(end, f0_mask, timeaxis, fs)
        y = pw.synthesize(f0_mask, sp, ap, fs, pw.default_frame_period)

        sf.write(f'zvucni_glasovi_after_sint/{letter}_end_{name}_after_sint.wav', y, fs)

        plt.figure()
        plt.title(f'Glas {letter} na kraju riječi')
        plt.plot(timeaxis, f0, 'r', label='Procjenjena f0 pomoću harvest() funkcije')
        # plt.plot(timeaxis_dio, f0_dio, 'y', label='Procjenjena f0 pomoću DIO() funkcije')
        plt.plot(timeaxis, f0_mask, 'g--', label='Pročišćena f0 pomoću stonemaska')

        plt.ylabel('frekvencija (Hz)')
        plt.xlabel('vrijeme (s)')
        plt.legend()
        plt.savefig(f'slike_f0_usporedbe/f0_{letter}_{name}_end.png')
        savefig(f'slike_before_after_sint_usporedbe/before_after_synt_{letter}_{name}_end.png', [end, y], letter + '_end')
        savefig(f'slike_sp_usporedbe/sp_{letter}_{name}_end.png', [sp], letter)
        savefig(f'slike_ap_usporedbe/ap_{letter}_{name}_end.png', [ap], letter, log=False)
        plt.close()
        max_end = np.max(f0)
        fe = 1

    if fb and fm and fe:
        x = [5, 10, 15]
        max_f0 = [max_beg, max_mid, max_end]
        plt.bar(x, height=max_f0)
        plt.axhline(np.average(max_f0), color='lightblue', linestyle='--', label='prosjek')
        plt.xticks(x, [f'{letter}_beg', f'{letter}_mid', f'{letter}_end'])
        plt.xlabel('pozicija')
        plt.ylabel('frekvencija (Hz)')
        plt.legend()
        plt.savefig(f'slike_f0_usporedbe/f0_{letter}_{name}_hist.png')
        plt.close()

    """
    if not fb and fm and fe:
        # savefig(f'slike_f0_usporedbe/f0_{letter}_{name}_mid_end.png', [f0_mid, f0_end])
    if fb and not fm and fe:
        # savefig(f'slike_f0_usporedbe/f0_{letter}_{name}_beg_end.png', [f0_beg, f0_end])
    if fb and fm and not fe:
        # savefig(f'slike_f0_usporedbe/f0_{letter}_{name}_beg_mid.png', [f0_beg, f0_mid])
    if not fb and not fm and fe:
        # savefig(f'slike_f0_usporedbe/f0_{letter}_{name}_end.png', [f0_end])
    if not fb and fm and not fe:
        # savefig(f'slike_f0_usporedbe/f0_{letter}_{name}_mid.png', [f0_mid])
    if fb and not fm and not fe:
        # savefig(f'slike_f0_usporedbe/f0_{letter}_{name}_beg.png', [f0_beg])
    """


def main(args):
    create_dirs()

    dir_wav = os.listdir('wav')
    dir_txt = os.listdir('txt')

    cnt = 0
    letters = ['a', 'e', 'i', 'o', 'u', 'j', 'l', 'm', 'n', 'r', 'v', 'b', 'd', 'g', 'z']
    for file in dir_wav:
        txt = open(f'txt/{dir_txt[cnt]}', "r")
        txt_lines = txt.readlines()

        for br in range(len(txt_lines)):
            txt_arr = txt_lines[br].split(" ")

        i = 0
        name, ext = file.split('.')
        while i != len(txt_arr) - 1:
            estimate_word(txt_arr[i], name)  # funkcija u kojoj uspoređujem riječ prije i poslije sinteze
            i += 1

        for let in letters:
            estimate(let, name)
            # print(name)
        cnt += 1


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
