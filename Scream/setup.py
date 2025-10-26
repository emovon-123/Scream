"""
Scream game installation script
"""

from setuptools import setup, find_packages

setup(
    name="scream-game",
    version="1.0.0",
    description="Voice-controlled side-scrolling jumping game",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "pygame==2.5.2",
        "numpy==1.24.3",
        "pyaudio==0.2.13",
    ],
    python_requires=">=3.8",
)
