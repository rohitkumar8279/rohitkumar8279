import json
from pathlib import Path
from datetime import datetime

def generate_svg(data):
    days = data.get('days', [])
    if not days:
        return "<svg></svg>"
    
    # Grid properties
    cell_size = 13
    cell_gap = 3
    week_width = cell_size + cell_gap
    
    # Palette definition for levels 0 to 5
    palette = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353', '#69f0a0']
    
    # Group by weeks (assuming GitHub HTML is already week-aligned)
    weeks = []
    current_week = []
    for day in days:
        current_week.append(day)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)
        
    width = 860
    height = 240
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    
    # Styles and Keyframe Animations
    svg.append('<style>')
    svg.append('''
        .bg { fill: #0d1117; rx: 8; ry: 8; }
        .text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; fill: #7d8590; }
        .footer-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; fill: #7d8590; }
        .cell { opacity: 0; animation: slideFadeIn 0.8s ease-out forwards; }
        @keyframes slideFadeIn {
            0% { opacity: 0; transform: translateY(5px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    ''')
    svg.append('</style>')
    
    # Background container
    svg.append(f'<rect class="bg" width="{width}" height="{height}" />')
    
    # Content group with margin
    margin_x = 40
    margin_y = 40
    svg.append(f'<g transform="translate({margin_x}, {margin_y})">')
    
    # Render day cells with staggered animation
    for w_idx, week in enumerate(weeks):
        for d_idx, day in enumerate(week):
            x = w_idx * week_width
            y = d_idx * week_width
            level = min(day.get('level', 0), len(palette) - 1)
            color = palette[level]
            # Diagonal delay for animation
            delay = (w_idx + d_idx) * 15 # in ms
            svg.append(f'<rect class="cell" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" ry="2" fill="{color}" style="animation-delay: {delay}ms;" />')
            
    # Render Month Labels
    month_labels = []
    prev_month = None
    for w_idx, week in enumerate(weeks):
        if not week: continue
        dt = datetime.strptime(week[0]['date'], '%Y-%m-%d')
        month = dt.strftime('%b')
        if month != prev_month:
            x = w_idx * week_width
            y = -10
            month_labels.append(f'<text class="text" x="{x}" y="{y}">{month}</text>')
            prev_month = month
            
    svg.extend(month_labels)
    
    # Render Day Labels
    svg.append('<text class="text" x="-30" y="22">Mon</text>')
    svg.append('<text class="text" x="-30" y="66">Wed</text>')
    svg.append('<text class="text" x="-30" y="110">Fri</text>')
    
    # Legend
    legend_x = 53 * week_width - 80
    legend_y = 7 * week_width + 15
    svg.append(f'<g transform="translate({legend_x}, {legend_y})">')
    svg.append('<text class="text" x="-35" y="11">Less</text>')
    for i, color in enumerate(palette):
        svg.append(f'<rect class="cell" x="{i * week_width}" y="0" width="{cell_size}" height="{cell_size}" rx="2" ry="2" fill="{color}" style="animation-delay: {(53 + 7) * 15}ms;" />')
    svg.append(f'<text class="text" x="{len(palette) * week_width + 5}" y="11">More</text>')
    svg.append('</g>')
    
    svg.append('</g>') # End of inner content group
    
    # Footer Stats
    stats_text = f"{data.get('total', 0)} contributions in the last year \u00B7 Current streak: {data.get('current_streak', 0)} days \u00B7 Longest: {data.get('longest_streak', 0)} days"
    svg.append(f'<text class="footer-text" x="{margin_x}" y="{height - 15}">{stats_text}</text>')
    
    svg.append('</svg>')
    return '\n'.join(svg)

def main():
    script_dir = Path(__file__).resolve().parent
    data_file = script_dir.parent / "data" / "contributions.json"
    out_file = script_dir.parent / "contrib-heatmap.svg"
    
    if not data_file.exists():
        print(f"Data file not found: {data_file}")
        return
        
    print(f"Reading data from {data_file}...")
    with data_file.open('r', encoding='utf-8') as f:
        data = json.load(f)
        
    svg_content = generate_svg(data)
    
    print(f"Writing SVG to {out_file}...")
    with out_file.open('w', encoding='utf-8') as f:
        f.write(svg_content)
        
    print("Done!")

if __name__ == "__main__":
    main()
