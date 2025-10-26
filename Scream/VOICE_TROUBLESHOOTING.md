# Voice Control Troubleshooting

## Quick Diagnosis

Run the test script:
```bash
python test_microphone.py
```

Observe the output. If you see:
- **Volume value always 0** → Microphone not working
- **Volume value very low (<100)** → Microphone volume too low
- **Volume value normal but doesn't turn green** → Threshold too high

## Detailed Steps

### 1. Verify PyAudio is Installed

```bash
python -c "import pyaudio; print('PyAudio installed')"
```

If error occurs, install PyAudio:
```bash
pip install pyaudio
```

If installation fails on Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

### 2. Check Microphone Permissions

**Windows**:
1. Open Settings → Privacy → Microphone
2. Ensure "Allow apps to access microphone" is enabled
3. Ensure command line/Python has permission

**macOS**:
1. System Preferences → Security & Privacy → Microphone
2. Allow Terminal/Python to access microphone

### 3. Check System Microphone Volume

**Windows**:
- Right-click taskbar volume icon → Recording Devices
- Select your microphone → Properties → Levels
- Ensure volume is not 0

**macOS**:
- System Preferences → Sound → Input
- Adjust input volume slider

### 4. Adjust Sound Threshold

If microphone works but game doesn't respond, edit `game.py`:

```python
SOUND_THRESHOLD = 300  # Lower this value to trigger more easily
```

**Recommended Values**:
- Quiet environment: 200-300
- Normal environment: 300-500
- Noisy environment: 500-800

### 5. Use In-Game Volume Display

After running the game, observe the top-right corner:
- **VOL: 0/300** (yellow) → Microphone not working
- **VOL: 50/300** (yellow) → Volume too low, need to get closer or increase volume
- **VOL: 400/300** (green) → Trigger successful

## Common Questions

### Q: Volume display always shows 0
**A**: 
1. Check Windows microphone permissions
2. Confirm microphone is connected
3. Run `test_microphone.py` for diagnosis

### Q: Volume value too low, how to increase?
**A**: 
1. Speak closer to the microphone
2. Increase microphone gain in Windows settings
3. Lower the `SOUND_THRESHOLD` value

### Q: Volume value normal but doesn't trigger
**A**: 
1. Check top-right corner showing "VOL: xxx/300"
2. If xxx > 300 but doesn't turn green, may be detection frequency issue
3. Try speaking continuously instead of brief shouts

### Q: PyAudio installation fails
**A**: 
Windows users can use pipwin:
```bash
pip install pipwin
pipwin install pyaudio
```

Or download wheel file:
1. Visit https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Download wheel file for your version
3. pip install the downloaded file

## Alternative Solutions

If voice control cannot be used, the game **fully supports keyboard control**:
- **Spacebar** to jump
- Click START to begin
- Click RESTART to restart

Even in "keyboard-only mode", the game experience is identical!


