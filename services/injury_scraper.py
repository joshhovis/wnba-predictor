import requests

def get_injuries():
    url = "https://www.rotowire.com/wnba/tables/injury-report.php?team=ALL&pos=ALL"
    res = requests.get(url)
    if res.status_code != 200:
        print("⚠️ Failed to fetch injury report")
        return []
    
    try:
        injuries = res.json()
    except Exception as e:
        print("⚠️ Error decoding Rotowire JSON:", e)
        return []
    
    return injuries

def get_team_injuries(team_name, injuries):
    return [
        injury for injury in injuries
        if injury.get("team") in team_name and injury.get("status") == "OUT"
    ]