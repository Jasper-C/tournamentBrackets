import pytest
import pandas as pd
import sqlite3
import json
from logic.data_import import validate_and_import

# Sample data for Teams and Ballparks
TEAMS_DATA = {
    "team_id": ["2023_mlb_nyy"],
    "location": ["New York"],
    "nickname": ["Yankees"],
    "abbreviation": ["NYY"],
    "year": [2023],
    "league": ["MLB"],
    "conference": [None],
    "division": [None],
    "place": [1],
    "head_coach": ["Aaron Boone"],
    "home_stadium": ["Yankee Stadium"],
    "wins": [99],
    "losses": [63],
    "ties": [0],
    "points_scored": [807],
    "points_allowed": [643],
    "primary_color": ["#1C2841"],
    "secondary_color": ["#A5ACAF"],
    "primary_text": ["#FFFFFF"],
    "secondary_text": ["#000000"],
}

BALLPARKS_DATA = {
    "team_id": ["2023_mlb_nyy"],
    "ballpark_name": ["Yankee Stadium"],
    "location": ["New York"],
    "single_chance_left": [5],
    "single_chance_right": [4],
    "home_run_chance_left": [15],
    "home_run_chance_right": [14],
    "wall_height_left": [True],
    "wall_height_right": [False],
}


def test_successful_import_teams(setup_test_db):
    """
    Test successful import of Teams data.
    """
    db_path = setup_test_db
    df = pd.DataFrame(TEAMS_DATA)
    validate_and_import(df, "Teams", db_path=db_path)

    # Verify data in the database
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Teams")
        rows = cursor.fetchall()

    assert len(rows) == 1
    assert rows[0][0] == "2023_mlb_nyy"  # team_id


def test_successful_import_ballparks(setup_test_db):
    """
    Test successful import of Ballparks data.
    """
    db_path = setup_test_db
    df = pd.DataFrame(BALLPARKS_DATA)
    validate_and_import(df, "Ballparks", db_path=db_path)

    # Verify data in the database
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Ballparks")
        rows = cursor.fetchall()

    assert len(rows) == 1
    assert rows[0][1] == "Yankee Stadium"  # ballpark_name


def test_missing_columns(setup_test_db):
    """
    Test that missing required columns raises an error.
    """
    db_path = setup_test_db
    df = pd.DataFrame({"team_id": ["2023_mlb_nyy"], "nickname": ["Yankees"]})  # Missing required columns
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_and_import(df, "Teams", db_path=db_path)
