# Tomas-Project
 Tomas Amaya
# Golf Leaderboard Dashboard

This Flask application scrapes ESPN's golf leaderboard and displays the top 5 players in a responsive web UI. 

## Features
- Scrapes live leaderboard data from ESPN
- Dynamic table rendering of all leaderboard columns
- Bar chart visualization of "To Par" metric using Chart.js
- Shows total score relative to par
-shows each individual round 



## Prerequisites
- Python 3.7 or later
- Internet connection to fetch ESPN data

## Installation
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd golf_stats_app
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Flask app:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Configuration
- No additional configuration or API keys required.



## Troubleshooting
- If you encounter parsing errors, ESPN may have updated their page structure. Inspect the HTML and update selectors accordingly.
