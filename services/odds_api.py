import requests
from datetime import datetime
from utils.helpers import ODDS_API_KEY

def get_todays_wnba_games(date_str=None):
    url = "https://api.the-odds-api.com/v4/sports/basketball_wnba/odds"
    params = {
        "regions": "us", # Search only U.S. sportsbook
        "markets": "totals", # Only searching over/under
        "bookmakers": "fanduel,draftkings",
        "oddsFormat": "decimal",
        "dateFormat": "iso",
        "apiKey": ODDS_API_KEY
    }

    print("Fetching today's WNBA games from Odds API...")
    res = requests.get(url, params=params)
    if res.status_code != 200:
        raise Exception(f"Odds API error: {res.status_code} - {res.text}")
    
    games = res.json()

    # Filter for only today's games
    if date_str is None:
        date_str = datetime.now().date().isoformat()
        
    today_games = []

    for game in games:
        game_time = game.get("commence_time", "")
        if not game_time.startswith(date_str):
            continue
            
        home = game.get("home_team", "Unknown")
        away = game.get("away_team", "Unknown")

        for bookmaker in game["bookmakers"]:
            if bookmaker["key"] not in ["fanduel", "draftkings"]:
                continue

            for market in bookmaker["markets"]:
                if market["key"] != "totals":
                    continue

                outcome = market["outcomes"][0] # First total line
                total_line = outcome.get("point")

                if total_line is None:
                    continue

                today_games.append({
                    "home": home,
                    "away": away,
                    "sportsbook": bookmaker["key"],
                    "line": total_line,
                    "start_time": game_time
                })

    print(f"✅ Found {len(today_games)} WNBA over/under lines for today.")
    return today_games
