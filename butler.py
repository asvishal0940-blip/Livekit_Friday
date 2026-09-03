#!/usr/bin/env python3
"""
Butler Mode Master CLI
Unified interface for all butler functions.

Usage:
  butler.py shot                           - Take screenshot
  butler.py point X Y "LABEL"              - Draw arrow at coordinates
  butler.py voice audition                 - Audition TTS voices
  butler.py voice speak "Text"             - Speak text
  butler.py voice set VOICE_ID             - Set butler voice
  butler.py voice quiet                    - Silent mode
  butler.py voice narrate                  - Resume narration
  butler.py voice status                   - Check voice settings
  butler.py click X Y [button] [clicks]    - Click at coordinates
  butler.py move X Y                       - Move mouse
  butler.py type "Text"                    - Type text
  butler.py key KEYNAME                    - Press key
  butler.py delay N                        - Wait N seconds
  butler.py help                           - Show this help
"""

import sys
import os
from pathlib import Path
import importlib.util

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Load modules with hyphenated names using importlib
def load_module(module_name, file_name):
    spec = importlib.util.spec_from_file_location(module_name, Path(__file__).parent / file_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

try:
    screen_guide = load_module("screen_guide", "screen-guide.py")
    voice = load_module("voice", "voice.py")
    win_control = load_module("win_control", "win-control.py")
except Exception as e:
    print(f"[ERROR] Failed to import modules: {e}")
    sys.exit(1)


def show_help():
    """Display help text."""
    print(__doc__)


def show_quick_help():
    """Display quick help for main commands."""
    print("""
Butler Mode - Quick Help
========================

SCREENSHOT & POINTING:
  butler shot                      - Capture screen
  butler point 50 50 "Button"      - Point at location with label

VOICE:
  butler voice audition            - Listen to voices
  butler voice speak "Text"        - Speak immediately
  butler voice set VOICE_ID        - Set butler voice
  butler voice quiet               - Silence
  butler voice narrate             - Resume voice

MOUSE & KEYBOARD:
  butler click 100 200             - Click
  butler move 100 200              - Move mouse
  butler type "hello"              - Type text
  butler key return                - Press key
  butler delay 2                   - Wait 2 seconds

UTILITY:
  butler setup                     - Run setup harness
  butler help                      - Full help

Examples:
  butler point 50 50 "Menu"
  butler click 500 300
  butler voice speak "Right there, sir."
  butler type "Hello World"
    """)


def route_command(args):
    """Route command to appropriate module."""
    if not args:
        show_quick_help()
        return True
    
    command = args[0].lower()
    
    # SCREENSHOT & POINTING
    if command == "shot":
        screen_guide.shot()
        return True
    
    elif command == "point":
        if len(args) < 4:
            print("Usage: butler point X Y \"LABEL\"")
            return False
        try:
            x = float(args[1])
            y = float(args[2])
            label = " ".join(args[3:])
            screen_guide.point(x, y, label)
            return True
        except ValueError:
            print("[ERROR] X and Y must be numbers (0-100)")
            return False
    
    # VOICE CONTROL
    elif command == "voice":
        if len(args) < 2:
            print("Usage: butler voice [audition|speak|set|quiet|narrate|status]")
            return False
        
        subcommand = args[1].lower()
        
        if subcommand == "audition":
            voice.audition_voices()
            return True
        
        elif subcommand == "speak":
            if len(args) < 3:
                print("Usage: butler voice speak \"Text\"")
                return False
            text = " ".join(args[2:])
            voice.speak(text, force=True)
            return True
        
        elif subcommand == "set":
            if len(args) < 3:
                print("Usage: butler voice set VOICE_ID")
                return False
            voice_id = args[2]
            voice.set_butler_voice(voice_id)
            print(f"[OK] Butler voice set to: {voice_id}")
            return True
        
        elif subcommand == "quiet":
            voice.set_quiet_mode(True)
            print("[OK] Quiet mode enabled")
            return True
        
        elif subcommand == "narrate":
            voice.set_quiet_mode(False)
            print("[OK] Narration mode enabled")
            voice.speak("Narration enabled, sir.")
            return True
        
        elif subcommand == "status":
            butler_voice = voice.get_butler_voice()
            quiet = voice.is_quiet_mode()
            mode_str = "QUIET" if quiet else "NARRATING"
            print(f"Voice: {butler_voice}")
            print(f"Mode: {mode_str}")
            return True
        
        else:
            print(f"[ERROR] Unknown voice subcommand: {subcommand}")
            return False
    
    # MOUSE & KEYBOARD
    elif command == "click":
        if len(args) < 3:
            print("Usage: butler click X Y [button] [clicks]")
            return False
        try:
            x, y = int(args[1]), int(args[2])
            button = args[3] if len(args) > 3 else "left"
            clicks = int(args[4]) if len(args) > 4 else 1
            win_control.click(x, y, button=button, clicks=clicks)
            return True
        except (ValueError, IndexError):
            print("[ERROR] Invalid arguments for click")
            return False
    
    elif command == "move":
        if len(args) < 3:
            print("Usage: butler move X Y")
            return False
        try:
            x, y = int(args[1]), int(args[2])
            win_control.move(x, y)
            return True
        except ValueError:
            print("[ERROR] X and Y must be numbers")
            return False
    
    elif command == "type":
        if len(args) < 2:
            print("Usage: butler type \"Text\"")
            return False
        text = " ".join(args[1:])
        win_control.type_text(text)
        return True
    
    elif command == "key":
        if len(args) < 2:
            print("Usage: butler key KEYNAME")
            return False
        key_name = args[1]
        win_control.press_key(key_name)
        return True
    
    elif command == "delay":
        if len(args) < 2:
            print("Usage: butler delay SECONDS")
            return False
        try:
            seconds = float(args[1])
            win_control.delay(seconds)
            return True
        except ValueError:
            print("[ERROR] Delay must be a number")
            return False
    
    # UTILITY
    elif command == "setup":
        import subprocess
        subprocess.run([sys.executable, "butler-setup.py"], cwd=Path(__file__).parent)
        return True
    
    elif command == "help":
        show_help()
        return True
    
    elif command == "--help" or command == "-h":
        show_help()
        return True
    
    else:
        print(f"[ERROR] Unknown command: {command}")
        print("Type 'butler help' for full help or 'butler' for quick help")
        return False


def main():
    """Main entry point."""
    try:
        success = route_command(sys.argv[1:])
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[OK] Stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
