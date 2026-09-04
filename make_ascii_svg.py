import sys
from pathlib import Path

# Configuration
CHAR_WIDTH = 5.2    # Approx width of monospace character in 7px font
CHAR_HEIGHT = 7.0
FONT_SIZE = "7px"
FILL_COLOR = "#8b949e"
BG_COLOR = "#0d1117"
DENSITY_RAMP = " .\\'`:-=+*cs#%@"

def map_pixel_to_char(pixel_value):
    # pixel_value is 0-255
    # ramp index: 0 is space (brightest), -1 is '@' (darkest)
    ramp = DENSITY_RAMP
    # pixel=0 (dark) -> index len(ramp)-1 (dense)
    # pixel=255 (bright) -> index 0 (sparse)
    idx = int((255 - pixel_value) / 255 * (len(ramp) - 1))
    # bound idx
    idx = max(0, min(len(ramp) - 1, idx))
    return ramp[idx]

def generate_ascii_art(img_path, cols=100, rows=53):
    from PIL import Image
    img = Image.open(img_path).convert("L")
    
    orig_w, orig_h = img.size
    aspect_ratio = orig_w / orig_h
    
    adjusted_rows = int(cols * (1 / aspect_ratio) * (CHAR_WIDTH / CHAR_HEIGHT))
    adjusted_rows = min(adjusted_rows, rows)
    if adjusted_rows <= 0:
        adjusted_rows = rows
        
    img = img.resize((cols, adjusted_rows), Image.Resampling.LANCZOS)
    
    pixels = img.getdata()
    ascii_str = ""
    for i, pixel in enumerate(pixels):
        ascii_str += map_pixel_to_char(pixel)
        if (i + 1) % cols == 0:
            ascii_str += "\n"
            
    return ascii_str.strip("\n").split("\n")

def get_placeholder_art():
    # Placeholder ASCII art spelling 'ROHIT'
    art = [
        "                                                                            ",
        "  RRRRRRRRRRR     OOOOOOOOO    HHH     HHH  IIIIIIIIII  TTTTTTTTTTTTTTTT    ",
        "  RRR      RRR  OOO       OOO  HHH     HHH     IIII     TTTTTTTTTTTTTTTT    ",
        "  RRR      RRR  OOO       OOO  HHH     HHH     IIII           TTTT          ",
        "  RRRRRRRRRRR   OOO       OOO  HHHHHHHHHHH     IIII           TTTT          ",
        "  RRR     RRR   OOO       OOO  HHHHHHHHHHH     IIII           TTTT          ",
        "  RRR      RRR  OOO       OOO  HHH     HHH     IIII           TTTT          ",
        "  RRR       RRR   OOOOOOOOO    HHH     HHH  IIIIIIIIII        TTTT          ",
        "                                                                            "
    ]
    return art

def generate_svg(ascii_lines, output_path):
    cols = max(len(line) for line in ascii_lines)
    rows = len(ascii_lines)
    
    # SVG dimensions
    width = 370
    char_w = width / cols
    char_h = char_w * (CHAR_HEIGHT / CHAR_WIDTH)
    
    height = int(rows * char_h + 20)
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <rect width="{width}" height="{height}" fill="{BG_COLOR}"/>
  <style>
    .text {{
      font-family: monospace;
      font-size: {FONT_SIZE};
      fill: {FILL_COLOR};
      white-space: pre;
    }}
    .cursor {{
      fill: {FILL_COLOR};
    }}
  </style>
'''
    
    total_anim_duration = 3.5
    wipe_duration = total_anim_duration * 0.4 
    stagger = (total_anim_duration - wipe_duration) / max(1, (rows - 1))
    
    for i, line in enumerate(ascii_lines):
        line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        y = (i + 1) * char_h + 10
        
        clip_id = f"clip_{i}"
        start_time = i * stagger
        
        svg += f'''
  <clipPath id="{clip_id}">
    <rect x="0" y="{y - char_h}" height="{char_h + 2}" width="0">
      <animate attributeName="width" from="0" to="{width}" begin="{start_time}s" dur="{wipe_duration}s" fill="freeze" />
    </rect>
  </clipPath>
  
  <g clip-path="url(#{clip_id})">
    <text x="10" y="{y}" class="text">{line}</text>
  </g>
  
  <rect x="10" y="{y - char_h + 1}" width="{char_w * 1.5}" height="{char_h - 2}" class="cursor" opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.99;1" begin="{start_time}s" dur="{wipe_duration}s" fill="freeze" />
    <animate attributeName="x" from="10" to="{width}" begin="{start_time}s" dur="{wipe_duration}s" fill="freeze" />
  </rect>
'''

    svg += '</svg>'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)

def main():
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent
    prepped_img_path = repo_root / "source-prepped.png"
    output_svg_path = repo_root / "rohit-ascii.svg"
    
    if prepped_img_path.exists():
        print(f"Found prepped image {prepped_img_path}. Operating in photo mode.")
        ascii_lines = generate_ascii_art(prepped_img_path)
    else:
        print(f"Prepped image not found. Operating in placeholder mode.")
        ascii_lines = get_placeholder_art()
        
    print(f"Generating SVG with {len(ascii_lines)} rows.")
    generate_svg(ascii_lines, output_svg_path)
    print(f"SVG successfully written to {output_svg_path}")

if __name__ == "__main__":
    main()
