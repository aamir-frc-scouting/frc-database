import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

select_query = 'SELECT MAX(PerformanceID) FROM PERFORMANCE'
cursor.execute(select_query)
results = cursor.fetchall()
id = results[0][0]

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
while True:
    id+=1
    entry = input("Data Entry: ")
    performance = entry.split('*')
    performance.insert(0,id)
    cursor.execute(insert_performance, [
        performance[0],  # PerformanceID
        performance[1],  # TeamNumber
        performance[2],  # MatchNumber
        performance[3],  # Preload
        performance[4],  # DriverStation
        performance[5],  # FieldPosition
        performance[6],  # AutoNotesMissed
        performance[7],  # Leave
        performance[8],  # AutoAmpNotes
        performance[9],  # AutoAmpNotesMissed
        performance[10], # AutoAmpPercentage
        performance[11], # AutoSpeakerNotes
        performance[12], # AutoSpeakerNotesMissed
        performance[13], # AutoSpeakerPercentage
        performance[14], # AutoComments
        performance[15], # TeleAmpNotes
        performance[16], # TeleAmpNotesMissed
        performance[17], # TeleAmpPercentage
        performance[18], # TeleSpeakerNotes
        performance[19], # TeleSpeakerNotesMissed
        performance[20], # TeleSpeakerPercentage
        performance[21], # Died
        performance[22], # Broke
        performance[23], # Defense
        performance[24], # TeleComments
        performance[25], # Cycles
        performance[26], # Passes
        performance[27], # StageLevel
        performance[28], # Harmony
        performance[29], # Trap
        performance[30], # StageComments
        performance[31]  # ScoutName
    ])
    connection.commit()