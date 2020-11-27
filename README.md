# Modeling and estimation of the fundamental frequency of speech with the world program
 
 ## Project setup:

1. Create virtual environment 
  * `virtual_env env_name`
2. Activate virtual environment
  * more on [how to activate virtual environment][1].
3. Run installation of dependencies from requirements.txt
  * `pip install -r requirements.txt`
4. Move to the cloned repository folder 
5. Run script for dividing sounds in separate .wav folders
  * `python get_voice.py`
6. Run script which calculates the fundamental frequency (f0), spectral envelop and aperiodicity and does the synthesis.
  * `python estimation.py`
  
Results of the above script are saved into separate folders where you can find diagrams of f0, spectral envelop, aperiodicity and some of signal before and after synthesis with the world program.

[1]: https://docs.python-guide.org/dev/virtualenvs/ "Virtual environment activation"
