from predictor.logger import init_db
from predictor.engine import predict_game
from services.stats_api import fetch_and_store_wnba_teams
from services.odds_api import get_todays_wnba_games
import sqlite3

def main():
    print("Initializing database...")
    init_db()

    print("Fetching team data...")
    fetch_and_store_wnba_teams()

    # Prompt for date input
    user_date = input("📅 Enter a date (YYYY-MM-DD) or press Enter for today: ").strip()
    date_to_use = user_date if user_date else None

    print("Fetching WNBA odds for: {date_to_use or 'today'}")
    games = get_todays_wnba_games(date_to_use)

    # Load cached team IDs from DB
    conn = sqlite3.connect("data/db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT id, short_name FROM teams")
    team_ids = {
        short_name.strip(): team_id
        for team_id, short_name in cursor.fetchall()
    }

    # print("Loaded team IDs:", team_ids)
    for game in games:
        predict_game(game, team_ids, conn)

    print("Setup complete.")

if __name__ == "__main__":
    main()