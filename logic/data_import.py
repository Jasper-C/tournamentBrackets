import pandas as pd
import sqlite3


def validate_and_import(data, table_name, db_path="main_sports.db"):
    """
    Validates and imports a DataFrame into the specified SQLite table.
    :param data: DataFrame containing the data to import.
    :param table_name: Table to import the data into ("Teams" or "Ballparks").
    :param db_path: Path to the SQLite database file.
    """
    # Ensure the input is a DataFrame
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Data must be a pandas DataFrame.")

    # Define required columns for each table
    required_columns = {
        "Teams": [
            "team_id", "location", "nickname", "abbreviation", "year", "league",
            "conference", "division", "place", "head_coach", "home_stadium", "wins",
            "losses", "ties", "points_scored", "points_allowed", "primary_color",
            "secondary_color", "primary_text", "secondary_text"
        ],
        "Ballparks": [
            "team_id", "ballpark_name", "location", "single_chance_left",
            "single_chance_right", "home_run_chance_left", "home_run_chance_right",
            "wall_height_left", "wall_height_right"
        ]
    }

    if table_name not in required_columns:
        raise ValueError(f"Unknown table: {table_name}")

    # Check for missing columns
    missing_columns = [col for col in required_columns[table_name] if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Import data into the database
    connection = sqlite3.connect(db_path)
    try:
        data.to_sql(table_name, connection, if_exists="append", index=False)
    finally:
        connection.close()
