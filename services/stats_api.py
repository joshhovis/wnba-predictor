import requests
import sqlite3
import os
from utils.helpers import BASKETBALL_API_KEY

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'db.sqlite')
BASE_URL = "https://v1.basketball.api-sports.io"

HEADERS = {
    "x-rapidapi-host": "v1.basketball.api-sports.io",
    "x-rapidapi-key": BASKETBALL_API_KEY
}

def fetch_and_store_wnba_teams():
    print("Fetching WBNA teams...")
    url = f"{BASE_URL}/teams?league=13&season=2025"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    if "response" not in data:
        print("⚠️ API response missing 'response' key")
        return
    
    teams = data["response"]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for team in teams:
        if team["country"]["name"] != "USA":
            continue
        team_id = team["id"]
        name = team["name"]
        logo = team["logo"]
        country = team["country"]["name"]
        short_name = name.replace(" W", "").strip()

        cursor.execute("""
            INSERT OR IGNORE INTO teams (id, name, short_name, logo_url, country)
            VALUES (?, ?, ?, ?, ?)
        """, (team_id, name, short_name, logo, country))

    conn.commit()
    conn.close()
    print(f"✅ {len(teams)} teams fetched and cached.")

def get_team_season_stats(team_id):
    url = f"{BASE_URL}/teams/statistics?league=13&season=2025&team={team_id}"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        print(f"⚠️ Failed to get stats for team ID {team_id}")
        return None
    
    return res.json().get("response", {})
