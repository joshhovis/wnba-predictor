TEAM_ABBR_MAP = {
    "ATL": "Atlanta Dream",
    "CHI": "Chicago Sky",
    "CON": "Connecticut Sun",
    "DAL": "Dallas Wings",
    "GSV": "Golden State Valkyries",
    "IND": "Indiana Fever",
    "LA":  "Los Angeles Sparks",
    "LV":  "Las Vegas Aces",
    "MIN": "Minnesota Lynx",
    "NY":  "New York Liberty",
    "PHO": "Phoenix Mercury",
    "SEA": "Seattle Storm",
    "WAS": "Washington Mystics"
}

def get_abbr_from_full_name(full_name):
    for abbr, name in TEAM_ABBR_MAP.items():
        if full_name.lower() == name.lower():
            return abbr
    return None
