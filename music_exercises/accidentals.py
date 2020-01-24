import statistics
import random
import time

from typing import List, Tuple, Dict
from time import monotonic
from blessings import Terminal

from . import Note

_ACCIDENTALS: Dict[str, Dict] = {
    'sharps': {
        Note('C'): [],
        Note('G'): [Note('F#')],
        Note('D'): [Note('F#'), Note('C#')],
        Note('A'): [Note('F#'), Note('C#'),
                    Note('G#')],
        Note('E'): [Note('F#'), Note('C#'),
                    Note('G#'), Note('D#')],
        Note('B'):
        [Note('F#'),
         Note('C#'),
         Note('G#'),
         Note('D#'),
         Note('A#')],
        Note('F#'): [
            Note('F#'),
            Note('C#'),
            Note('G#'),
            Note('D#'),
            Note('A#'),
            Note('E#')
        ],
        Note('C#'): [
            Note('F#'),
            Note('C#'),
            Note('G#'),
            Note('D#'),
            Note('A#'),
            Note('E#'),
            Note('B#')
        ]
    },
    'flats': {
        Note('C'): [],
        Note('F'): [Note('Bb')],
        Note('Bb'): [Note('Bb'), Note('Eb')],
        Note('Eb'): [Note('Bb'), Note('Eb'),
                     Note('Ab')],
        Note('Ab'): [Note('Bb'),
                     Note('Eb'),
                     Note('Ab'),
                     Note('Db')],
        Note('Db'):
        [Note('Bb'),
         Note('Eb'),
         Note('Ab'),
         Note('Db'),
         Note('Gb')],
        Note('Gb'):
        [Note('Bb'),
         Note('Eb'),
         Note('Ab'),
         Note('Db'),
         Note('Gb'),
         Note('Cb')],
    }
}


class Accidentals():
    def __init__(self):
        self.num_trials: int = 0
        self.num_success: int = 0
        self.times: List[int] = []
        self.term = Terminal()

    def choose_challenge(self) -> Tuple[Note, int]:
        flat = random.random() < 0.5

        collection = _ACCIDENTALS['flats'] if flat else _ACCIDENTALS['sharps']

        choice = random.sample(list(collection), 1)[0]

        return choice, collection[choice]

    def correct_answer(self, input_str, correct, notes):
        if notes:
            if len(input_str.split()) != len(correct):
                return False
            for note_str in input_str.split():
                if Note.from_name(note_str) not in correct:
                    return False
            return True
        else:
            return int(input_str) == len(correct)

    def play(self, notes):
        t = self.term
        with t.location():
            while True:

                note, answer = self.choose_challenge()

                start_monotonic = monotonic()

                success_ratio = 0 if self.num_trials == 0 else int(
                    self.num_success / float(self.num_trials) * 100)

                avg_resp_time = statistics.mean(
                    self.times) if len(self.times) > 0 else 0.0
                print(
                    f'{t.clear_eos}{self.num_success}/{self.num_trials} correct ({success_ratio}%), {avg_resp_time:.2f} seconds avg.',
                    end='')
                question_prefix = 'What' if notes else 'How many'
                input_str = input(
                    f'{t.move_down}{question_prefix} accidentals does {t.bold}{note}{t.normal} have?\n'
                )
                correct = False
                self.num_trials += 1
                try:
                    if self.correct_answer(input_str, answer, notes):
                        self.num_success += 1
                        correct = True
                    self.times.append(monotonic() - start_monotonic)
                except ValueError:
                    # Treat parse errors as incorrect answer
                    pass

                challenge_delay = 5
                correct_answer_str = ', '.join(map(lambda nt: nt.names[0], answer)) if notes else len(answer)
                correct_str = f'is {t.red}{t.bold}Incorrect! Correct answer would have been `{correct_answer_str}`.'
                if correct:
                    challenge_delay = 1  # wait a shorter amount if the answer was correct
                    correct_str = f'is {t.green}{t.bold}Correct!'
                print(f'{t.move_up}', end='')
                print(f'{input_str} {correct_str}{t.normal}',
                      end='',
                      flush=True)

                time.sleep(challenge_delay)
                print(t.move_up, t.move_up, t.move_x(0), end='')