import time
import curses

# Function to read frames from the file
def read_frames_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().split('\n\n')  # Split frames based on the blank line separator

# Function to play animation using curses for smoother output
def play_animation(stdscr, frames, fps=30):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(33)   # Update every 33ms, adjust to match desired framerate
    
    frame_interval = 1 / fps  # Interval between frames in seconds
    last_time = time.time()  # Start time of the animation
    accumulated_time = 0  # Time accumulator for precise frame sync

    while True:
        for frame in frames:
            current_time = time.time()
            elapsed_time = current_time - last_time
            accumulated_time += elapsed_time  # Track how much time has passed in total
            
            # Skip frames if too much time has passed
            frames_to_skip = int(accumulated_time // frame_interval)
            accumulated_time -= frames_to_skip * frame_interval  # Keep the remaining time

            # Display the frame if enough time has passed
            if frames_to_skip > 0:
                stdscr.clear()  # Clear the screen
                stdscr.addstr(0, 0, frame)  # Add the emoji frame to the screen
                stdscr.refresh()  # Refresh the screen to show the frame
                print(f"Skipped {frames_to_skip} frames")  # Debugging line to see how many frames are skipped

            # Update the last time
            last_time = current_time

            # Sleep to maintain the desired frame rate and avoid excessive CPU usage
            time.sleep(frame_interval)

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
