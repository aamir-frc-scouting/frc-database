import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

create_teams_table = '''
CREATE TABLE IF NOT EXISTS TEAMS (
    TeamNumber INT PRIMARY KEY
)
'''

create_matches_table = '''
CREATE TABLE IF NOT EXISTS MATCHES (
    MatchNumber INT PRIMARY KEY,
    MatchType TEXT CHECK(MatchType IN ('practice', 'qualification', 'elimination')),
    Red1 INT,
    Red2 INT,
    Red3 INT,
    Blue1 INT,
    Blue2 INT,
    Blue3 INT,
    FOREIGN KEY (Red1) REFERENCES TEAMS(TeamNumber),
    FOREIGN KEY (Red2) REFERENCES TEAMS(TeamNumber),
    FOREIGN KEY (Red3) REFERENCES TEAMS(TeamNumber),
    FOREIGN KEY (Blue1) REFERENCES TEAMS(TeamNumber),
    FOREIGN KEY (Blue2) REFERENCES TEAMS(TeamNumber),
    FOREIGN KEY (Blue3) REFERENCES TEAMS(TeamNumber)
)
'''

create_performance_table = '''
CREATE TABLE IF NOT EXISTS PERFORMANCE (
    PerformanceID INT PRIMARY KEY,
    TeamNumber INT,
    MatchNumber	INT,
    Preload BOOLEAN,
    DriverStation TEXT CHECK(DriverStation IN ('Red1', 'Red2', 'Red3', 'Blue1', 'Blue2', 'Blue3')),
    FieldPosition INT,
    AutoNotesMissed INT,
    Leave BOOLEAN,
    AutoAmpNotes INT,
    AutoAmpNotesMissed INT,
    AutoAmpPercentage FLOAT,
    AutoSpeakerNotes INT,
    AutoSpeakerNotesMissed INT,
    AutoSpeakerPercentage FLOAT,
    AutoComments TEXT,
    TeleAmpNotes INT,
    TeleAmpNotesMissed INT,
    TeleAmpPercentage FLOAT,
    TeleSpeakerNotes INT,
    TeleSpeakerNotesMissed INT,
    TeleSpeakerPercentage FLOAT,
    Died BOOLEAN,
    Broke BOOLEAN,
    Defense BOOLEAN,
    TeleComments TEXT,
    Cycles INT,
    Passes INT,
    StageLevel TEXT CHECK(StageLevel IN ('No Park', 'Parked', 'Onstage', 'Spotlit')),
    Harmony BOOLEAN,
    Trap BOOLEAN,
    StageComments TEXT,
    ScoutName TEXT,
    FOREIGN KEY (TeamNumber) REFERENCES TEAMS(TeamNumber),
    FOREIGN KEY (MatchNumber) REFERENCES MATCHES(MatchNumber)
)
'''

create_attributes_table='''
CREATE TABLE IF NOT EXISTS ATTRIBUTES (
    AttributeID INT PRIMARY KEY,
    ScoutName TEXT,
    TeamNumber INT,
    TeamName TEXT,
    Dimensions TEXT,
    Weight FLOAT,
    DriveTrain TEXT,
    CodingLanguage TEXT,
    VisionTracking TEXT,
    Autonomous TEXT,
    IntakeFrom TEXT,
    IntakeType TEXT,
    AmpScoring TEXT,
    SpeakerScoring TEXT,
    TrapScoring	TEXT,
    ShootingMechanism TEXT,
    ShootingLocation TEXT,
    Climb TEXT,
    Harmonize TEXT,
    ClimbTime TEXT,
    ClimbPosition TEXT,
    DriveTeam TEXT,
    BestAt TEXT,
    Picture	TEXT,
    Bumper TEXT,
    GraciousProfessionalism	TEXT,
    Comments TEXT,
    FOREIGN KEY (TeamNumber) REFERENCES TEAMS(TeamNumber)
)
'''

cursor.execute(create_teams_table)
cursor.execute(create_matches_table)
cursor.execute(create_performance_table)
cursor.execute(create_attributes_table)
connection.commit()

insert_team = '''
INSERT INTO TEAMS(TeamNumber)
VALUES (?)
'''

team_numbers = []  # SCRUBBED: Real team numbers removed for privacy



#for team_number in team_numbers:
#    cursor.execute(insert_team, [team_number])
#connection.commit()

insert_match = '''
INSERT INTO MATCHES (MatchNumber, MatchType, Red1, Red2, Red3, Blue1, Blue2, Blue3)
VALUES (?,?,?,?,?,?,?,?)
'''

insert_performance = '''
INSERT INTO PERFORMANCE (
    PerformanceID,
    TeamNumber,
    MatchNumber,
    Preload,
    DriverStation,
    FieldPosition,
    AutoNotesMissed,
    Leave,
    AutoAmpNotes,
    AutoAmpNotesMissed,
    AutoAmpPercentage,
    AutoSpeakerNotes,
    AutoSpeakerNotesMissed,
    AutoSpeakerPercentage,
    AutoComments,
    TeleAmpNotes,
    TeleAmpNotesMissed,
    TeleAmpPercentage,
    TeleSpeakerNotes,
    TeleSpeakerNotesMissed,
    TeleSpeakerPercentage,
    Died,
    Broke,
    Defense,
    TeleComments,
    Cycles,
    Passes,
    StageLevel,
    Harmony,
    Trap,
    StageComments,
    ScoutName
)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
'''

matches = []  # SCRUBBED: Real match data removed for privacy

#for match in matches:
#    cursor.execute(insert_match, [match[0],match[1],match[2],match[3],match[4],match[5],match[6],match[7]])
#connection.commit()

cursor.close()
connection.close()