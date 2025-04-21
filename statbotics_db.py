import sqlite3
import statbotics

# Create or connect to a SQLite database
conn = sqlite3.connect('team_stats.db')
cursor = conn.cursor()

# Create a table to store the team stats for each year (Adjust columns based on the data you need)
cursor.execute('''
CREATE TABLE IF NOT EXISTS team_stats (
    team_number INTEGER,
    year INTEGER,
    team_name TEXT,
    country TEXT,
    state TEXT,
    district TEXT,
    rookie_year INTEGER,
    wins INTEGER,
    losses INTEGER,
    total_points REAL,
    auto_points REAL,
    teleop_points REAL,
    endgame_points REAL,
    auto_rp REAL,
    coral_rp REAL,
    barge_rp REAL,
    total_coral_points REAL,
    total_algae_points REAL,
    rank INTEGER,
    percentile REAL,
    district_points INTEGER,
    district_rank INTEGER,
    PRIMARY KEY (team_number, year)
);
''')

# Instantiate the Statbotics object
sb = statbotics.main.Statbotics()

# Team numbers list
team_numbers = [
    1323, 2910, 1778, 422, 868, 5468, 5406, 4272, 2974, 125, 6328, 3538, 4499, 4909,
    148, 2832, 3937, 7426, 3044, 5535, 2228, 449, 2468, 1072, 5026, 3847, 6147, 343,
    624, 7617, 1807, 188, 2412, 294, 5472, 10523, 360, 1388, 9072, 5142, 3655, 1730,
    6940, 108, 6459, 10014, 2429, 5843, 7563, 1710, 8590, 7565, 930, 948, 1502, 1825,
    10428, 6431, 7444, 4905, 6996, 6665, 1880, 3008, 10077, 9787, 7531, 6738, 9085,
    7415, 5124, 2635, 5553, 7538, 4091
]

# Define the year for which you want to fetch data
year = 2025  # Example year

# Loop through the team numbers and fetch the data using statbotics API
for team_number in team_numbers:
    # Fetch the team data for the specific year using the Statbotics API
    team_data = sb.get_team_year(team_number, year, fields=['all'])  # Add specific fields as necessary

    # Extract the relevant information from the returned data
    team_name = team_data.get('name', 'N/A')
    country = team_data.get('country', 'N/A')
    state = team_data.get('state', 'N/A')
    district = team_data.get('district', 'N/A')
    rookie_year = team_data.get('rookie_year', 0)
    wins = team_data.get('record', {}).get('wins', 0)
    losses = team_data.get('record', {}).get('losses', 0)
    total_points = team_data.get('epa', {}).get('breakdown', {}).get('total_points', 0.0)
    auto_points = team_data.get('epa', {}).get('breakdown', {}).get('auto_points', 0.0)
    teleop_points = team_data.get('epa', {}).get('breakdown', {}).get('teleop_points', 0.0)
    endgame_points = team_data.get('epa', {}).get('breakdown', {}).get('endgame_points', 0.0)
    auto_rp = team_data.get('epa', {}).get('breakdown', {}).get('auto_rp', 0.0)
    coral_rp = team_data.get('epa', {}).get('breakdown', {}).get('coral_rp', 0.0)
    barge_rp = team_data.get('epa', {}).get('breakdown', {}).get('barge_rp', 0.0)
    total_coral_points = team_data.get('epa', {}).get('breakdown', {}).get('total_coral_points', 0.0)
    total_algae_points = team_data.get('epa', {}).get('breakdown', {}).get('total_algae_points', 0.0)
    rank = team_data.get('ranks', {}).get('total', {}).get('rank', 0)
    percentile = team_data.get('ranks', {}).get('total', {}).get('percentile', 0.0)
    district_points = team_data.get('district_points', 0)
    district_rank = team_data.get('district_rank', 0)

    # Ensure that all values are correctly passed and added
    values = (
        team_number, year, team_name, country, state, district, rookie_year, wins, losses,
        total_points, auto_points, teleop_points, endgame_points, auto_rp, coral_rp, barge_rp,
        total_coral_points, total_algae_points, rank, percentile, district_points, district_rank
    )
    
    # Insert the team data into the database
    cursor.execute('''
    INSERT OR REPLACE INTO team_stats (
        team_number, year, team_name, country, state, district, rookie_year, wins, losses,
        total_points, auto_points, teleop_points, endgame_points, auto_rp, coral_rp, barge_rp,
        total_coral_points, total_algae_points, rank, percentile, district_points, district_rank
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', values)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully inserted into the database.")
