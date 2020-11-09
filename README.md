# another-one-the-game
game inspired by a popular Italian quiz tv show - entry for deepspeech-italian-contest

This game has been submitted as an entry for the [deepspeech-italian-contest](https://github.com/MozillaItalia/DeepSpeech-Contest)

## Compatibility
This game has been tested (and it is fully working) on Linux or macOS.

## How to install
- Install portaudio (for Debian based the instructions below - other distros, use a search engine):
```
sudo apt install libportaudio2 libasound-dev libportaudio-ocaml sox
```
**AND**

- Download latest zip available (here: https://github.com/dag7dev/another-one-the-game/releases)
- unzip it
- in Terminal type: pip install -r requirements.txt in the root of the unzipped folder
- run ```./another-one-x-x-x```

**OR**

- Install portaudio and sox as well, clone the repo by using git or wheatever.
- Type:
```
pip3 install -r requirements.txt
```
on your terminal

If you prefer to download the repo with the GUI, just switch to GUI branch and repeat the procedure

## How to run
If you downloaded the zip, run:
```./another-one-x-x-x```

Otherwise in the root directory:
```
python3 main.py
```

The script will download every required files and the game will start.

## How to play
Instructions are displayed at the beginning.

Italian:
```
Questo gioco prende ispirazione da un famoso gioco italiano
televisivo, nel quale bisogna rispondere a delle domande
con una particolarita': non bisogna dare la risposta giusta
bensi' la risposta sbagliata.

Quando apparira' la domanda sullo schermo, bisognera' rispondere
ad alta voce in modo errato per andare avanti.

Il gioco finisce quando si finiscono i tentativi massimi (3)
oppure quando si indovinano dieci risposte sbagliate di fila.
```

English:
```
This game has been inspired by a famous italian quiz tv show
where you answer to questions but, you will need to give
the wrong answer and not the right one.

When the question will appears on the screen, you need to
answer wrongly (with voice) to go to the next question.

The game ends when you make a ten questions streak
(ten answers given) or when you finish your lives.

You have three lives!
Good luck!
```

Buon divertimento!
