import pytz
import requests
from datetime import datetime
from dateutil import parser
from utils.helpers import ODDS_API_KEY

def get_todays_wnba_games(date_str=None):
    url = "https://api.the-odds-api.com/v4/sports/basketball_wnba/odds"
    params = {
        "regions": "us", # Search only U.S. sportsbook
        "markets": "totals", # Only searching over/under
        "bookmakers": "draftkings",
        "oddsFormat": "decimal",
        "dateFormat": "iso",
        "apiKey": ODDS_API_KEY
    }

    print("Fetching today's WNBA games from Odds API...")
    res = requests.get(url, params=params)
    if res.status_code != 200:
        raise Exception(f"Odds API error: {res.status_code} - {res.text}")
    
    games = res.json()

    eastern = pytz.timezone("US/Eastern")
    target_date = date_str or datetime.now(eastern).date().isoformat()

    today_games = []

    for game in games:
        utc_time = parser.isoparse(game.get("commence_time", ""))
        local_time = utc_time.astimezone(eastern).date().isoformat()

        if local_time != target_date:
            continue
            
        home = game.get("home_team", "Unknown")
        away = game.get("away_team", "Unknown")

        for bookmaker in game["bookmakers"]:
            if bookmaker["key"] not in ["draftkings"]:
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
                    "start_time": game["commence_time"]
                })

    print(f"✅ Found {len(today_games)} WNBA over/under lines for today.")
    return today_games
