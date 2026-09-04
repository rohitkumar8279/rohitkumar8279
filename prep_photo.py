import argparse
import sys
from pathlib import Path
from rembg import remove
import cv2
import numpy as np
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description="Preprocess photo for ASCII art generator.")
    
    # repo root is parent of scripts directory
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent
    default_input = repo_root / "source-photo.jpg"
    default_output = repo_root / "source-prepped.png"
    
    parser.add_argument("input_path", nargs="?", default=str(default_input), help="Path to input photo")
    args = parser.parse_args()
    
    input_path = Path(args.input_path).resolve()
    output_path = default_output
    
    print(f"Input path: {input_path}")
    if not input_path.exists():
        print(f"Error: Input file {input_path} does not exist.")
        sys.exit(1)
        
    print("Loading image and removing background...")
    try:
        input_image = Image.open(input_path)
        # Remove background (returns an RGBA image)
        nobg_image = remove(input_image)
    except Exception as e:
        print(f"Error removing background: {e}")
        sys.exit(1)
        
    print("Converting to grayscale and applying OpenCV CLAHE...")
    # Convert RGBA to numpy array
    img_np = np.array(nobg_image)
    
    # Extract alpha channel and color channels
    if img_np.shape[2] == 4:
        alpha = img_np[:, :, 3]
        rgb = img_np[:, :, :3]
    else:
        alpha = np.ones((img_np.shape[0], img_np.shape[1]), dtype=np.uint8) * 255
        rgb = img_np
        
    # Convert to grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    
    # Apply CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray_clahe = clahe.apply(gray)
    
    print("Compositing onto pure white background...")
    # Create white background
    white_bg = np.ones_like(gray_clahe) * 255
    
    # Normalize alpha to 0-1
    alpha_norm = alpha.astype(float) / 255.0
    
    # Composite: output = alpha * foreground + (1-alpha) * background
    composite = (gray_clahe * alpha_norm + white_bg * (1 - alpha_norm)).astype(np.uint8)
    
    # Save output
    try:
        out_img = Image.fromarray(composite)
        out_img.save(output_path)
        print(f"Successfully saved prepped image to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
