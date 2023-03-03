import curses
import time
import sys
import threading
from studyGuideDatabase import hltcorpApi
import random
import subprocess
import os
import json
queue = []
next_question = False
#TODO: use queue to load questions
loadquestions = 0
current_number = 1
hlt_thread = None



def hltStudyGuides():
    global loadquestions,next_question,stdscr
    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.addstr(f"Loading questions...\n\n", curses.A_ITALIC)
    # stdscr = curses.initscr()
    pending_questions = hltcorpApi.getQuestions() # get the questions from the database, hope it loads all of them at once
    if next_question == True:
        stdscr.refresh()
        # stdscr.addstr(f"{loadquestions}\n\n", curses.A_ITALIC)
        pending_questions.skip(loadquestions) # skip the next 5 questions
        next_question = False
        queue.clear()
    for _data in pending_questions:
        loadquestions += 1
        if 'ZQUESTION' in _data:
            studyquestion = _data['ZQUESTION']
            info = hltcorpApi.generateQuestions(_data,studyquestion,stdscr)
            queue.append(info)
            #load the first 10 questions
            if len(queue) == 10:
                # stdscr.addstr(f"Questions loaded...\n\n", curses.A_ITALIC)
                stdscr.refresh()
                return True
        else:
            continue


# start a thread to load the questions


# put this in a thread so it runs in the background
def start_hltStudyGuides():
    global hlt_thread
    hlt_thread = threading.Thread(target=hltStudyGuides)
    hlt_thread.start()

def stop_hltStudyGuides():
    global hlt_thread
    if hlt_thread:
        hlt_thread.join()
        hlt_thread = None

# this is meant to be a thread that will start loading the questions
start_hltStudyGuides()
def studyinfomation():
    # do not block the main thread
    if next_question == True:
        queue.pop(0)
    while not queue:
        time.sleep(0.1)
    for data in queue:
        questions = data['question']
        options = [record['answer'] for record in data['records']]
        correct_answer = data['correct_answer']
        answer_options = [record['answer'] for record in data['records']]
        rationale = data['rationale']
        random.shuffle(options)
        return questions, options, correct_answer, answer_options, rationale




# questions, options, correct_answer, answer_options, rationale = studyinfomation()
def covert_to_letter(selected_option_idx):
    for i in range(1, 27):
        if i == selected_option_idx:
            letter = chr(ord('a') + i - 1)
            return letter


def returnDatabank(nextQuestion,stdscr):
    global current_question,next_question,questions, options, correct_answer, answer_options, rationale,current_number
    if nextQuestion == False:
        # current_number += 1
        return questions, options, correct_answer, answer_options, rationale
    else:
        next_question = True
        current_number += 1
        questions, options, correct_answer, answer_options, rationale = studyinfomation()
def print_menu(stdscr, selected_option_idx):
    global current_question
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    # curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    stdscr.refresh()
    stdscr.addstr(f'Plant Operator Study Guide \n\n',curses.color_pair(2))
    current_question = (f'{current_number}). {questions} \n\n')
    curses.curs_set(1) # enable the cursor
    stdscr.addstr(current_question, curses.A_ITALIC)
    for i, option in enumerate(options):
        if i == selected_option_idx:
            stdscr.addstr(f"{i + 1}. {option}\n", curses.color_pair(2))
            # stdscr.addstr(f'{chr(65+i)}. {option}\n', curses.A_REVERSE)
        else:
            stdscr.addstr(f"{i + 1}. {option}\n", curses.color_pair(1))
            # stdscr.addstr(f'{chr(65+i)}. {option}\n')
    stdscr.refresh()
    # return question


def main(stdscr):
    global next_question,  questions, options, correct_answer, answer_options, rationale
    questions, options, correct_answer, answer_options, rationale = studyinfomation()
    next_question = False
    curses.curs_set(0)
    selected_option_idx = 0
    print_menu(stdscr, selected_option_idx) #initial print
    last_spacebar_press_time = 0
    spacebar_held_start_time = None
    while True:

        key = stdscr.getch()

        current_time = time.time()
        if key == ord(' '):
            if current_time - last_spacebar_press_time < 0.2: # spacebar pressed twice
                selected_option_idx = (selected_option_idx - 1) % len(options)
            else: # spacebar pressed once
                selected_option_idx = (selected_option_idx + 1) % len(options)
            last_spacebar_press_time = current_time
            print_menu(stdscr, selected_option_idx)
        elif key == curses.KEY_ENTER or key in [10, 13]: # Enter key pressed
            stdscr.clear()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            stdscr.refresh()

            selected_option = options[selected_option_idx]
            if selected_option == correct_answer:
                stdscr.addstr(f'Correct! \n\n')
                stdscr.addstr(f'{current_question} \n\n')
                stdscr.addstr(f'{correct_answer}\n\n')
                if rationale:
                    stdscr.addstr("\n\nRationale:\n", curses.A_BOLD)
                    stdscr.addstr(rationale, curses.A_NORMAL)
                next_question = True
                returnDatabank(next_question,stdscr)
                next_question = False
                # reset index
                selected_option_idx = 0
            else:
                stdscr.addstr(f'Incorrect\n\n', curses.color_pair(1))
                if rationale:
                    stdscr.addstr("\n\nRationale:\n", curses.A_BOLD)
                    stdscr.addstr(rationale, curses.A_NORMAL)
                stdscr.addstr(f'\n\n{current_question}\n\n')
                stdscr.addstr(f'Press any key to continue \n\n')
                next_question = False
            stdscr.refresh()
            stdscr.getch()
            print_menu(stdscr, selected_option_idx)

        elif key == curses.KEY_RESIZE: # handle terminal resize
            print_menu(stdscr, selected_option_idx)
        elif key == ord(' ') and not spacebar_held_start_time: # spacebar pressed and held
            spacebar_held_start_time = current_time




notesOptions = len(sys.argv)
if notesOptions == 1:
    try:
        subprocess.call("bash ./helper.sh s ", shell=True)
        subprocess.call("bash ./helper.sh i ", shell=True)
        curses.wrapper(main)
    except KeyboardInterrupt:
        subprocess.call("bash ./helper.sh q ", shell=True)
        if not queue:
            print("- No questions in queue to save")
        else:
            with open("current_state.json", "w") as f:
                json.dump({"current_question": current_question, "current_number": current_number}, f)
        os._exit(0)
else:
    if sys.argv[1] == "-j":
        print("- searching for jobs...")





