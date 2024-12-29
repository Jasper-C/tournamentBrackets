import sqlite3

def initialize_database(db_path="main_sports.db"):
    """
    Initializes the database with the required schema.
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create Teams table (if not already created)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Teams (
        team_id TEXT UNIQUE NOT NULL,
        location TEXT NOT NULL,
        nickname TEXT NOT NULL,
        abbreviation TEXT NOT NULL,
        year INTEGER NOT NULL,
        league TEXT NOT NULL,
        conference TEXT DEFAULT NULL,
        division TEXT DEFAULT NULL,
        place INTEGER DEFAULT NULL,
        head_coach TEXT DEFAULT NULL,
        home_stadium TEXT DEFAULT NULL,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        ties INTEGER DEFAULT 0,
        points_scored INTEGER DEFAULT 0,
        points_allowed INTEGER DEFAULT 0,
        primary_color TEXT DEFAULT NULL,
        secondary_color TEXT DEFAULT NULL,
        primary_text TEXT DEFAULT NULL,
        secondary_text TEXT DEFAULT NULL
    );
    """)

    # Create Ballparks table (if not already created)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ballparks (
        team_id TEXT NOT NULL,
        ballpark_name TEXT NOT NULL,
        location TEXT DEFAULT NULL,
        single_chance_left INTEGER DEFAULT 0,
        single_chance_right INTEGER DEFAULT 0,
        home_run_chance_left INTEGER DEFAULT 0,
        home_run_chance_right INTEGER DEFAULT 0,
        wall_height_left BOOLEAN DEFAULT TRUE,
        wall_height_right BOOLEAN DEFAULT TRUE
    );
    """)

    # Create Tournaments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tournaments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT DEFAULT '',
        type TEXT NOT NULL, -- Tournament type (e.g., "single_elimination")
        status TEXT NOT NULL, -- Current status (e.g., "created", "in_progress")
        league TEXT NOT NULL, 
        date_created TEXT NOT NULL, -- ISO timestamp
        last_updated TEXT NOT NULL, -- ISO timestamp
        tournament_data TEXT NOT NULL -- JSON details for the tournament
    );
    """)

    connection.commit()
    connection.close()
    print("Database schema initialized.")


if __name__ == "__main__":
    initialize_database()
