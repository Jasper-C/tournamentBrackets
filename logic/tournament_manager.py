import sqlite3
import json
from datetime import datetime


def save_tournament(name, description, tournament_type, tournament_data, league, db_path="main_sports.db"):
    """
    Saves a new tournament to the database.
    :param name: Name of the tournament.
    :param description: Brief description of the tournament.
    :param tournament_type: Type of the tournament (e.g., "single_elimination").
    :param tournament_data: Dictionary containing the tournament structure (stored as JSON).
    :param db_path: Path to the SQLite database.
    """
    tournament_json = json.dumps(tournament_data)  # Convert dictionary to JSON string
    timestamp = datetime.now().isoformat()

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO Tournaments (name, description, type, status, league, date_created, last_updated, tournament_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """, (name, description, tournament_type, "created", league, timestamp, timestamp, tournament_json))
        connection.commit()

def load_tournament(tournament_id, db_path="main_sports.db"):
    """
    Loads a tournament from the database by ID.
    :param tournament_id: ID of the tournament to load.
    :param db_path: Path to the SQLite database.
    :return: Dictionary containing the tournament structure and metadata, or None if not found.
    """
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT name, description, type, status, date_created, last_updated, tournament_data
        FROM Tournaments WHERE id = ?;
        """, (tournament_id,))
        result = cursor.fetchone()

    if result:
        name, description, tournament_type, status, date_created, last_updated, tournament_json = result
        return {
            "id": tournament_id,
            "name": name,
            "description": description,
            "type": tournament_type,
            "status": status,
            "date_created": date_created,
            "last_updated": last_updated,
            "data": json.loads(tournament_json)  # Convert JSON string back to dictionary
        }
    else:
        return None

def update_tournament(tournament_id, updated_data, status, db_path="main_sports.db"):
    """
    Updates an existing tournament in the database.
    :param tournament_id: ID of the tournament to update.
    :param updated_data: Updated tournament structure as a dictionary.
    :param status: New status of the tournament (e.g., "in_progress", "finished").
    :param db_path: Path to the SQLite database.
    """
    updated_json = json.dumps(updated_data)  # Convert dictionary to JSON string
    timestamp = datetime.now().isoformat()

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE Tournaments
        SET tournament_data = ?, status = ?, last_updated = ?
        WHERE id = ?;
        """, (updated_json, status, timestamp, tournament_id))
        connection.commit()
