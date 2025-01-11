# Tutorial: Running the "Bad Apple" Animation in Emojis on Your Terminal

Result: https://www.youtube.com/watch?v=glo_xlNPFyY

This tutorial will guide you through the steps to set up and run the "Bad Apple" animation in emojis on your terminal. It includes preprocessing the frames to improve performance and ensures smooth playback.

---

## Prerequisites

### 1. Python and Required Libraries
Make sure you have Python installed. You'll also need the following Python libraries:
- `Pillow` for image processing
- `curses` for terminal animation (already included in Python for Linux/macOS; install `windows-curses` if you're on Windows)

Install the libraries:
```bash
pip install pillow
pip install windows-curses  # Only for Windows users
```

### 2. Video Frames
You need the individual video frames for the animation as PNG files. Extract the frames from the "[Bad Apple](https://www.youtube.com/watch?v=FtutLA63Cp8)" video using a tool like `ffmpeg`:

```bash
ffmpeg -i bad_apple.mp4 -vf "scale=60:30" frames/frame_%04d.png
```
This command extracts the frames, scales them to 60x30 pixels (adjust as needed), and saves them in a folder named `frames/`.

---

## Step 1: Preprocess Frames into an Emoji File

Preprocessing the frames into a single file ensures smoother playback by avoiding real-time frame conversion.

Create a script named `generate_frames.py`:

```python
import os
from PIL import Image

# Convert pixel brightness to moon phase emoji (more detailed phases)
def pixel_to_moon(pixel):
    brightness = sum(pixel) / 3
    if brightness > 240:
        return '🌕'
    elif brightness > 200:
        return '🌖'
    elif brightness > 160:
        return '🌔'
    elif brightness > 120:
        return '🌓'
    elif brightness > 80:
        return '🌒'
    elif brightness > 40:
        return '🌘'
    else:
        return '🌑'

# Convert image to emoji frame
def image_to_emoji(frame_path):
    img = Image.open(frame_path).convert('L').resize((60, 30))  # Adjust resolution here
    emojis = [pixel_to_moon((px, px, px)) for px in img.getdata()]
    return '\n'.join(''.join(emojis[i:i+60]) for i in range(0, len(emojis), 60))

# Process all frames and save to a single file
def preprocess_frames(input_folder, output_file):
    frame_paths = sorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.png')])
    with open(output_file, 'w', encoding='utf-8') as f:
        for frame_path in frame_paths:
            print(f"Processing {frame_path}")
            f.write(image_to_emoji(frame_path) + '\n\n')

if __name__ == "__main__":
    preprocess_frames('frames', 'frames/emoji_frames.txt')
```

Run the script:
```bash
python generate_frames.py
```
This will create a file named `frames/emoji_frames.txt` containing all the preprocessed frames.

---

## Step 2: Play the Animation

Create a script named `main.py`:

```python
import time
import curses

# Function to read frames from the file
def read_frames_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().split('\n\n')  # Split frames based on the blank line separator

# Function to play animation using curses for smoother output
def play_animation(stdscr, frames, fps=30):
    curses.curs_set(0)  # Hide cursor
    frame_interval = 1 / fps  # Interval between frames in seconds
    last_time = time.time()  # Start time of the animation

    while True:
        for frame in frames:
            current_time = time.time()
            elapsed_time = current_time - last_time

            if elapsed_time >= frame_interval:
                stdscr.clear()  # Clear the screen
                stdscr.addstr(0, 0, frame)  # Add the emoji frame to the screen
                stdscr.refresh()  # Refresh the screen to show the frame

                last_time = current_time  # Update the last time for the next frame
            else:
                time.sleep(frame_interval - elapsed_time)  # Sleep to maintain FPS

# Main function to load and start the animation
def main():
    frames_file = 'frames/emoji_frames.txt'
    frames = read_frames_from_file(frames_file)
    print(f"Found {len(frames)} frames.")
    if not frames:
        print("No frames found or loaded. Exiting program.")
        return

    curses.wrapper(lambda stdscr: play_animation(stdscr, frames))

if __name__ == "__main__":
    main()
```

Run the script:
```bash
python main.py
```

---

## Adjustments and Tips

1. **Change Resolution**:
   Adjust the resolution in `generate_frames.py` by modifying the `resize((60, 30))` line. Higher resolution creates more detailed animations but requires a larger terminal window.

2. **Adjust FPS**:
   Modify the `fps` parameter in `main.py` to match the original video (e.g., 30 FPS).

3. **Ensure Terminal Size**:
   Make sure your terminal window is large enough to display the animation (e.g., 60 columns wide and 30 rows tall for the default resolution).

4. **Debugging**:
   If the animation lags or skips, try reducing the resolution or FPS.

---

Enjoy your "Bad Apple" animation in emojis!

