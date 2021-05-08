# Modeling and estimation of the fundamental frequency of speech with the world program

## Project setup:

1. Create virtual environment

- `virtual_env env_name`

2. Activate virtual environment

- more on [how to activate virtual environment][1].

3. Run installation of dependencies from requirements.txt

- `pip install -r requirements.txt`

4. Move to the cloned repository folder
5. Run script which calculates the fundamental frequency (f0), spectral envelop and aperiodicity and does the synthesis.

- `python main.py`

Results of the above script are saved into separate folders where you can find charts of f0, spectral envelop, aperiodicity and some of signals before and after synthesis with the WORLD program.

[1]: https://docs.python-guide.org/dev/virtualenvs/ "Virtual environment activation"
