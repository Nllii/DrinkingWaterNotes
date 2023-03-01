import curses
import time
import json

with open('quiz_data.json', 'r') as f:
    data = json.load(f)


questions = data['question']
options = [record['answer'] for record in data['records']]
correct_answer = data['correct_answer']
answer_options = [record['answer'] for record in data['records']]

def covert_to_letter(selected_option_idx):
    for i in range(1, 27):
        if i == selected_option_idx:
            letter = chr(ord('a') + i - 1)
            return letter



def print_menu(stdscr, selected_option_idx):
    stdscr.clear()
    question = (f'{questions} \n\n')
    stdscr.addstr(question, curses.A_ITALIC)
    for i, option in enumerate(options):
        if i == selected_option_idx:
            stdscr.addstr(f'{chr(65+i)}. {option}\n', curses.A_REVERSE)
        else:
            stdscr.addstr(f'{chr(65+i)}. {option}\n')

    stdscr.refresh()
    return question


def main(stdscr):
    curses.curs_set(0) # hide the cursor
    selected_option_idx = 0
    print_menu(stdscr, selected_option_idx)
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
            get_question = print_menu(stdscr, selected_option_idx)
        elif key == curses.KEY_ENTER or key in [10, 13]: # Enter key pressed
            stdscr.clear()
            user_choice = covert_to_letter(selected_option_idx + 1)
            if user_choice.upper() == chr(answer_options.index(correct_answer) + 65):
                stdscr.addstr(f'Correct! \n\n')
                # add question
                stdscr.addstr(f'{get_question} \n\n')
                # add answer
                stdscr.addstr(f'{correct_answer} \n\n')

                stdscr.addstr(f'Press any key to continue')
            else:
                # stdscr.addstr(f'\nYou selected option {selected_option_idx + 1}: {options[selected_option_idx]} \n\n')
                stdscr.addstr(f'Incorrect. \n\n')
                #TODO: Add rationale
                stdscr.addstr(f'Press any key to continue')


            stdscr.refresh()
            stdscr.getch()
            print_menu(stdscr, selected_option_idx)

        elif key == curses.KEY_RESIZE: # handle terminal resize
            print_menu(stdscr, selected_option_idx)
        elif key == ord(' ') and not spacebar_held_start_time: # spacebar pressed and held
            spacebar_held_start_time = current_time



curses.wrapper(main)
