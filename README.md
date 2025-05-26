# WNBA Over/Under Predictor Bot

This bot analyzes WNBA games and predicts whether the final score will go over or under the sportsbook's betting line using team stats, injury reports, and head-to-head trends.

## Features

- ✅ Pulls betting odds from the Odds API (DraftKings & FanDuel)
- ✅ Converts odds timing to local time for accurate date filtering
- ✅ Caches WNBA team IDs from API-Basketball
- ✅ Fetches team performance stats from API-Basketball
- ✅ Adjusts predictions based on real-time injury data (via Rotowire)
- ✅ Incorporates head-to-head historical performance across multiple seasons
- ✅ Logs all predictions to a local SQLite database
- 🔄 Streamlit dashboard for interacting with predictions (coming next)

## How It Works

1. Pulls scheduled games and over/under lines from DraftKings & FanDuel
2. Retrieves team scoring/defensive averages over recent games
3. Adjusts prediction based on injuries and H2H trends
4. Predicts whether the game will go over or under the total
5. Logs the recommendation and confidence to SQLite for review

## Status

### ✅ Step 1: Project Initialization
- Created project folder and structure
- Set up virtual environment, dependencies (`requests`, `python-dotenv`, `sqlite3`, etc.)
- Initialized Git repo and `.gitignore`
- Created base Python modules and `README.md`

### ✅ Step 2: Team ID Caching
- Pulled all WNBA teams from API-Basketball
- Cached team names and IDs into a local SQLite `teams` table
- Filtered out incorrect teams (e.g., Toyota Antelopes W)

### ✅ Step 3: Odds Retrieval
- Connected to the Odds API (DraftKings/FanDuel)
- Pulled over/under lines for upcoming games
- Implemented timezone-safe filtering to match games by local date

### ✅ Step 4: Injury Integration
- Scraped real-time injury data from Rotowire (JSON endpoint)
- Mapped team abbreviations to full names
- Adjusted predicted total based on number of players marked "OUT"

### ✅ Step 5: Stats Integration
- Pulled team stats (PPG/OPPG) from API-Basketball using recent games
- Filtered only finished games to ensure valid scoring data
- Incorporated offensive and defensive metrics per team

### ✅ Step 6: Prediction Engine + Logging
- Combined team stats + injuries to calculate predicted totals
- Compared predicted totals against sportsbook line
- Determined Over/Under pick and confidence level
- Logged predictions to SQLite (`predictions` table)

### ✅ Step 7: Head-to-Head (H2H) Trend Blending
- Integrated historical H2H performance across 2025–2023
- Validated minimum number of H2H games before use
- Blended H2H adjusted score with base predicted total if sufficient

### 🟡 Step 8: Streamlit Dashboard (Next)
- Display predictions interactively
- Allow user to mark results (hit/miss) to feed learning
- Graph trends, win rate, filters, and logs
