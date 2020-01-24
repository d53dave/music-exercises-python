import click

from music_exercises.intervals import Intervals
from music_exercises.accidentals import Accidentals


@click.group()
def cli():
    pass


@cli.command()
@click.option('-r', '--range', 'range', type=str)
def intervals(range):
    game = Intervals(range)
    game.play()


@cli.command()
@click.option('--notes', type=bool, is_flag=True, default=False)
def accidentals(notes):
    game = Accidentals()
    game.play(notes)


if __name__ == '__main__':
    cli()
