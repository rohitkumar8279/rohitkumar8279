import json
import re
import sys
import urllib.request
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def fetch_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching contributions: {e}")
        return None
    return html

def parse_contributions(html):
    soup = BeautifulSoup(html, "html.parser")
    days = []
    
    # Try finding td with data-date
    td_cells = soup.find_all('td', attrs={'data-date': True})
    
    # Also find tooltips for counts
    tooltips = {tt.get('for'): tt.text.strip() for tt in soup.find_all('tool-tip')}
    
    for td in td_cells:
        date_str = td.get('data-date')
        level_str = td.get('data-level', '0')
        level = int(level_str)
        
        count = 0
        
        # Determine the count from tooltip or text
        tooltip_id = td.get('id')
        text = tooltips.get(tooltip_id, "")
        if not text:
            text = td.text
        
        if "No contributions" in text:
            count = 0
        else:
            match = re.search(r'^(\d+)\s+contribution', text)
            if match:
                count = int(match.group(1))
                
        days.append({
            'date': date_str,
            'count': count,
            'level': level
        })
        
    days.sort(key=lambda x: x['date'])
    return days

def calculate_stats(days):
    total = 0
    current_streak = 0
    longest_streak = 0
    best_day = {'date': None, 'count': 0}
    monthly_totals = defaultdict(int)
    
    streak = 0
    for day in days:
        count = day['count']
        date = day['date']
        total += count
        
        dt = datetime.strptime(date, '%Y-%m-%d')
        month_name = dt.strftime('%B')
        monthly_totals[month_name] += count
        
        if count > 0:
            streak += 1
            if streak > longest_streak:
                longest_streak = streak
        else:
            streak = 0
            
        if count > best_day['count']:
            best_day = {'date': date, 'count': count}
            
    # Streak at the end of the year
    current_streak = streak
    
    return {
        'days': days,
        'total': total,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'best_day': best_day,
        'monthly_totals': dict(monthly_totals)
    }

def main():
    username = "rohitkumar8279"
    print(f"Fetching contributions for {username}...")
    html = fetch_contributions(username)
    if not html:
        sys.exit(1)
        
    days = parse_contributions(html)
    if not days:
        print("No contribution data found. Empty calendar or parsing failed.")
        sys.exit(1)
        
    stats = calculate_stats(days)
    
    # Resolve paths relative to this script
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    out_file = data_dir / "contributions.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
        
    print(f"Total Contributions: {stats['total']}")
    print(f"Current Streak: {stats['current_streak']}")
    print(f"Longest Streak: {stats['longest_streak']}")
    if stats['best_day']['date']:
        print(f"Best Day: {stats['best_day']['date']} ({stats['best_day']['count']} contributions)")
    print(f"Saved data to {out_file}")

if __name__ == "__main__":
    main()
