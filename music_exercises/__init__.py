from typing import List

_NUM_NOTES = 12

NOTES: List['Note'] = []


class Note():
    def __init__(self, *name_strs: str) -> None:
        self.names: List[str] = []

        for name in name_strs:
            self.names.append(name)

    @classmethod
    def from_name(cls, name: str) -> 'Note':
        assert len(name.strip()) > 0
        name_upper = name[0].upper() if len(
            name) == 1 else name[0].upper() + name[1]
        for note in NOTES:
            if name_upper in note.names:
                return note
        else:
            raise AssertionError(f'Invalid note: {name}')

    @classmethod
    def with_distance(cls, base: 'Note', distance: int) -> 'Note':
        note_idx = NOTES.index(base)
        new_idx = (note_idx + distance) % _NUM_NOTES

        return NOTES[new_idx]

    @classmethod
    def from_position(cls, position: int) -> 'Note':
        assert position > 0
        assert position < _NUM_NOTES

        return NOTES[position]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Note):
            return False
        for other_name in other.names:
            for self_name in self.names:
                if other_name == self_name:
                    return True
        return False

    def __str__(self):
        s = ' or '.join(self.names)
        return s


NOTES.extend([
    Note('A'),
    Note('A#', 'Bb'),
    Note('B'),
    Note('C'),
    Note('C#', 'Db'),
    Note('D'),
    Note('D#', 'Eb'),
    Note('E'),
    Note('F'),
    Note('F#', 'Gb'),
    Note('G'),
    Note('G#', 'Ab')
])
