import pytest
import sqlite3
import json
from logic.tournament_manager import save_tournament, load_tournament, update_tournament

TOURNAMENT_DATA = {
    "teams": [
        {"id": "team_1", "name": "Team A"},
        {"id": "team_2", "name": "Team B"},
        {"id": "team_3", "name": "Team C"},
        {"id": "team_4", "name": "Team D"}
    ],
    "rounds": [
        {
            "round_number": 1,
            "matches": [
                {"match_id": 1, "team1": "team_1", "team2": "team_4", "winner": None},
                {"match_id": 2, "team1": "team_2", "team2": "team_3", "winner": None}
            ]
        }
    ]
}


def test_save_tournament(setup_test_db):
    """
    Test saving a tournament to the database.
    """
    db_path = setup_test_db
    save_tournament(
        name="Test Tournament",
        description="A test tournament",
        tournament_type="single_elimination",
        tournament_data=TOURNAMENT_DATA,
        db_path=db_path
    )

    # Verify data in the database
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name, description, type, status, tournament_data FROM Tournaments")
        result = cursor.fetchone()

    assert result is not None
    assert result[0] == "Test Tournament"  # name
    assert result[1] == "A test tournament"  # description
    assert result[2] == "single_elimination"  # type
    assert result[3] == "created"  # status
    assert json.loads(result[4]) == TOURNAMENT_DATA  # tournament_data


def test_load_tournament(setup_test_db):
    """
    Test loading a tournament from the database.
    """
    db_path = setup_test_db
    save_tournament(
        name="Test Tournament",
        description="A test tournament",
        tournament_type="single_elimination",
        tournament_data=TOURNAMENT_DATA,
        db_path=db_path
    )

    # Load the tournament
    tournament = load_tournament(1, db_path=db_path)
    assert tournament is not None
    assert tournament["name"] == "Test Tournament"
    assert tournament["description"] == "A test tournament"
    assert tournament["type"] == "single_elimination"
    assert tournament["status"] == "created"
    assert tournament["data"] == TOURNAMENT_DATA


def test_update_tournament(setup_test_db):
    """
    Test updating a tournament in the database.
    """
    db_path = setup_test_db
    save_tournament(
        name="Test Tournament",
        description="A test tournament",
        tournament_type="single_elimination",
        tournament_data=TOURNAMENT_DATA,
        db_path=db_path
    )

    # Update tournament status and data
    updated_data = TOURNAMENT_DATA.copy()
    updated_data["rounds"][0]["matches"][0]["winner"] = "team_1"  # Set a winner
    update_tournament(1, updated_data, "in_progress", db_path=db_path)

    # Verify the update
    tournament = load_tournament(1, db_path=db_path)
    assert tournament["status"] == "in_progress"
    assert tournament["data"]["rounds"][0]["matches"][0]["winner"] == "team_1"
