import re
from setuptools import setup, find_packages

setup(
    name="Tetris-in-Python",
    version="0.0.1",
    description="This is a Tetris game built using python and pygame.",
    url="https://github.com/ernum/Tetris-In-Python",
    author="hostedt, jerikso and umeh",
    packages=find_packages(where="."),
    package_data={
        "Tetris.Sound.SoundEffect": ["*.wav"],
        "Tetris.Sound.Soundtrack": ["*.ogg"],
        "Tetris.images": ["*.png"],
        "Tetris.fonts": ["*.ttf"],
    },
    include_package_data=True,
    install_requires=[
        'pygame'
    ],
    python_requires='>=3'
)
