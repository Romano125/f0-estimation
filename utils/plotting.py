import matplotlib.pyplot as plt
import numpy as np

from constants.common import EPSILON


def savefig(filename, figlist, sound, log=True):
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
                    plt.plot(f, color='lightblue',
                             label=f'speech {sound} signal before synthesis')
                else:
                    plt.plot(f, color='lightgreen',
                             label=f'speech {sound} signal after synthesis')
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
            plt.imshow(x.T, origin='lower', interpolation='none',
                       aspect='auto', extent=(0, x.shape[0], 0, x.shape[1]))
    else:
        raise ValueError('Input dimension must < 3.')

    plt.savefig(filename)
    plt.close()


def plot_f0(sound, sound_position, timeaxis, f0, f0_mask, file_path):
    plt.figure()
    plt.title(f'Sound {sound} at the {sound_position} of the word')
    plt.plot(timeaxis, f0, 'r',
             label='Estimated f0 with harvest')
    # plt.plot(timeaxis_dio, f0_dio, 'y',
    #          label='Estimated f0 with DIO')
    plt.plot(timeaxis, f0_mask, 'g--',
             label='Cleaned f0 with stonemask')

    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.legend()
    plt.savefig(file_path)
    plt.close()


def plot_f0_comparison(sound, f0_begin, f0_middle, f0_end, file_path):
    x = [5, 10, 15]
    f0_max = [f0_begin, f0_middle, f0_end]
    plt.bar(x, height=f0_max)
    plt.axhline(np.average(f0_max), color='lightblue',
                linestyle='--', label='Average')
    plt.xticks(x, [f'{sound}_begin', f'{sound}_middle', f'{sound}_end'])
    plt.xlabel('Position')
    plt.ylabel('Frequency (Hz)')
    plt.legend()
    plt.savefig(file_path)
    plt.close()
