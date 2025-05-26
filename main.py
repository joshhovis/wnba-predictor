from predictor.logger import init_db
from services.stats_api import fetch_and_store_wnba_teams
from services.odds_api import get_todays_wnba_games

def main():
    print("Initializing database...")
    init_db()

    print("Fetching team data...")
    fetch_and_store_wnba_teams()

    print("Fetching today's game odds...")
    games = get_todays_wnba_games()

    for game in games:
        print(game)

    print("Setup complete.")

if __name__ == "__main__":
    main()