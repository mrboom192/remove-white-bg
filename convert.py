import os
from PIL import Image
import numpy as np
import cv2

def convert_to_color_with_transparency(input_path: str, output_path: str, color: tuple = (0, 0, 0)):
    """
    Converts an image such that all final pixels take on a specified color with adjusted transparency.

    Parameters:
        input_path (str): Path to the input image.
        output_path (str): Path where the output image will be saved.
        color (tuple): RGB color (R, G, B) to apply instead of black. Default is black (0, 0, 0).
    """
    try:
        # Open the image
        image = Image.open(input_path).convert("RGBA")  # Ensure RGBA mode for transparency

        # Convert to NumPy array
        image_np = np.array(image, dtype=np.float32)  # Use float for better calculations

        # Convert to grayscale for proper alpha adjustment
        gray = cv2.cvtColor(image_np.astype(np.uint8), cv2.COLOR_RGBA2GRAY)

        # Compute the alpha channel based on grayscale values
        alpha = 255 - gray  # Convert grayscale to alpha (white becomes transparent)

        # Apply the chosen color instead of black
        for c in range(3):  # Iterate over R, G, B channels
            image_np[:, :, c] = color[c]  # Set to specified color

        # Assign the computed alpha channel
        image_np[:, :, 3] = alpha

        # Convert back to uint8
        image_np = np.clip(image_np, 0, 255).astype(np.uint8)

        # Save the output image
        output_image = Image.fromarray(image_np)
        output_image.save(output_path)

        print(f"✅ Processed: {os.path.basename(input_path)} -> Saved at {output_path} with color {color}!")

    except Exception as e:
        print(f"❌ Error processing {input_path}: {e}")


def process_all_images(input_folder: str, output_folder: str, color: tuple = (0, 0, 0)):
    """
    Processes all images in the input folder and saves them in the output folder.

    Parameters:
        input_folder (str): Path to the folder containing input images.
        output_folder (str): Path to the folder where processed images will be saved.
        color (tuple): RGB color (R, G, B) to apply instead of black.
    """
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Process all image files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")):  # Check for valid image formats
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            convert_to_color_with_transparency(input_path, output_path, color)


# Example Usage: Process all images in 'input_images' and save to 'output_images'
input_dir = "input"
output_dir = "output"
process_all_images(input_dir, output_dir, color=(0, 0, 0))  # Change color as needed
