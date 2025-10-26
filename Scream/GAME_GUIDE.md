# Scream Game Guide

## Game Features

- 🎮 **Click to Start**: Click START button on the cover to enter the game
- 🎯 **Progressive Speed**: Higher scores increase pipe movement speed
- 📊 **Top-Right Display**: Real-time score and volume display
- 🔄 **Click to Restart**: Click RESTART button after game over

## Controls

### Entering the Game
- **Click START** or press **Spacebar** to start the game

### Game Control
- **Shout Loudly**: Use microphone sound control (if available)
- **Spacebar**: Jump (always available)

### Restarting
- **Click RESTART button** or press **R key**

### Exiting the Game
- **ESC key**

## Game Mechanics

### Progressive Speed
- Initial speed: 5 pixels/frame
- Speed increases 0.1 pixels/frame per point scored
- Example: Speed is 6 at 10 points, 7 at 20 points

### Scoring Rules
- Each obstacle passed grants 1 point
- Game ends on collision

## Interface Guide

### Start Screen
- Game title "SCREAM"
- Control hints
- START button

### Game Screen
- **Top-right corner** displays:
  - SCORE: Current score
  - VOL: Volume value (if microphone available)
- Pipe obstacles
- Character

### Game Over Screen
- GAME OVER message
- Final score
- RESTART button

## Volume Display

If microphone is available, top-right shows volume:
- **Yellow**: Volume below threshold (no jump)
- **Green**: Volume reaches threshold (triggers jump)

## System Requirements

- Python 3.8+
- pygame
- numpy
- pyaudio (optional, for voice control)

## Installation

```bash
pip install pygame numpy
pip install pyaudio  # Optional
```

## Running

```bash
python game.py
```


