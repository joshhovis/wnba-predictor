import os
from dotenv import load_dotenv

load_dotenv()

# environment variables
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
BASKETBALL_API_KEY = os.getenv("BASKETBALL_API_KEY")
