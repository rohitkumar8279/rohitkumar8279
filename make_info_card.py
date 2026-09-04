import os
from pathlib import Path

def generate_svg():
    static_mode = os.environ.get('STATIC') == '1'
    
    width = 490
    height = 320
    bg_color = "#0d1117"
    border_color = "#30363d"
    text_color = "#c9d1d9"
    
    colors = {
        'cyan': '#58a6ff',
        'green': '#39d353',
        'magenta': '#bc8cff',
        'yellow': '#d29922',
        'red': '#f85149',
        'white': '#ffffff',
        'black': '#010409',
        'gray': '#8b949e',
        'blue': '#1f6feb'
    }

    style = ""
    if not static_mode:
        style = """
    <style>
        .line {
            opacity: 0;
            animation: fadeInSlide 0.5s ease-out forwards;
        }
        @keyframes fadeInSlide {
            0% {
                opacity: 0;
                transform: translateX(-10px);
            }
            100% {
                opacity: 1;
                transform: translateX(0);
            }
        }
        .delay-0 { animation-delay: 0ms; }
        .delay-1 { animation-delay: 150ms; }
        .delay-2 { animation-delay: 300ms; }
        .delay-3 { animation-delay: 450ms; }
        .delay-4 { animation-delay: 600ms; }
        .delay-5 { animation-delay: 750ms; }
        .delay-6 { animation-delay: 900ms; }
        .delay-7 { animation-delay: 1050ms; }
        .delay-8 { animation-delay: 1200ms; }
    </style>"""
    else:
        style = """
    <style>
        .line { opacity: 1; }
    </style>"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    {style}
    <rect width="{width}" height="{height}" fill="{bg_color}" rx="6" ry="6" stroke="{border_color}" stroke-width="1.5"/>
    <g font-family="Consolas, 'Courier New', monospace" font-size="14" fill="{text_color}" transform="translate(20, 20)">
"""
    
    lines_data = [
        # Title
        f'<text y="15" font-size="15" font-weight="bold"><tspan fill="{colors["green"]}">rohitkumar8279</tspan><tspan fill="{colors["white"]}">@github</tspan></text>',
        # Separator
        '<text y="35">─────────────────────</text>',
        # Rows
        f'<text y="60"><tspan fill="{colors["cyan"]}">Now      </tspan><tspan fill="{colors["white"]}">→ B.Tech Student · Full Stack Developer</tspan></text>',
        f'<text y="85"><tspan fill="{colors["green"]}">Stack    </tspan><tspan fill="{colors["white"]}">→ JavaScript, Python, React, Node.js</tspan></text>',
        f'<text y="110"><tspan fill="{colors["magenta"]}">AI/ML    </tspan><tspan fill="{colors["white"]}">→ TensorFlow, PyTorch, Deep Learning</tspan></text>',
        f'<text y="135"><tspan fill="{colors["yellow"]}">Projects </tspan><tspan fill="{colors["white"]}">→ Air Quality Intelligence, Interview Agent</tspan></text>',
        f'<text y="160"><tspan fill="{colors["red"]}">Research </tspan><tspan fill="{colors["white"]}">→ Medical AI, FMR Thesis (BTP)</tspan></text>',
        f'<text y="185"><tspan fill="{colors["cyan"]}">Interests</tspan><tspan fill="{colors["white"]}">→ AI Agents, System Design, Open Source</tspan></text>',
        # Color blocks
    ]

    palette = [
        colors['black'], colors['red'], colors['green'], colors['yellow'],
        colors['blue'], colors['magenta'], colors['cyan'], colors['white']
    ]
    
    color_blocks = '<g transform="translate(0, 230)">'
    for i, c in enumerate(palette):
        color_blocks += f'<rect x="{i*25}" y="0" width="15" height="15" fill="{c}"/>'
    color_blocks += '</g>'
    
    lines_data.append(color_blocks)

    for i, line_content in enumerate(lines_data):
        delay_class = f"delay-{i}"
        svg += f'        <g class="line {delay_class}">\n            {line_content}\n        </g>\n'

    svg += """    </g>\n</svg>"""

    script_dir = Path(__file__).resolve().parent
    out_path = script_dir.parent / "info-card.svg"
    
    with out_path.open("w", encoding="utf-8") as f:
        f.write(svg)
    
    print(f"Info card written to {out_path}")

if __name__ == "__main__":
    generate_svg()
