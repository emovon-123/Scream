# PyAudio Installation Guide

If the game prompts that PyAudio installation failed, please follow these steps:

## Windows Users

### Method 1: Using pipwin (Recommended)

```bash
pip install pipwin
pipwin install pyaudio
```

### Method 2: Using wheel files

1. Download the wheel file for your version from [PyPI](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
   - Python 3.8: `PyAudio‑0.2.13‑cp38‑cp38‑win_amd64.whl`
   - Python 3.9: `PyAudio‑0.2.13‑cp39‑cp39‑win_amd64.whl`
   - Python 3.10: `PyAudio‑0.2.13‑cp310‑cp310‑win_amd64.whl`
   - Python 3.11: `PyAudio‑0.2.13‑cp311‑cp311‑win_amd64.whl`

2. Run in the directory where the file was downloaded:
```bash
pip install PyAudio‑0.2.13‑cp38‑cp38‑win_amd64.whl
```
(Please replace the filename with the actual file you downloaded)

### Method 3: Using conda (if using Anaconda)

```bash
conda install pyaudio
```

## MacOS Users

First install PortAudio:
```bash
brew install portaudio
```

Then install PyAudio:
```bash
pip install pyaudio
```

## Linux Users

Ubuntu/Debian:
```bash
sudo apt-get install portaudio19-dev python-pyaudio
```

Fedora:
```bash
sudo dnf install portaudio-devel python-pyaudio
```

Arch Linux:
```bash
sudo pacman -S portaudio python-pyaudio
```

## Tips

**Even if PyAudio installation fails, you can still play the game using keyboard control (Spacebar)!**

The game is designed to automatically downgrade to keyboard control mode when PyAudio is unavailable, so you can still enjoy the game even without voice input functionality.

## Verify Installation

After successful installation, you can verify:

```bash
python -c "import pyaudio; print('PyAudio installed successfully!')"
```

If it displays "PyAudio installed successfully!", then the installation is correct.
