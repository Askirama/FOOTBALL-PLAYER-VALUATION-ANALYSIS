# create_football_db.py
import pandas as pd
import sqlite3

def create_player_database():
    # Load the CSV
    df = pd.read_csv("/Users/abubakaraskirama/Documents/Football_analysis/fifa_players.csv")
    
    # Create database connection
    conn = sqlite3.connect('player_finance.db')
    
    # Load into SQLite
    df.to_sql('players', conn, index=False, if_exists='replace')
    
    # Verify
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
    print("✅ Tables created:", tables['name'].tolist())
    
    # Check row count
    count = pd.read_sql("SELECT COUNT(*) as player_count FROM players", conn)
    print(f"✅ Players loaded: {count['player_count'][0]}")
    
    return conn

# Create the database
conn = create_player_database()