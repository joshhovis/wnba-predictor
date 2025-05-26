from services.stats_api import get_team_season_stats
from services.injury_scraper import get_injuries, get_team_injuries
from utils.team_map import get_abbr_from_full_name
from predictor.logger import log_prediction

def predict_game(game, team_ids, db_connection):
    home = game["home"]
    away = game["away"]
    sportsbook = game["sportsbook"]
    line = game["line"]
    start_time = game["start_time"]

    # Get team IDs
    home_id = team_ids.get(home)
    away_id = team_ids.get(away)
    if not home_id or not away_id:
        print(f"❌ Missing team ID for {home} or {away}")
        return
    
    # Get stats
    home_stats = get_team_season_stats(home_id)
    away_stats = get_team_season_stats(away_id)

    home_ppg = home_stats.get("points", {}).get("for", {}).get("average", 0)
    away_ppg = away_stats.get("points", {}).get("for", {}).get("average", 0)
    home_opg = home_stats.get("points", {}).get("against", {}).get("average", 0)
    away_opg = away_stats.get("points", {}).get("against", {}).get("average", 0)

    # Raw predicted total
    predicted_total = (home_ppg + away_ppg + home_opg + away_opg) / 2

    # Account for injuries
    injuries = get_injuries()
    home_abbr = get_abbr_from_full_name(home)
    away_abbr = get_abbr_from_full_name(away)

    injured_home = get_team_injuries(home_abbr, injuries)
    injured_away = get_team_injuries(away_abbr, injuries)

    total_injured = len(injured_home) + len(injured_away)
    predicted_total -= total_injured * 5 # rough adjustment for now

    # Prediction decision
    prediction = "Over" if predicted_total > line else "Under"
    spread = abs(predicted_total - line)
    confidence = min(1.0, max(0.5, spread / 10))

    injury_notes = f"{len(injured_home)} OUT for {home}, {len(injured_away)} OUT for {away}"

    print(f"🏀 {home} vs {away} ({sportsbook}) → {prediction} ({predicted_total:.1f} vs line {line})")

    # Log prediction
    log_prediction(
        conn=db_connection,
        game_id=f"{home}_vs_{away}_{start_time}",
        date=start_time.split("T")[0],
        team_home=home,
        team_away=away,
        sportsbook=sportsbook,
        line=line,
        predicted_total=predicted_total,
        prediction=prediction,
        confidence=confidence,
        injury_notes=injury_notes
    )
