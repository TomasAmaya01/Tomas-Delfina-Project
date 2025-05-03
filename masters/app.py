from flask import Flask, render_template, abort
import requests
from bs4 import BeautifulSoup
import os

# Ensure working directory is project root for templates/static discovery
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(basedir, 'templates'),
    static_folder=os.path.join(basedir, 'static')
)

# ESPN Golf Leaderboard URL
ESPN_URL = "https://www.espn.com/golf/leaderboard"
# Browser-like headers to avoid blocking
REQUEST_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/113.0.0.0 Safari/537.36'
    )
}

def fetch_leaderboard(top_n=5):
    """
    Scrapes ESPN's golf tournament leaderboard and returns top N players and the first player's flag URL.
    """
    resp = requests.get(ESPN_URL, headers=REQUEST_HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', class_='Table')
    if not table or not table.tbody:
        raise RuntimeError("Could not parse leaderboard from ESPN page")

    # Extract headers
    header_cells = table.find('thead').find_all('th')
    header_names = [h.get_text(strip=True) for h in header_cells]
    keys = [name.lower().replace(' ', '_') for name in header_names]
    # Determine index of Player column
    try:
        player_idx = header_names.index('Player')
    except ValueError:
        player_idx = None

    # Extract rows
    rows = table.find('tbody').find_all('tr')
    leaderboard = []
    bg_flag = ''
    for i, row in enumerate(rows[:top_n]):
        cols = row.find_all('td')
        entry = {}
        # On first row, fetch flag image from Player cell
        if i == 0 and player_idx is not None and player_idx < len(cols):
            img_tag = cols[player_idx].find('img')
            if img_tag and img_tag.has_attr('src'):
                bg_flag = img_tag['src']
        # Build entry dict
        for idx, key in enumerate(keys):
            entry[key] = cols[idx].get_text(strip=True) if idx < len(cols) else ''
        leaderboard.append(entry)

    return keys, leaderboard, bg_flag

@app.route('/')
def index():
    """
    Renders the dashboard with leaderboard and flag background.
    """
    try:
        headers, players, bg_flag = fetch_leaderboard(5)
        name_key = next((h for h in headers if 'player' in h or 'name' in h), headers[1])
        par_key = next((h for h in headers if 'par' in h), None)
    except Exception as e:
        abort(500, description=f"Error fetching leaderboard: {e}")
    return render_template('index.html', headers=headers, players=players,
                           name_key=name_key, par_key=par_key, bg_flag=bg_flag)

if __name__ == '__main__':
    os.chdir(basedir)
    app.run(debug=True)
