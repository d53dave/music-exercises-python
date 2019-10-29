import click

from music_exercises.intervals import Intervals


@click.command()
@click.option('-i', '--intervals', 'intervals', type=str)
def cli(intervals):
    game = Intervals(intervals)
    game.play()


if __name__ == '__main__':
    cli(None)
