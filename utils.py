import os
import wget
import random
import tarfile
from difflib import SequenceMatcher


def get_answers(question):
    answers = question.split(",")
    answers = answers[0].split(" o ")
    return answers[0], answers[1]


def generate_random_questions(questions, number_of_questions, limit):
    """
    :param questions: questions from file
    :param number_of_questions: total number of questions
    :param limit: how many questions needs to be generated
    :return: questions in a random order
    """
    order = []
    random_questions = []

    try:
        order = random.sample(range(0, number_of_questions), limit)
    except Exception:
        print("Can't generate order.")

    for i in range(0, limit):
        question = questions[order[i]]
        random_questions.append(question)

    return random_questions


def check_for_files():
    return True if os.path.isfile("alphabet.txt") and os.path.isfile("scorer") and os.path.isfile("output_graph.pbmm") else False


def check_for_xz():
    return True if os.path.isfile("model_tensorflow_it.tar.xz") else False


def download_model():
    print("Downloading Italian model...")
    wget.download(
        "https://github.com/MozillaItalia/DeepSpeech-Italian-Model/releases/download/2020.08.07"
        "/model_tensorflow_it.tar.xz",
        'model_tensorflow_it.tar.xz')


def untar():
    print("\nUnzipping model...")
    tar = tarfile.open("model_tensorflow_it.tar.xz")
    tar.extractall()
    tar.close()


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