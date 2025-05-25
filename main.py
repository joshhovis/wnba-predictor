from predictor.logger import init_db
from services.stats_api import fetch_and_store_wnba_teams

def main():
    print("Initializing database...")
    init_db()
    print("Fetching team data...")
    fetch_and_store_wnba_teams()
    print("Setup complete.")

if __name__ == "__main__":
    main()