import os
from PIL import Image

# Convert pixel brightness to moon phase emoji (more detailed phases)
def pixel_to_moon(pixel):
    brightness = sum(pixel) / 3
    if brightness > 240:
        return '🌕'  # Full Moon
    elif brightness > 215:
        return '🌝'  # Gibbous
    elif brightness > 190:
        return '🌖'  # Waxing Crescent 2
    elif brightness > 170:
        return '🌔'  # Waxing Crescent
    elif brightness > 150:
        return '🌓'  # First Quarter
    elif brightness > 130:
        return '🌗'  # Waning Crescent 2
    elif brightness > 110:
        return '🌘'  # Waning Crescent
    else:
        return '🌑'  # New Moon

# Generate emoji frames and save to file
def generate_frames(frame_paths, output_file, width=80, height=40):
    frames = []
    for frame_path in frame_paths:
        if os.path.exists(frame_path):
            try:
                img = Image.open(frame_path).convert('L').resize((width, height))
                emojis = [pixel_to_moon((px, px, px)) for px in img.getdata()]
                frame = '\n'.join(''.join(emojis[i:i+width]) for i in range(0, len(emojis), width))
                frames.append(frame)
            except Exception as e:
                print(f"Error processing {frame_path}: {e}")
        else:
            print(f"Frame not found: {frame_path}")
    
    # Save the frames to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(frames))
    
    print(f"Frames successfully saved to {output_file}")

# Main function to call generate_frames
def main():
    output_file = 'frames/emoji_frames.txt'
    frame_paths = [f'frames/frame_{i:04d}.png' for i in range(1, 9500)]  # Adjust frame count based on video
    generate_frames(frame_paths, output_file)

if __name__ == "__main__":
    main()
