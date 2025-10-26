"""
Test microphone and sound detection functionality
Run this script to diagnose microphone issues
"""

try:
    import pyaudio
    import numpy as np
    
    print("PyAudio installed")
    
    # Configuration
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    print("Initializing microphone...")
    
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    
    print("\nMicrophone initialized successfully!")
    print("Listening to microphone input...")
    print("Please speak into the microphone and observe the volume value")
    print("When the volume value turns green, it means the trigger threshold has been exceeded\n")
    
    import time
    SOUND_THRESHOLD = 300
    
    try:
        for i in range(100):  # Listen for about 5 seconds
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_data).mean()
            
            # Calculate color
            if volume > SOUND_THRESHOLD:
                status = "\033[92mTRIGGERED!\033[0m"  # Green
            else:
                status = "\033[90mNot triggered\033[0m"  # Gray
            
            print(f"\rVolume: {int(volume):4d} / {SOUND_THRESHOLD} {status}", end="")
            time.sleep(0.05)
        
        print("\n\nTest completed!")
        print("\nDiagnosis results:")
        print("1. If volume value is always 0, check microphone permissions")
        print("2. If volume value is very low (<100), move closer to microphone or increase volume")
        print("3. If volume value is normal but doesn't trigger, lower SOUND_THRESHOLD")
        print("4. If you see 'TRIGGERED!', the microphone is working properly")
        
    except KeyboardInterrupt:
        print("\nTest interrupted")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
    
except ImportError:
    print("Error: PyAudio not installed")
    print("Please run: pip install pyaudio")
    print("\nIf installation fails on Windows, try:")
    print("  pip install pipwin")
    print("  pipwin install pyaudio")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nPossible causes:")
    print("1. Microphone not connected")
    print("2. Microphone permissions not granted")
    print("3. Another program is using the microphone")
