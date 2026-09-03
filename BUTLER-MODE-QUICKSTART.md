# Butler Mode Quick Start (Windows)

## First-Time Setup

```bash
cd d:\Ultron

# Run the interactive setup
butler setup
```

Or run directly:
```bash
venv\Scripts\python.exe butler-setup.py
```

This will:
- ✓ Audition Windows TTS voices
- ✓ Pick your butler voice (save to .voice-config)
- ✓ Test screenshot system
- ✓ Test pointer system
- ✓ Test Notepad integration
- ✓ Test voice narration
- ✓ Test quiet/narrate modes
- ✓ Test mouse control

## After Setup: Using Butler Mode

### Finding Things (Automatic)
```
User: "Where do I click to...?"
↓
Assistant: (automatically)
  python screen-guide.py shot          → Take screenshot
  Look at screen-guide/latest.png      → Analyze it
  python screen-guide.py point X Y     → Draw arrow
  "Right there, sir."                  → Speak & answer
```

### Taking Over ("take over and...")
```
User: "take over and open Notes"
↓
Assistant:
  1. Take screenshot
  2. Show plan (3-6 steps)
  3. Wait for "go"
  4. Execute step by step with voice commentary
  5. Show result after each step
  6. Stop when user says "stop"
```

### Voice Control
```
quiet       → Silent mode (no voice output)
narrate     → Enable voice (resume butler commentary)
```

---

## File Locations

```
d:\Ultron\
├── screen-guide\           # Screenshots saved here
│   └── latest.png
├── screen-guide.py         # Screenshot + arrow tool
├── voice.py                # Voice control
├── win-control.py          # Mouse/keyboard control
├── butler-setup.py         # Setup harness (run this first!)
└── CLAUDE.md              # This documentation
```

---

## Troubleshooting

**"Permission denied" errors**
→ Run PowerShell as Administrator if you encounter permission issues

**"say" or "screencapture" not found**
→ These are macOS commands. You're on Windows—use the Windows versions in CLAUDE.md

**Arrow not visible in image viewer**
→ Make sure screen-guide/latest.png exists and Pillow is installed

**No TTS voices available**
→ Check Windows Settings > Time & Language > Speech for installed voices

---

## All Commands Reference

```bash
# Screenshots
butler shot                    # Capture screen
butler point 50 50 "Button"   # Draw arrow at 50%, 50%

# Voice
butler voice audition         # Listen to voices
butler voice speak "Text"     # Speak now
butler voice set VOICE_ID     # Set butler voice
butler voice quiet            # Silent mode
butler voice narrate          # Enable voice
butler voice status           # Check settings

# Mouse control
butler move 100 200           # Move mouse
butler click 100 200          # Click
butler type "hello"           # Type text
butler key return             # Press key
butler delay 2                # Wait 2 seconds

# Setup
butler setup                  # Run setup harness
butler help                   # Show help
```

---

## Important Notes

✓ **All commands run on Windows** using:
- PIL/ImageGrab for screenshots
- pyttsx3 for Windows TTS
- pyautogui for mouse/keyboard control
- Default Windows image viewer

---

**Ready?** Run: `venv\Scripts\python.exe butler-setup.py`
