# mamba create -n timelapse pillow moviepy numpy tqdm
import os
import sys
import logging
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip
from datetime import timedelta
import numpy as np
from tqdm import tqdm  # You'll need to install the tqdm library

def create_timelapse(input_dir, output_file, fps, spf, font_file=None, text_color="white", text_position=(10, 10)):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Check if the input directory exists
    if not os.path.isdir(input_dir):
        logging.error(f"Input directory '{input_dir}' does not exist.")
        return

    # Collect all image file paths
    image_files = sorted([os.path.join(input_dir, img) for img in os.listdir(input_dir) if img.endswith(('png', 'jpg', 'jpeg', 'JPG'))])

    if not image_files:
        logging.warning("No images found in the directory.")
        return

    # Load the images and add timecode
    images = []
    for idx, img_path in enumerate(tqdm(image_files, desc="Processing images")):
        try:
            img = Image.open(img_path)
        except Exception as e:
            logging.error(f"Error opening image '{img_path}': {e}")
            continue

        draw = ImageDraw.Draw(img)

        # Calculate the timecode for the current frame
        total_seconds = idx * spf
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        timecode = f"{int(days):02d}d {int(hours):02d}m {int(minutes):02d}s"

        # Choose a font and size
        font_size = 150  # Adjust this value to make the text bigger or put to 0 to not have a timecode

        try:
            if font_file:
                font = ImageFont.truetype(font_file, font_size)
            else:
                # Use a default system font with the desired size
                font = ImageFont.load_default().font_variant(size=font_size)
        except Exception as e:
            logging.error(f"Error loading font file '{font_file}': {e}")
            continue

        # Add timecode to the image
        draw.text(text_position, timecode, font=font, fill=text_color)

        # Convert the image to a numpy array and append to the list
        images.append(np.array(img))

    # Create a timelapse video
    logging.info("Creating timelapse video...")
    video_clip = ImageSequenceClip(images, fps=fps)
    video_clip.write_videofile(output_file, codec="libx264")
    logging.info(f"Timelapse video saved to '{output_file}'")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python timelapse.py <input_directory> <output_file> <fps> <spf> [font_file] [text_color] [text_position_x] [text_position_y]")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_file = sys.argv[2]
    fps = int(sys.argv[3])
    spf = int(sys.argv[4])
    font_file = sys.argv[5] if len(sys.argv) > 5 else None
    text_color = sys.argv[6] if len(sys.argv) > 6 else "white"
    text_position_x = int(sys.argv[7]) if len(sys.argv) > 7 else 10
    text_position_y = int(sys.argv[8]) if len(sys.argv) > 8 else 10

    create_timelapse(input_directory, output_file, fps, spf, font_file, text_color, (text_position_x, text_position_y))