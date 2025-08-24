UNDERSTAT_YEAR = 2025

team_order = [
    "team",
    "pts",
    "wins",
    "draws",
    "loses",
    "scored",
    "conceded",
    "xG",
    "xGA",
    "npxG",
    "npxGA",
    "npxGD",
    "xpts",
    "ppda",
    "ppda_allowed",
    "deep",
    "deep_allowed"
]

player_orders = {
    "goalkeepers": [
        "first_name", "second_name", "team_against", "Home_Away", "minutes",
        "xGC", "total_points", "xPoints", "clean_sheets", "goals_conceded", "saves",
        "bonus", "form", "penalties_saved", "yellow_cards", "red_cards"
    ],
    "defenders": [
        "first_name", "second_name", "team_against", "Home_Away", "minutes", "xGC", 
        "total_points", "xPoints", "goals_scored", "assists",
        "clean_sheets", "goals_conceded", "xG", "xA", "defensive_points", 
        "clearances_blocks_interceptions","recoveries", "tackles", "defensive_contribution",
        "bonus", "form", "yellow_cards", "red_cards"
    ],
    "midfielders": [
        "first_name", "second_name", "team_against", "Home_Away", "minutes",
        "xG", "xA", "xGC", "total_points", "xPoints", "goals_scored", "assists",
        "clean_sheets", "goals_conceded", "defensive_points", "clearances_blocks_interceptions",
        "recoveries", "tackles", "defensive_contribution",
        "bonus", "form", "yellow_cards", "red_cards"
    ],
    "attackers": [
        "first_name", "second_name", "team_against", "Home_Away", "minutes",
        "xG", "xA", "total_points", "xPoints", "goals_scored", "assists", "bonus", "form",
        "defensive_contribution", "defensive_points", "yellow_cards", "red_cards"
    ]
}