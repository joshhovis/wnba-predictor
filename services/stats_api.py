import requests
import sqlite3
import os
import time
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

def get_team_avg_score(team_id, num_games=8):
    print(f"📊 Fetching recent games for team {team_id}...")
    games_url = f"{BASE_URL}/games?team={team_id}&season=2024&league=13"
    res = requests.get(games_url, headers=HEADERS)

    if res.status_code != 200:
        print(f"⚠️ Failed to get recent games for team ID {team_id}")
        return 0, 0
    
    response = res.json().get("response", [])
    print(f"🔍 Found {len(response)} total games for team {team_id}")

    # Fallback that removes league filter if no games are found for a team - Had a bug where the new team (Golden State Valkyries) were not displaying game data when using a league filter
    if len(response) == 0:
        print(f"⚠️ No games returned for team {team_id} with league filter. Trying without league...")
        fallback_url = f"{BASE_URL}/games?team={team_id}&season=2025"
        res = requests.get(fallback_url, headers=HEADERS)
        response = res.json().get("response", [])

    for g in response[:5]:
        print(f"  - {g['date']} | Status: {g['status']['short']} | Home: {g['teams']['home']['name']} | Away: {g['teams']['away']['name']}")

    recent_games = [game for game in response if game.get("status", {}).get("short") in ["FT", "AOT"]][:num_games]

    if not recent_games:
        print(f"⚠️ No finished games found for team ID {team_id}")
        return 0, 0
    
    total_points = 0
    total_allowed = 0
    counted = 0

    for game in recent_games:
        game_id = game["id"]
        stats_url = f"{BASE_URL}/games/statistics/teams?id={game_id}"
        stats_res = requests.get(stats_url, headers=HEADERS)

        if stats_res.status_code != 200:
            print(f"⚠️ Failed to get stats for game {game_id}")
            continue

        stats = stats_res.json().get("response", [])
        if len(stats) != 2:
            continue

        team_stat = None
        opponent_stat = None

        for stat in stats:
            if stat["team"]["id"] == team_id:
                team_stat = stat
            else:
                opponent_stat = stat
        
        if not team_stat or not opponent_stat:
            continue

        # Estimate points: FGs + FTs (3's included in FG total)
        fg = team_stat["field_goals"]["total"]
        ft = team_stat["freethrows_goals"]["total"]
        team_points = fg * 2 + ft
        opp_fg = opponent_stat["field_goals"]["total"]
        opp_ft = opponent_stat["freethrows_goals"]["total"]
        opp_points = opp_fg * 2 + opp_ft

        total_points += team_points
        total_allowed += opp_points
        counted += 1

        time.sleep(0.5)
    
    if counted == 0:
        return 0, 0
    
    return round(total_points / counted, 1), round(total_allowed / counted, 1)

def get_h2h_avg_score(team1_id, team2_id, num_games=5, min_valid_games=3):
    fallback_seasons = ["2025", "2024", "2023"]
    valid_games = []

    for season in fallback_seasons:
        print(f"🔎 Checking H2H for season {season}")
        url = f"{BASE_URL}/games?h2h={team1_id}-{team2_id}&league=13&season={season}"
        res = requests.get(url, headers=HEADERS)

        if res.status_code != 200:
            print(f"⚠️ Failed to get H2H for {team1_id}-{team2_id} in {season}")
            continue

        response = res.json().get("response", [])
        for g in response:
            scores = g.get("scores", {})
            if scores.get("home", {}).get("total") is not None and scores.get("away", {}).get("total") is not None:
                valid_games.append(g)

        # ✅ Stop if we hit our minimum
        if len(valid_games) >= min_valid_games:
            break

    if len(valid_games) < min_valid_games:
        print(f"⚠️ Only found {len(valid_games)} valid H2H games for {team1_id} vs {team2_id}. Skipping.")
        return None

    valid_games = sorted(valid_games, key=lambda g: g["date"], reverse=True)[:num_games]

    total_score = 0
    for game in valid_games:
        s = game["scores"]
        total_score += s["home"]["total"] + s["away"]["total"]

    print(f"ℹ️ Using {len(valid_games)} H2H games for {team1_id} vs {team2_id}")
    return round(total_score / len(valid_games), 2)
