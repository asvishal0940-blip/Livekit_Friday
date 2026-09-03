#!/bin/bash
# macOS Control Helper
# Controls mouse, clicks, and typing via AppleScript
# Usage:
#   mac-control.sh click X Y              - Click at pixel coordinates
#   mac-control.sh type "Text"            - Type text
#   mac-control.sh key KEYNAME            - Press a key
#   mac-control.sh move X Y               - Move mouse to coordinates

if [[ $# -lt 2 ]]; then
    echo "Usage: mac-control.sh [click|type|key|move] [args...]"
    exit 1
fi

COMMAND=$1
shift

case "$COMMAND" in
    click)
        X=$1
        Y=$2
        osascript <<EOF
set clickX to $X
set clickY to $Y
tell application "System Events"
    click at {clickX, clickY}
end tell
EOF
        ;;
    
    type)
        TEXT="$1"
        # Escape quotes for AppleScript
        TEXT="${TEXT//\"/\\\"}"
        osascript <<EOF
tell application "System Events"
    keystroke "$TEXT"
end tell
EOF
        ;;
    
    key)
        KEY_NAME=$1
        # Map common key names to AppleScript
        case "$KEY_NAME" in
            return|enter) KEY_CODE="return" ;;
            tab) KEY_CODE="tab" ;;
            space) KEY_CODE="space" ;;
            escape|esc) KEY_CODE="escape" ;;
            backspace|delete) KEY_CODE="delete" ;;
            up) KEY_CODE="up arrow" ;;
            down) KEY_CODE="down arrow" ;;
            left) KEY_CODE="left arrow" ;;
            right) KEY_CODE="right arrow" ;;
            home) KEY_CODE="home" ;;
            end) KEY_CODE="end" ;;
            page_up) KEY_CODE="page up" ;;
            page_down) KEY_CODE="page down" ;;
            *) KEY_CODE="$KEY_NAME" ;;
        esac
        
        osascript <<EOF
tell application "System Events"
    key code for key name "$KEY_CODE"
end tell
EOF
        ;;
    
    move)
        X=$1
        Y=$2
        osascript <<EOF
set moveX to $X
set moveY to $Y
tell application "System Events"
    set cursorPosition to {moveX, moveY}
    move mouse to cursorPosition
end tell
EOF
        ;;
    
    *)
        echo "Unknown command: $COMMAND"
        exit 1
        ;;
esac
