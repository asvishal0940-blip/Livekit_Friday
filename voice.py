#!/usr/bin/env python3
"""
Voice Controller for butler mode (Windows)
Handles voice narration with quiet/narrate modes using pyttsx3.
"""

import sys
from pathlib import Path

try:
    import pyttsx3
    HAS_TTS = True
except ImportError:
    HAS_TTS = False

# Configuration file for storing voice preference
CONFIG_FILE = Path(__file__).parent / ".voice-config"
DEFAULT_VOICE = "default"

# Global engine instance
_engine = None

def _get_engine():
    """Get or create the pyttsx3 engine."""
    global _engine
    if _engine is None and HAS_TTS:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', 150)  # Slower, more butler-like
    return _engine

def get_butler_voice():
    """Get the configured butler voice, or use default."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return f.read().strip()
    return DEFAULT_VOICE

def set_butler_voice(voice_name):
    """Save the butler voice choice."""
    with open(CONFIG_FILE, 'w') as f:
        f.write(voice_name)

def is_quiet_mode():
    """Check if quiet mode is enabled."""
    quiet_file = Path(__file__).parent / ".quiet-mode"
    return quiet_file.exists()

def set_quiet_mode(enabled):
    """Enable/disable quiet mode."""
    quiet_file = Path(__file__).parent / ".quiet-mode"
    if enabled:
        quiet_file.touch()
    else:
        quiet_file.unlink(missing_ok=True)

def speak(text, force=False):
    """
    Speak text using Windows pyttsx3.
    force=True will speak even in quiet mode.
    """
    if not HAS_TTS:
        return
    
    if is_quiet_mode() and not force:
        return
    
    try:
        engine = _get_engine()
        if engine:
            voice_id = get_butler_voice()
            if voice_id != "default":
                engine.setProperty('voice', voice_id)
            engine.say(text)
            engine.runAndWait()
    except Exception:
        # Silently fail if TTS not available
        pass

def get_available_voices():
    """Get list of available TTS voices on Windows."""
    if not HAS_TTS:
        return []
    
    try:
        engine = _get_engine()
        if engine:
            return [v.id for v in engine.getProperty('voices')]
    except Exception:
        pass
    
    return []

def audition_voices():
    """Audition available Windows voices."""
    if not HAS_TTS:
        print("Error: pyttsx3 not installed")
        return []
    
    print("Auditioning Windows TTS voices...\n")
    
    try:
        voices = get_available_voices()
        
        if not voices:
            print("No voices found. Install Windows TTS voices in Settings.")
            return []
        
        print(f"Found {len(voices)} voice(s). Testing...\n")
        
        engine = _get_engine()
        
        for i, voice_id in enumerate(voices, 1):
            engine.setProperty('voice', voice_id)
            print(f"[Voice {i}] {voice_id}")
            engine.say("Right there, sir.")
            engine.runAndWait()
            print()
        
        return voices
        
    except Exception as e:
        print(f"Error auditioning voices: {e}")
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: python voice.py [audition|speak TEXT|quiet|narrate|status|set-voice VOICE_ID]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "audition":
        audition_voices()
    
    elif command == "speak":
        if len(sys.argv) < 3:
            print("Usage: python voice.py speak TEXT")
            sys.exit(1)
        text = " ".join(sys.argv[2:])
        speak(text, force=True)  # Force speak regardless of quiet mode
    
    elif command == "quiet":
        set_quiet_mode(True)
        print("[OK] Quiet mode enabled")
    
    elif command == "narrate":
        set_quiet_mode(False)
        print("[OK] Narration mode enabled")
        speak("Narration enabled, sir.")
    
    elif command == "status":
        voice = get_butler_voice()
        quiet = is_quiet_mode()
        mode_str = "QUIET" if quiet else "NARRATING"
        print(f"Voice: {voice}")
        print(f"Mode: {mode_str}")
        print(f"TTS Available: {'Yes' if HAS_TTS else 'No'}")
    
    elif command == "set-voice":
        if len(sys.argv) < 3:
            print("Usage: python voice.py set-voice VOICE_ID")
            sys.exit(1)
        voice_id = sys.argv[2]
        set_butler_voice(voice_id)
        print(f"[OK] Butler voice set to: {voice_id}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
