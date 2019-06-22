Postupak pokretanja:

1. Kreiramo virtual environment => virtual_env ime_environmenta
2. Aktiviramo virtual environment => više o tome na poveznici https://docs.python-guide.org/dev/virtualenvs/
3. Pokrenemo naredbu pip install -r requirements.txt kako bi instalirali sve potrebno za izvođenje programa
3. Preselimo se pomoću terminala u folder gdje smo napravili clone repozitorija
4. Pokrenemo naredbu python get_voice.py koja rastavlja zvučne glasove u zasebne .wav datoteke
5. Pokrenemo naredbu python estimation.py koja pomoću programa world računa osnovnu frekvenciju (f0), spektralnu ovojnicu i aperiodičnost te provodi sintezu, nakon te naredbe u zasebne datoteke spremaju se dijagrami f0, spektralne ovojnice, aperiodičnosti te usporedbe signala prije i nakon sinteze world programom.
