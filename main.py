import json
import os
import wave
import PySimpleGUI as sg
import sounddevice as sd
from scipy.io.wavfile import write

import utils
import numpy as np
from deepspeech import Model


def check_for_ds():
    """
    Check if Deepspeech is present or not. If not it downloads Italian deepspeech model.
    :return:
    """
    string = ""

    # PRINT THE
    layout = [[sg.Text(size=(100, 5), key='text')]]
    window = sg.Window('Preparing the game...', layout, finalize=True, size=(300, 200))
    window.disappear()

    # manage the window
    event, values = window.read(timeout=100)
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        exit(0)

    if not os.path.exists('DS'):
        os.makedirs('DS')
        string += "DS"

    os.chdir("DS")

    flg_files = utils.check_for_files()
    flg_xz = utils.check_for_xz()

    if not flg_xz and not flg_files:
        window.reappear()
        window['text'].update("Downloading italian Deepspeech model...")
        window.refresh()
        utils.download_model()

        window['text'].update("Unzipping model...")
        window.refresh()
        utils.untar()

        os.remove("model_tensorflow_it.tar.xz")
    elif flg_xz:
        window.reappear()

        window['text'].update("Unzipping model...")
        window.refresh()

        utils.untar()
        os.remove("model_tensorflow_it.tar.xz")

    os.chdir("..")

    window.disappear()
    window.close()


# DEFINING THE MAIN WINDOW
lbl_q = ""
lbl_a1 = ""
lbl_a2 = ""
lbl_result = ""
lbl_deep = "Ascolto..."
lbl_question = " Domanda 1/10"
progressed = ""

layout = [
    [sg.Text(lbl_question, background_color="#E05A00", key='lbl_question', size=(13, 1), font=("Helvetica", 14))],
    [sg.Text(lbl_q, key='lbl_q', background_color="#663A82", justification='center', size=(100, 1),
             font=("Helvetica", 18))],
    [],
    [sg.Text(lbl_a1, key='lbl_a1', background_color="#009900", justification='center', size=(42, 1),
             font=("Helvetica", 12)),
     sg.Text(lbl_a2, key='lbl_a2', background_color="#009900", justification='center', size=(42, 1),
             font=("Helvetica", 12))],
    [sg.ProgressBar(10, orientation='h', size=(100, 20), key='progbar')],
    [sg.Text(lbl_deep, justification='center', size=(100, 1), key='lbl_deep', font=("Helvetica", 18),
             background_color="#CCCC00")],
    [sg.Text(lbl_result, justification='center', size=(100, 1), key='lbl_result', font=("Helvetica", 15))]
]

check_for_ds()

# Create the window
window = sg.Window('another-one-the-game', layout, finalize=True, size=(800, 200))

##################
# GAME VARIABLES #
##################
# audio variables
sample_rate = 16000
duration_of_recording = 3

# deepspeech check
ds = Model("DS/output_graph.pbmm")

# questions
questions = None

# open question file (at least one)
fd = open("db/domande.json")

# load file
try:
    questions = json.load(fd)
except ValueError:
    print("Non e' un file JSON. Prova con un file domande.json e delle domande!")

check_for_ds()

while True:
    # game variables
    progressed = 0
    lives = 3  # the user has 3 lives
    limit = 10  # the game ends when the user gives n answers
    bar_prog = 0

    total_number_of_questions = len(questions)
    random_questions = utils.generate_random_questions(questions, total_number_of_questions, limit)

    # main game loop
    while progressed < limit and lives > 0:
        window['lbl_question'].update(" Domanda " + str(progressed + 1) + "/" + str(limit))

        # manage the window
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            exit(0)

        # Output a message to the window
        window['lbl_q'].update(random_questions[progressed]["text"])
        window['lbl_a1'].update(utils.get_answers(random_questions[progressed]["text"])[0])
        window['lbl_a2'].update(utils.get_answers(random_questions[progressed]["text"])[1])
        window.refresh()

        # record the audio
        window['lbl_deep'].update("Ascolto...")
        window.refresh()
        rec = sd.rec(int(duration_of_recording * sample_rate), dtype="int16", samplerate=sample_rate, channels=1)
        sd.wait()
        write('DS/out.wav', sample_rate, rec)

        window['lbl_deep'].update("Elaboro...")
        window.refresh()

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
        if float(utils.similar(stt_text, random_questions[progressed]["answer"].lower())) >= 0.5:
            progressed += 1
            window['progbar'].update(progressed)
            window['lbl_result'].update("Esatto!", background_color="green")
        else:
            lives -= 1
            progressed = 0
            window['progbar'].update(progressed)
            window['lbl_result'].update("SBAGLIATO! Hai detto: " + stt_text, background_color="red")

    if progressed == limit:
        s = "COMPLIMENTI! Hai vinto!"

    if lives == 0:
        s = "GAME OVER! Riprova!"

    window.disappear()

    res = sg.popup_yes_no(s + "\n" + "Vuoi giocare ancora?")

    if res.lower() == "no":
        exit(0)

    # reset progress bar
    window['progbar'].update(0)
    window.reappear()
