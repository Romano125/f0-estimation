import os


def create_processed_directories():
    if os.path.isdir('veprad_processed') == False:
        os.mkdir('veprad_processed')
    if os.path.isdir('veprad_processed/sounds') == False:
        os.mkdir('veprad_processed/sounds')
    if os.path.isdir('veprad_processed/sounds/begin') == False:
        os.mkdir('veprad_processed/sounds/begin')
    if os.path.isdir('veprad_processed/sounds/middle') == False:
        os.mkdir('veprad_processed/sounds/middle')
    if os.path.isdir('veprad_processed/sounds/end') == False:
        os.mkdir('veprad_processed/sounds/end')
    if os.path.isdir('veprad_processed/words') == False:
        os.mkdir('veprad_processed/words')


def create_synthesis_directories():
    if os.path.isdir('synthesis') == False:
        os.mkdir('synthesis')
    if os.path.isdir('synthesis/sounds') == False:
        os.mkdir('synthesis/sounds')
    if os.path.isdir('synthesis/sounds/begin') == False:
        os.mkdir('synthesis/sounds/begin')
    if os.path.isdir('synthesis/sounds/middle') == False:
        os.mkdir('synthesis/sounds/middle')
    if os.path.isdir('synthesis/sounds/end') == False:
        os.mkdir('synthesis/sounds/end')
    if os.path.isdir('synthesis/words') == False:
        os.mkdir('synthesis/words')


def create_plots_synthesis_directories():
    if os.path.isdir('plots/synthesis') == False:
        os.mkdir('plots/synthesis')
    if os.path.isdir('plots/synthesis/words') == False:
        os.mkdir('plots/synthesis/words')


def create_plots_directories():
    if os.path.isdir('plots/sounds') == False:
        os.mkdir('plots/sounds')
    if os.path.isdir('plots/sounds/begin') == False:
        os.mkdir('plots/sounds/begin')
    if os.path.isdir('plots/sounds/begin/f0') == False:
        os.mkdir('plots/sounds/begin/f0')
    if os.path.isdir('plots/sounds/begin/spectral_envelop') == False:
        os.mkdir('plots/sounds/begin/spectral_envelop')
    if os.path.isdir('plots/sounds/begin/aperiodicity') == False:
        os.mkdir('plots/sounds/begin/aperiodicity')
    if os.path.isdir('plots/sounds/begin/synthesis_comparison') == False:
        os.mkdir('plots/sounds/begin/synthesis_comparison')
    if os.path.isdir('plots/sounds/middle') == False:
        os.mkdir('plots/sounds/middle')
    if os.path.isdir('plots/sounds/middle/f0') == False:
        os.mkdir('plots/sounds/middle/f0')
    if os.path.isdir('plots/sounds/middle/spectral_envelop') == False:
        os.mkdir('plots/sounds/middle/spectral_envelop')
    if os.path.isdir('plots/sounds/middle/aperiodicity') == False:
        os.mkdir('plots/sounds/middle/aperiodicity')
    if os.path.isdir('plots/sounds/middle/synthesis_comparison') == False:
        os.mkdir('plots/sounds/middle/synthesis_comparison')
    if os.path.isdir('plots/sounds/end') == False:
        os.mkdir('plots/sounds/end')
    if os.path.isdir('plots/sounds/end/f0') == False:
        os.mkdir('plots/sounds/end/f0')
    if os.path.isdir('plots/sounds/end/spectral_envelop') == False:
        os.mkdir('plots/sounds/end/spectral_envelop')
    if os.path.isdir('plots/sounds/end/aperiodicity') == False:
        os.mkdir('plots/sounds/end/aperiodicity')
    if os.path.isdir('plots/sounds/end/synthesis_comparison') == False:
        os.mkdir('plots/sounds/end/synthesis_comparison')
    if os.path.isdir('plots/sounds/f0_comparison') == False:
        os.mkdir('plots/sounds/f0_comparison')
