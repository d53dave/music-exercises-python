from setuptools import setup

setup(
    name='music-exercises',
    version='0.1',
    py_modules=['music-exercises'],
    install_requires=[
        'Click', 'music22', 'mido', 'python-rtmidi'
    ],
    entry_points='''
        [console_scripts]
        music-exercises=exercises.cli:cli
    ''',
)
