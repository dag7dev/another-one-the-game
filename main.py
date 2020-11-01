import os
import ssl
import wget
import wave
import random
import tarfile
import DBManager
import numpy as np
import sounddevice as sd
from deepspeech import Model
from tinydb import TinyDB, Query
from scipy.io.wavfile import write
from difflib import SequenceMatcher


def generate_random_questions(questions, number_of_questions, limit):
    """
    :param questions: questions from DB
    :param number_of_questions: total number of questions
    :param limit: how many questions needs to be generated
    :return: questions in a random order
    """
    order = []
    random_questions = []

    try:
        order = random.sample(range(1, number_of_questions + 1), 20)
    except Exception:
        print("Can't generate order.")
        exit(1)

    for i in range(0, limit):
        question = questions.search(Query().id == str(order[i]))
        random_questions.append(question)

    return random_questions


def check_for_ds():
    """
    Check if Deepspeech is present or not. If not it downloads Italian deepspeech model.
    :return:
    """

    if not os.path.exists('DS'):
        os.makedirs('DS')

    os.chdir("DS")

    if not os.path.isfile("model_tensorflow_it.tar.xz"):
        print("Downloading Italian model...")
        wget.download(
            "https://github.com/MozillaItalia/DeepSpeech-Italian-Model/releases/download/2020.08.07"
            "/model_tensorflow_it.tar.xz",
            'model_tensorflow_it.tar.xz')

    if not os.path.isfile("alphabet.txt") and not os.path.isfile("scorer") and not os.path.isfile("output_graph.pbmm"):
        print("\nUnzipping model...")
        tar = tarfile.open("model_tensorflow_it.tar.xz")
        tar.extractall()
        tar.close()

    os.chdir("..")

    print()


def similar(a, b):
    """
    Check if two strings are similar with builtins.
    :param a: first string
    :param b: second string
    :return: coefficient of similarity
    """

    return SequenceMatcher(None, a, b).ratio()


def clear():
    """
    clear the terminal depending if you are on Windows or Linux
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def intro_message():
    """
    prints the intro message and ask to user if he wants to start the game
    """
    print("=== AnotherOne ===")
    print("=== dag7-2020 ===")
    print("Questo gioco prende ispirazione da un famoso gioco italiano\n"
          "televisivo, nel quale bisogna rispondere a delle domande\n"
          "con una particolarita': non bisogna dare la risposta giusta\n"
          "bensi' la risposta sbagliata.\n\n"
          "Quando apparira' la domanda sullo schermo, bisognera' rispondere\n"
          "AD ALTA VOCE in modo errato per andare avanti.\n\n"
          "Il gioco finisce quando si finiscono i tentativi massimi (3)\n"
          "oppure quando si indovinano dieci risposte sbagliate di fila\n")

    return input("Pronto? [S/n]")


def main():
    # game variables
    progressed = 0
    lives = 3  # the user has 3 lives
    limit = 10  # the game ends when the user gives n answers

    # audio variables
    sample_rate = 16000
    duration_of_recording = 2

    # deepspeech checks
    check_for_ds()
    ds = Model("DS/output_graph.pbmm")

    # questions
    DBManager.populate_db()
    questions = TinyDB('db/domande.json')
    number_of_questions = len(questions.all())
    random_questions = generate_random_questions(questions, number_of_questions, limit)

    clear()

    # what the user is going to do
    r = intro_message().lower()

    if r != "s" and r != "":
        clear()
        print("Alla prossima!")
        print()
        exit(1)

    # main game loop
    while progressed < limit and lives > 0:
        print(random_questions[progressed][0].get("text_ita"))

        # record the audio
        rec = sd.rec(int(duration_of_recording * sample_rate), dtype="int16", samplerate=sample_rate, channels=1)
        sd.wait()
        write('DS/out.wav', sample_rate, rec)

        # starts ds recognizer
        fin = wave.open("DS/out.wav", 'rb')
        fs_orig = fin.getframerate()
        if fs_orig != ds.sampleRate():
            print(
                "Your audio has not been correctly recorded. Please try to fix it and try again! (must be in 16000khz)")
            exit(1)
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
        stt_text = ds.stt(audio).lower().replace(" ", "")

        # check the output
        if float(similar(stt_text, random_questions[progressed][0].get("answer").lower())) >= 0.5:
            progressed += 1
        else:
            print("SBAGLIATO! " + "\nHai detto:" + stt_text)
            print()
            lives -= 1
            progressed = 0

    if progressed == limit:
        print("COMPLIMENTI! Hai vinto!")
        exit(0)

    if lives == 0:
        print("GAME OVER! Riprova!")
        exit(1)


ssl._create_default_https_context = ssl._create_unverified_context
main()
