from services.stats_api import get_team_avg_score
from services.stats_api import get_h2h_avg_score
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
    home_ppg, home_opg = get_team_avg_score(home_id)
    away_ppg, away_opg = get_team_avg_score(away_id)

    if home_ppg == 0 and away_ppg == 0:
        print(f"⚠️ No scoring data found for {home} or {away}")
        return

    # Raw predicted total
    predicted_total = (home_ppg + away_ppg + home_opg + away_opg) / 2

    # Factor in h2h history between teams
    h2h_total = get_h2h_avg_score(home_id, away_id)
    if h2h_total is not None:
        predicted_total = (predicted_total + h2h_total) / 2
        print(f"  → H2H adjusted total: {predicted_total}")
    else:
        print(f"  → H2H skipped due to insufficient historical data")


    # Account for injuries
    injuries = get_injuries()
    home_abbr = get_abbr_from_full_name(home)
    away_abbr = get_abbr_from_full_name(away)

    injured_home = get_team_injuries(home_abbr, injuries)
    injured_away = get_team_injuries(away_abbr, injuries)

    total_injured = len(injured_home) + len(injured_away)
    predicted_total -= total_injured * 5 # rough adjustment for now

    print(f"  → home_ppg: {home_ppg}, away_ppg: {away_ppg}, home_opg: {home_opg}, away_opg: {away_opg}")
    print(f"  → Pre-injury predicted total: {(home_ppg + away_ppg + home_opg + away_opg) / 2}")
    print(f"  → Total OUT players: {total_injured}")

    # Prediction decision
    prediction = "Over" if predicted_total > line else "Under"
    predicted_total = round(predicted_total, 2)
    spread = round(abs(predicted_total - line), 2)
    confidence = round(min(1.0, max(0.5, spread / 10)), 2)

    injury_notes = f"{len(injured_home)} OUT for {home}, {len(injured_away)} OUT for {away}"

    print(f"🏀 {home} vs {away} ({sportsbook}) → {prediction} (Predicted: {predicted_total:.1f} | Line: {line} | Spread: {spread:.1f})")

    # Log prediction
    log_prediction(
        conn=db_connection,
        game_id=f"{home}_vs_{away}_{start_time}_{sportsbook}",
        date=start_time.split("T")[0],
        team_home=home,
        team_away=away,
        sportsbook=sportsbook,
        line=line,
        predicted_total=predicted_total,
        spread=spread,
        prediction=prediction,
        confidence=confidence,
        injury_notes=injury_notes
    )
