#!/usr/bin/env python3
"""
Screen Guide Helper (Windows)
Captures screenshots and adds annotated pointers.

Usage:
  python screen-guide.py shot              - Capture full screen to screen-guide/latest.png
  python screen-guide.py point X Y LABEL   - Draw arrow at (X%, Y%) with LABEL and open in default viewer
"""

import sys
import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageGrab

# Try to import voice module (optional, for narration)
try:
    sys.path.insert(0, str(Path(__file__).parent))
    import voice
    HAS_VOICE = True
except ImportError:
    HAS_VOICE = False

SCREEN_GUIDE_DIR = Path(__file__).parent / "screen-guide"
LATEST_IMG = SCREEN_GUIDE_DIR / "latest.png"


def shot():
    """Capture full screen using PIL on Windows."""
    SCREEN_GUIDE_DIR.mkdir(exist_ok=True)
    try:
        # Capture full screen
        screenshot = ImageGrab.grab()
        screenshot.save(LATEST_IMG)
        print(f"[OK] Screenshot saved to {LATEST_IMG}")
        if HAS_VOICE:
            voice.speak("Screenshot taken, sir.")
    except Exception as e:
        print(f"✗ Screenshot failed: {e}", file=sys.stderr)
        sys.exit(1)


def point(x_pct, y_pct, label):
    """
    Draw a red-orange arrow pointing at (x%, y%) with label in a pill.
    x_pct, y_pct: percentages (0-100)
    label: short text label (2-4 words)
    """
    if not LATEST_IMG.exists():
        print(f"✗ No screenshot found. Run 'shot' first.", file=sys.stderr)
        sys.exit(1)
    
    img = Image.open(LATEST_IMG)
    width, height = img.size
    
    # Convert percentages to pixels
    x = int(width * x_pct / 100)
    y = int(height * y_pct / 100)
    
    draw = ImageDraw.Draw(img, "RGBA")
    
    # Arrow parameters
    arrow_color = (255, 140, 0)      # Red-orange
    outline_color = (255, 255, 255)  # White
    arrow_length = 80
    arrow_width = 8
    head_size = 20
    
    # Calculate arrow direction (pointing towards x, y from upper-left)
    angle = math.atan2(y - height * 0.1, x - width * 0.1)
    start_x = x - arrow_length * math.cos(angle)
    start_y = y - arrow_length * math.sin(angle)
    
    # Draw arrow line with white outline
    for offset in range(-2, 3):
        for offset2 in range(-2, 3):
            if offset * offset + offset2 * offset2 <= 4:
                draw.line(
                    [(start_x + offset, start_y + offset2), (x + offset, y + offset2)],
                    fill=outline_color,
                    width=arrow_width + 4
                )
    
    # Draw arrow line
    draw.line([(start_x, start_y), (x, y)], fill=arrow_color, width=arrow_width)
    
    # Draw arrowhead (triangle)
    angle_offset = 0.5
    left_x = x - head_size * math.cos(angle - angle_offset)
    left_y = y - head_size * math.sin(angle - angle_offset)
    right_x = x - head_size * math.cos(angle + angle_offset)
    right_y = y - head_size * math.sin(angle + angle_offset)
    
    # Arrowhead with outline
    for offset_range in range(-2, 3):
        for offset_range2 in range(-2, 3):
            if offset_range * offset_range + offset_range2 * offset_range2 <= 4:
                draw.polygon(
                    [(x + offset_range, y + offset_range2),
                     (left_x + offset_range, left_y + offset_range2),
                     (right_x + offset_range, right_y + offset_range2)],
                    fill=outline_color
                )
    
    draw.polygon(
        [(x, y), (left_x, left_y), (right_x, right_y)],
        fill=arrow_color
    )
    
    # Draw label in dark pill near tail
    pill_x = int(start_x)
    pill_y = int(start_y - 25)
    pill_width = len(label) * 8 + 20
    pill_height = 32
    
    # Draw rounded pill background (dark semi-transparent)
    draw.rectangle(
        [(pill_x - pill_width // 2, pill_y - pill_height // 2),
         (pill_x + pill_width // 2, pill_y + pill_height // 2)],
        fill=(0, 0, 0, 200),
        outline=(255, 255, 255, 255),
        width=2
    )
    
    # Draw text (basic - using default font)
    try:
        draw.text((pill_x, pill_y), label, fill=(255, 255, 255), anchor="mm")
    except TypeError:
        # Fallback for older PIL versions
        draw.text((pill_x - len(label) * 3, pill_y - 5), label, fill=(255, 255, 255))
    
    # Save and open
    img.save(LATEST_IMG)
    print(f"[OK] Arrow added: {label} at ({x_pct}%, {y_pct}%)")
    
    # Open in default viewer (Windows)
    try:
        os.startfile(str(LATEST_IMG))
        print(f"[OK] Opened in default viewer")
        
        # Speak butler line
        if HAS_VOICE:
            voice.speak("Right there, sir.")
    except Exception as e:
        print(f"✗ Failed to open image: {e}", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        print("Usage: python screen-guide.py [shot|point X Y LABEL]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "shot":
        shot()
    elif command == "point":
        if len(sys.argv) < 5:
            print("Usage: python screen-guide.py point X Y LABEL", file=sys.stderr)
            sys.exit(1)
        try:
            x = float(sys.argv[2])
            y = float(sys.argv[3])
            label = " ".join(sys.argv[4:])
            point(x, y, label)
        except ValueError:
            print("✗ X and Y must be numbers (0-100)", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"✗ Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
