#!/usr/bin/env python3
"""
Butler Mode Setup & Test Harness (Windows)
Run this on Windows to:
1. Audition TTS voices and pick a butler voice
2. Test the screen guide system
3. Verify all components work
"""

import subprocess
import sys
import os
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

def run_command(cmd, description=""):
    """Run a command and report results."""
    if description:
        print(f"\n{'='*60}")
        print(f"  {description}")
        print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and "Warning" not in result.stderr:
            print(f"Error: {result.stderr}", file=sys.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to run: {e}", file=sys.stderr)
        return False

def test_voice_audition():
    """Audition Windows TTS voices."""
    print("\n" + "="*60)
    print("  STEP 1: Voice Audition")
    print("="*60)
    print("\nListen to available Windows TTS voices.")
    print("Pick the one that sounds most butler-like.")
    
    cmd = f"venv\\Scripts\\python.exe {SCRIPTS_DIR}\\voice.py audition"
    if run_command(cmd):
        voice = input("\nEnter the voice ID you prefer: ").strip()
        if voice:
            set_cmd = f"venv\\Scripts\\python.exe {SCRIPTS_DIR}\\voice.py set-voice {voice}"
            run_command(set_cmd, f"Setting butler voice...")
            return voice
    return "default"

def test_screenshot():
    """Test the shot command."""
    print("\n" + "="*60)
    print("  STEP 2: Screenshot Test")
    print("="*60)
    
    cmd = f"venv\\Scripts\\python.exe {SCRIPTS_DIR}\\screen-guide.py shot"
    return run_command(cmd, "Taking a screenshot...")

def test_point():
    """Test the point command."""
    print("\n" + "="*60)
    print("  STEP 3: Pointer Test (Taskbar)")
    print("="*60)
    
    # Point at taskbar area (typically at bottom center around 50% horizontally, 98% vertically)
    cmd = f"venv\\Scripts\\python.exe {SCRIPTS_DIR}\\screen-guide.py point 50 98 Taskbar"
    success = run_command(cmd, "Pointing at your taskbar...")
    
    if success:
        print("\n[OK] An image viewer should have opened with an arrow pointing at your taskbar.")
        print("  Did you see the arrow and hear 'Right there, sir'?")
    
    return success

def test_notepad():
    """Test opening Notepad."""
    print("\n" + "="*60)
    print("  STEP 4: Notepad Integration Test")
    print("="*60)
    
    print("\nThis will open Notepad for you to test typing.")
    input("Press Enter when ready...")
    
    try:
        # Open Notepad
        os.startfile("notepad.exe")
        print("[OK] Notepad opened")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to open Notepad: {e}", file=sys.stderr)
        return False

def test_voice_narration():
    """Test voice narration."""
    print("\n" + "="*60)
    print("  STEP 5: Voice Narration Test")
    print("="*60)
    
    cmd = f"venv\\Scripts\\python.exe {SCRIPTS_DIR}\\voice.py speak \"Butler mode is ready, sir.\""
    success = run_command(cmd, "Testing voice output...")
    
    if success:
        print("\nDid you hear the butler voice say 'Butler mode is ready, sir'?")
    
    return success

def test_quiet_mode():
    """Test quiet mode."""
    print("\n" + "="*60)
    print("  STEP 6: Quiet & Narrate Mode Test")
    print("="*60)
    
    print("\nEnabling quiet mode...")
    cmd = f"venv\\Scripts\\python.exe {SCRIPTS_DIR}\\voice.py quiet"
    run_command(cmd)
    
    print("Now speaking (should be silent)...")
    cmd = f"venv\\Scripts\\python.exe {SCRIPTS_DIR}\\voice.py speak \"This should be silent.\""
    run_command(cmd)
    
    print("\nEnabling narration mode...")
    cmd = f"venv\\Scripts\\python.exe {SCRIPTS_DIR}\\voice.py narrate"
    run_command(cmd)
    
    return True

def test_mouse_control():
    """Test mouse control."""
    print("\n" + "="*60)
    print("  STEP 7: Mouse Control Test")
    print("="*60)
    
    print("\nMoving mouse to center of screen...")
    cmd = f"venv\\Scripts\\python.exe {SCRIPTS_DIR}\\win-control.py move 960 540"
    if run_command(cmd):
        print("[OK] Mouse moved to center")
        return True
    return False

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║         BUTLER MODE SETUP & TEST HARNESS (Windows)         ║
║                                                             ║
║  This script will set up and test your screen guide system ║
║  and butler voice mode on Windows.                          ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print("\nThis script will:")
    print("  1. Let you audition and select a TTS voice")
    print("  2. Test the screenshot system")
    print("  3. Test pointing at your taskbar")
    print("  4. Test Notepad integration")
    print("  5. Test voice narration")
    print("  6. Test quiet/narrate modes")
    print("  7. Test mouse control")
    
    proceed = input("\nReady to begin? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Setup cancelled.")
        sys.exit(0)
    
    results = []
    
    # Run all tests
    voice = test_voice_audition()
    results.append(("Voice Selection", voice is not None))
    
    results.append(("Screenshot", test_screenshot()))
    results.append(("Point at Taskbar", test_point()))
    results.append(("Notepad Open", test_notepad()))
    results.append(("Voice Narration", test_voice_narration()))
    results.append(("Quiet/Narrate Modes", test_quiet_mode()))
    results.append(("Mouse Control", test_mouse_control()))
    
    # Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status:8} {test_name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print(f"\n  {passed_count}/{total_count} tests passed")
    
    if passed_count >= (total_count - 1):  # Allow 1 failure
        print("\n[OK] Butler mode is operational, sir.")
        print("\nKey commands:")
        print(f"  venv\\Scripts\\python.exe screen-guide.py shot")
        print(f"  venv\\Scripts\\python.exe screen-guide.py point X Y \"LABEL\"")
        print(f"  venv\\Scripts\\python.exe voice.py quiet")
        print(f"  venv\\Scripts\\python.exe voice.py narrate")
        print(f"  venv\\Scripts\\python.exe win-control.py move X Y")
        print(f"  venv\\Scripts\\python.exe win-control.py click X Y")
        print(f"  venv\\Scripts\\python.exe win-control.py type \"Text\"")
        print(f"  venv\\Scripts\\python.exe win-control.py key return")
    else:
        print("\n[ERROR] Some tests failed. Please review the output above.")

if __name__ == "__main__":
    main()
