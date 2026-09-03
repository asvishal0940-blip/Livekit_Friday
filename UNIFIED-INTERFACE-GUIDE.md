# Butler Unified Interface Guide

## Overview

All butler mode commands are now accessible through a single unified interface via `butler.py`. This eliminates the need to remember individual module names and command syntax.

## Quick Start

### Option 1: Direct Python (Always Works)
```powershell
venv\Scripts\python.exe butler.py [command] [args]
```

### Option 2: Batch Wrapper (Recommended for PowerShell)
```powershell
.\butler.bat [command] [args]
```

### Option 3: Add to PATH (System-Wide Access)
1. Open Environment Variables (Settings → Environment Variables)
2. Add `d:\Ultron` to your PATH
3. Then use: `butler.bat command` or `butler.bat` from anywhere

## Complete Command Reference

### Screenshots & Pointing

```bash
# Take a screenshot
butler.py shot

# Draw an arrow pointing at coordinates (percentages: 0-100)
butler.py point 50 50 "Save Button"
butler.py point 75 20 "Close Button"
butler.py point 25 98 "Taskbar"
```

### Voice Control

```bash
# Audition available TTS voices
butler.py voice audition

# Speak text immediately
butler.py voice speak "Hello, this is a test"

# Set the preferred butler voice
butler.py voice set VOICE_ID

# Enable/disable voice narration
butler.py voice quiet      # Silent mode
butler.py voice narrate    # Resume voice

# Check current voice and mode
butler.py voice status
```

### Mouse & Keyboard Control

```bash
# Move mouse to pixel coordinates
butler.py move 960 540

# Click at coordinates
butler.py click 500 300           # Left click (default)
butler.py click 500 300 right     # Right click
butler.py click 500 300 left 2    # Double-click

# Type text
butler.py type "Hello World"

# Press keys
butler.py key return              # Enter key
butler.py key escape              # Escape key
butler.py key tab                 # Tab key
butler.py key space               # Space bar
butler.py key up                  # Arrow keys
butler.py key f1                  # Function keys

# Wait/delay
butler.py delay 2                 # Wait 2 seconds
butler.py delay 0.5               # Wait 0.5 seconds
```

### System Commands

```bash
# Run interactive setup
butler.py setup

# Show help
butler.py help
```

## Real-World Workflow Examples

### Example 1: Screenshot and Point
```bash
# Take screenshot
butler.py shot

# Look at D:\Ultron\screen-guide\latest.png
# Identify element location as percentage

# Point at it
butler.py point 75 50 "Submit Button"
```

### Example 2: Automate a Form Fill
```bash
# Click on first field
butler.py click 300 200

# Type name
butler.py type "John Doe"

# Move to next field
butler.py key tab

# Type email
butler.py type "john@example.com"

# Press submit
butler.py key return
```

### Example 3: Test and Verify
```bash
# Enable narration
butler.py voice narrate

# Move to element and take screenshot
butler.py move 500 400
butler.py delay 0.5
butler.py shot

# Point at area of interest
butler.py point 50 50 "Test Element"

# Verify voice is working
butler.py voice speak "Test complete"
```

## Wrapper Scripts

### butler.bat (Windows Batch)
- **Location:** `d:\Ultron\butler.bat`
- **Usage:** `.\butler.bat command` (from PowerShell)
- **Advantage:** No Python version syntax needed
- **Note:** Requires `.\ ` prefix in PowerShell unless in PATH

### butler.py (Python Master)
- **Location:** `d:\Ultron\butler.py`
- **Usage:** `python butler.py command` or `venv\Scripts\python.exe butler.py command`
- **Advantage:** Always works, no wrapper dependencies

### butler.ps1 (PowerShell)
- **Location:** `d:\Ultron\butler.ps1`
- **Usage:** `.\butler.ps1 command`
- **Note:** Requires PowerShell execution policy bypass (see Troubleshooting)

## Troubleshooting

### PowerShell Execution Policy Error
**Error:** "cannot be loaded because running scripts is disabled"

**Solution 1: Use Batch Wrapper**
```powershell
.\butler.bat command
```

**Solution 2: Bypass for Single Execution**
```powershell
pwsh -ExecutionPolicy Bypass -File butler.ps1 command
```

**Solution 3: Permanently Enable Scripts (Admin Required)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Command Not Found
**Error:** "butler.bat is not recognized"

**Solution 1: Use Full Path**
```powershell
venv\Scripts\python.exe butler.py command
```

**Solution 2: Add to PATH**
- Open Settings → Environment Variables
- Edit PATH environment variable
- Add: `d:\Ultron`
- Restart PowerShell

**Solution 3: Use .\ Prefix**
```powershell
.\butler.bat command  # From d:\Ultron directory
```

### Voice Not Speaking
**Check Status:**
```bash
butler.py voice status
```

**If mode is QUIET:**
```bash
butler.py voice narrate
```

**If no voice is set:**
```bash
butler.py voice audition      # Pick a voice
butler.py voice set VOICE_ID  # Set it (copy from audition output)
```

## Advanced Usage

### Batch Commands from Script
Create a PowerShell script to run multiple butler commands:

```powershell
# my-task.ps1
$butler = "venv\Scripts\python.exe butler.py"

& $butler voice narrate
& $butler shot
& $butler point 50 50 "Target"
& $butler click 500 300
& $butler delay 1
& $butler shot
```

Run with:
```bash
powershell -ExecutionPolicy Bypass -File my-task.ps1
```

### Keyboard Shortcuts
Supported key names for `butler.py key`:
- Letters: `a` - `z` (lowercase)
- Numbers: `0` - `9`
- Arrow keys: `up`, `down`, `left`, `right`
- Special: `return`, `tab`, `escape`, `space`, `delete`, `backspace`
- Function: `f1` - `f12`
- Modifiers: Can combine with shift (e.g., `shift+a` for capital A)

### Mouse Button Clicks
```bash
# Left (default)
butler.py click 500 300

# Right
butler.py click 500 300 right

# Middle
butler.py click 500 300 middle

# Multiple clicks
butler.py click 500 300 left 2    # Double-click
butler.py click 500 300 left 3    # Triple-click
```

## Legacy Direct Module Access

While unified interface is recommended, you can still call individual modules:

```bash
# Screenshots
venv\Scripts\python.exe screen-guide.py shot
venv\Scripts\python.exe screen-guide.py point 50 50 "Label"

# Voice
venv\Scripts\python.exe voice.py audition
venv\Scripts\python.exe voice.py speak "Text"

# Mouse/Keyboard
venv\Scripts\python.exe win-control.py move 500 300
venv\Scripts\python.exe win-control.py click 500 300
```

## Getting Help

```bash
# Show full command reference
butler.py help

# Show voice status
butler.py voice status

# Run interactive setup with tests
butler.py setup
```

---

**Status:** Unified interface fully functional and tested. All butler commands accessible via single entry point.

**Version:** 1.0 (Windows-optimized, Python 3.12)

**Last Updated:** 2025
