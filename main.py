from predictor.logger import init_db
from services.stats_api import fetch_and_store_wnba_teams
from services.odds_api import get_todays_wnba_games

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

    for game in games:
        print(game)

    print("Setup complete.")

if __name__ == "__main__":
    main()