import statistics
import random
import time

from typing import List
from time import monotonic
from blessings import Terminal

from . import Note

INTERVALS = {
    1: ['min 2nd', 'm2'],
    2: ['maj 2nd', 'M2'],
    3: ['min 3rd', 'm3'],
    4: ['maj 3rd', 'M3'],
    5: ['perf 4th', 'p4'],
    6: ['#4 / b5', '#4', 'b5'],
    7: ['perf 5th', 'p5'],
    8: ['min 6th', 'm6'],
    9: ['maj 6th', 'M6'],
    10: ['min 7th', 'm7'],
    11: ['maj 7th', 'M7']
}


def _find_interval_by_name(name: str) -> int:
    for i in range(1, len(INTERVALS)):
        if INTERVALS[i] == name:
            return i
    else:
        raise AssertionError(f'Interval not found: {name}')


class Intervals():
    """
        Intervals game
    """
    def __init__(self, options: str):
        self.lower_idx = 1
        self.upper_idx = 11
        if options is not None:
            option_tokens = options.split('-')
            assert len(option_tokens) == 2

            self.lower_idx = _find_interval_by_name(option_tokens[0])
            self.upper_idx = _find_interval_by_name(option_tokens[1])

            assert self.lower_idx < self.upper_idx

        self.num_trials: int = 0
        self.num_success: int = 0
        self.times: List[int] = []
        self.term = Terminal()

    def choose_challenge(self):
        interval: int = random.randint(1, 11)
        start_note: Note = Note.from_position(random.randint(1, 11))
        correct_note: Note = Note.with_distance(start_note, interval)
        return interval, start_note, correct_note

    def play(self):
        t = self.term
        with t.location():
            while True:

                interval, start_note, correct_note = self.choose_challenge()

                interval_name = INTERVALS[interval][0]

                start_note_name = start_note.names[0] if len(
                    start_note.names) == 1 else start_note.names[
                        random.randint(0, 1)]

                start_monotonic = monotonic()

                success_ratio = 0 if self.num_trials == 0 else int(
                    self.num_success / float(self.num_trials) * 100)

                avg_resp_time = statistics.mean(
                    self.times) if len(self.times) > 0 else 0.0
                print(
                    f'{t.clear_eos}{self.num_success}/{self.num_trials} correct ({success_ratio}%), {avg_resp_time:.2f} seconds avg.',
                    end='')
                input_str = input(
                    f'{t.move_down}What is the {t.bold}{interval_name}{t.normal} of {t.bold}{start_note_name}{t.normal}?\n'
                )
                correct = False
                self.num_trials += 1
                try:
                    input_note = Note.from_name(input_str)

                    if input_note == correct_note:
                        self.num_success += 1
                        correct = True
                    self.times.append(monotonic() - start_monotonic)
                except AssertionError:
                    # Treat parse errors as incorrect answer
                    pass

                challenge_delay = 2
                correct_str = f'is {t.red}{t.bold}Incorrect! Correct answer would have been `{correct_note}`.'
                if correct:
                    challenge_delay = 1  # wait a shorter amount if the answer was correct
                    correct_str = f'is {t.green}{t.bold}Correct!'
                print(f'{t.move_up}', end='')
                print(f'{input_str} {correct_str}{t.normal}',
                      end='',
                      flush=True)

                time.sleep(challenge_delay)
                print(t.move_up, t.move_up, t.move_x(0), end='')
