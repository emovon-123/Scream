# Scream - Voice-Controlled Jumping Game

A voice-controlled side-scrolling jumping game inspired by Flappy Bird, featuring a black and white art style.

## Game Features

- 🎤 **Voice Control**: Control character jumping through microphone detection
- 🖱️ **Mouse Interaction**: Click START to begin, click RESTART to restart
- ⚡ **Progressive Speed**: Higher scores lead to faster movement speed
- 📊 **Clean UI**: Score and volume displayed in the top-right corner
- 🎨 **Black & White Style**: Minimalist black and white art design
- 🎮 **Classic Gameplay**: Flappy Bird-like side-scrolling jumping experience

## Installation

### Prerequisites
- Python 3.8 or higher
- Microphone device (optional, keyboard control still available if not available)

### Windows Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

**Important Notes**:
- If PyAudio installation fails, the game can still run normally with **keyboard control (Spacebar)**
- To use voice control on Windows, try:
```bash
pip install pipwin
pipwin install pyaudio
```
- Detailed PyAudio installation guide: [INSTALL_PYAUDIO.md](INSTALL_PYAUDIO.md)

## Gameplay

### Starting the Game

After installing dependencies, run the game:
```bash
python game.py
```

### Controls

#### Starting the Game
- **Click START button** or press **Spacebar**

#### Game Control
- **Voice Control** (if available): Shout loudly to make the character jump
- **Spacebar**: Jump

#### Restarting
- **Click RESTART button** or press **R key**

#### Exiting the Game
- **ESC key**

### Game Mechanics

- **Progressive Speed**: Initial speed 5 pixels/frame, increases 0.1 pixels/frame per point
- **Scoring Rules**: Each obstacle passed grants 1 point
- **Higher Score = Faster Speed**: Difficulty gradually increases

## Configuration

Default window size: 800x600
Adjust by modifying `WINDOW_WIDTH` and `WINDOW_HEIGHT` in `game.py`.

## Sound Threshold

If the default sound threshold doesn't suit your environment, modify the `SOUND_THRESHOLD` variable in `game.py`.

## File Structure

```
Scream/
├── game.py                # Main game file
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── setup.py              # Installation script
├── CONTRIBUTING.md       # Contribution guide
├── INSTALL_PYAUDIO.md    # PyAudio installation guide
└── Character/            # Game assets
    ├── gifs/
    ├── misc/
    └── sheets/
```

## Troubleshooting

### PyAudio Installation Issues

**Windows**:
```bash
pip install pipwin
pipwin install pyaudio
```

**MacOS**:
```bash
brew install portaudio
pip install pyaudio
```

**Linux**:
```bash
sudo apt-get install portaudio19-dev python-pyaudio
pip install pyaudio
```

### Microphone Permissions

Ensure the game has permission to access the microphone. Check microphone permissions in Windows settings.

## Contributing

Issues and Pull Requests are welcome!

## License

This project is for learning and research purposes only.
