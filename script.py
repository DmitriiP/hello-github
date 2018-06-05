import json
import subprocess
from random import randint
from datetime import timedelta, datetime
from itertools import chain

from letters import *

LOW_NUMBER = (1, 7,)
HIGH_NUMBER = (20, 23,)

message = [
    LETTER_H,
    SPACE,
    LETTER_E,
    SPACE,
    LETTER_L,
    SPACE,
    LETTER_L,
    SPACE,
    LETTER_O,
    SPACE,
    SPACE,
    SPACE,
    LETTER_G,
    SPACE,
    LETTER_I,
    SPACE,
    LETTER_T,
    SPACE,
    LETTER_H,
    SPACE,
    LETTER_U,
    SPACE,
    LETTER_B,
    SPACE,
]

def show_message(chained_once_message):
    print_message = list(zip(*chained_once_message))
    for line in print_message:
        row = []
        for point in line:
            if point:
                row.append('*')
            else:
                row.append(' ')
        print(''.join(row))
    print('Full time to show the message (in weeks):', len(print_message[0]))

def set_start_date(today):
    if today.weekday() != 6:  # Sunday
        raise ValueError("Should start at Sunday!")
    with open("start_date", "w") as f:
        f.write(today.isoformat())

def get_start_date(num_weeks):
    today = datetime.utcnow().date()
    try:
        with open("start_date") as f:
            start_date = datetime.strptime(f.read()[:10], '%Y-%m-%d').date()
        # Enabling cycles
        if today - start_date > timedelta(weeks=num_weeks):
            set_start_date(today)
            return today
        return start_date
    except FileNotFoundError:
        set_start_date(today)
        return today

def target_count(start_date, today, message):
    diff = (today - start_date).days
    try:
        if message[diff]:
            return randint(*HIGH_NUMBER)
        else:
            return randint(*LOW_NUMBER)
    except IndexError:
        return randint(*LOW_NUMBER)

def save_work_dict(work_dict):
    with open("work_dict", "w") as f:
        json.dump(work_dict, f)

def get_work_dict():
    try:
        with open("work_dict") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def do_contribution():
    with open("contribution", "a") as f:
        f.write('*')
    subprocess.run(['git', 'commit', '-am', 'Hello Github!'])
    subprocess.run(['git', 'push', 'origin', 'master'])


if __name__ == '__main__':
    message = list(chain(*message))
    show_message(message)
    message = list(chain(*message))
    start_date = get_start_date(len(message)/7)
    print('Started at:', start_date)

    today = datetime.utcnow().date()

    work_dict = get_work_dict()
    todo = work_dict.setdefault(today.isoformat(), {
        'contributed': 0,
        'target': target_count(start_date, today, message)
    })
    print(todo)
    if todo['contributed'] < todo['target']:
        do_contribution()
        todo['contributed'] += 1
    save_work_dict(work_dict)
