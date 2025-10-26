# Voice Control Guide

## How to Check if Microphone Works

While running the game, the top-left corner displays:
- **Volume**: Current microphone-detected volume value
- **Threshold**: Sound threshold for triggering jumps
- **Volume Bar**: Real-time volume level display

## Volume Bar Guide

- **Gray Background**: Represents volume bar range
- **Red/Green**: Current volume (red = below threshold, green = above threshold)
- **White Vertical Line**: Trigger threshold position

## Adjusting Sound Threshold

If you find you need to shout louder to trigger, modify the `SOUND_THRESHOLD` value in `game.py`:

```python
SOUND_THRESHOLD = 800  # Lower this value to trigger more easily (e.g., change to 500)
```

**Recommended Values**:
- Quiet environment: 500-800
- Noisy environment: 1000-1500
- Requires loud shouting: 1500+

## Common Issues

### 1. Volume Bar Not Moving (Shows 0)
**Possible Causes**:
- Microphone not connected or damaged
- Windows microphone permissions not granted
- PyAudio not properly installed

**Solutions**:
1. Check Windows microphone settings
2. Ensure microphone permissions are enabled
3. Reinstall PyAudio (refer to INSTALL_PYAUDIO.md)

### 2. Volume Always Low (< 100)
**Possible Causes**:
- Microphone too far from mouth
- Microphone volume settings too low
- Environment too quiet

**Solutions**:
1. Speak closer to the microphone
2. Increase microphone volume in Windows settings
3. Lower the `SOUND_THRESHOLD` value

### 3. Volume Exceeds Threshold But Doesn't Trigger
**Possible Causes**:
- Sound detection frequency issues

**Solutions**:
1. Speak more continuously
2. Slightly increase `SOUND_THRESHOLD` to avoid false triggers

## Testing Microphone

1. Run the game
2. After starting the game, check the top-left corner
3. Speak into the microphone and observe if the volume value changes
4. If the volume value changes, the microphone is working properly
5. Adjust `SOUND_THRESHOLD` to a suitable level

## Best Practices

- **Quiet Environment**: Set threshold to 500-800
- **Normal Environment**: Set threshold to 800-1200
- **Noisy Environment**: Set threshold to 1200-2000
- In actual use, adjust to the threshold that works best for you based on the volume bar


