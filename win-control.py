#!/usr/bin/env python3
"""
Windows Control Helper
Controls mouse, clicks, and typing on Windows via pyautogui.

Usage:
  python win-control.py move X Y              - Move mouse to pixel coordinates
  python win-control.py click X Y             - Click at pixel coordinates
  python win-control.py type "Text to type"   - Type text
  python win-control.py key KEYNAME           - Press a key
  python win-control.py delay N               - Wait N seconds
"""

import sys
import time
import pyautogui

# Disable PyAutoGUI safety features (user responsibility)
pyautogui.FAILSAFE = False

# Key name mapping
KEY_MAP = {
    'return': 'enter',
    'enter': 'enter',
    'tab': 'tab',
    'space': 'space',
    'escape': 'esc',
    'esc': 'esc',
    'backspace': 'backspace',
    'delete': 'delete',
    'up': 'up',
    'down': 'down',
    'left': 'left',
    'right': 'right',
    'home': 'home',
    'end': 'end',
    'pageup': 'pageup',
    'pagedown': 'pagedown',
    'f1': 'f1',
    'f2': 'f2',
    'f3': 'f3',
    'f4': 'f4',
    'f5': 'f5',
    'f6': 'f6',
    'f7': 'f7',
    'f8': 'f8',
    'f9': 'f9',
    'f10': 'f10',
    'f11': 'f11',
    'f12': 'f12',
    'insert': 'insert',
    'printscreen': 'printscreen',
    'pause': 'pause',
}

def move(x, y):
    """Move mouse to coordinates."""
    try:
        x, y = int(x), int(y)
        pyautogui.moveTo(x, y, duration=0.5)
        print(f"[OK] Mouse moved to ({x}, {y})")
    except Exception as e:
        print(f"[ERROR] Move failed: {e}", file=sys.stderr)
        sys.exit(1)

def click(x, y, button='left', clicks=1):
    """Click at coordinates."""
    try:
        x, y = int(x), int(y)
        pyautogui.click(x, y, clicks=clicks, button=button)
        print(f"[OK] Clicked at ({x}, {y})")
    except Exception as e:
        print(f"[ERROR] Click failed: {e}", file=sys.stderr)
        sys.exit(1)

def type_text(text):
    """Type text."""
    try:
        # Add small delay between key presses for reliability
        pyautogui.write(text, interval=0.05)
        print(f"[OK] Typed: {text}")
    except Exception as e:
        print(f"[ERROR] Type failed: {e}", file=sys.stderr)
        sys.exit(1)

def press_key(key_name):
    """Press a key."""
    try:
        key_name = key_name.lower()
        key = KEY_MAP.get(key_name, key_name)
        pyautogui.press(key)
        print(f"[OK] Pressed: {key}")
    except Exception as e:
        print(f"[ERROR] Key press failed: {e}", file=sys.stderr)
        sys.exit(1)

def delay(seconds):
    """Wait for N seconds."""
    try:
        seconds = float(seconds)
        time.sleep(seconds)
        print(f"[OK] Waited {seconds} seconds")
    except Exception as e:
        print(f"[ERROR] Delay failed: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python win-control.py [move|click|type|key|delay] [args...]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "move":
        if len(sys.argv) < 4:
            print("Usage: python win-control.py move X Y")
            sys.exit(1)
        move(sys.argv[2], sys.argv[3])
    
    elif command == "click":
        if len(sys.argv) < 4:
            print("Usage: python win-control.py click X Y [button] [clicks]")
            sys.exit(1)
        button = sys.argv[4] if len(sys.argv) > 4 else 'left'
        clicks = int(sys.argv[5]) if len(sys.argv) > 5 else 1
        click(sys.argv[2], sys.argv[3], button=button, clicks=clicks)
    
    elif command == "type":
        if len(sys.argv) < 3:
            print("Usage: python win-control.py type \"Text\"")
            sys.exit(1)
        text = " ".join(sys.argv[2:])
        type_text(text)
    
    elif command == "key":
        if len(sys.argv) < 3:
            print("Usage: python win-control.py key KEYNAME")
            sys.exit(1)
        press_key(sys.argv[2])
    
    elif command == "delay":
        if len(sys.argv) < 3:
            print("Usage: python win-control.py delay SECONDS")
            sys.exit(1)
        delay(sys.argv[2])
    
    else:
        print(f"[ERROR] Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
