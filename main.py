import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

select_query = 'SELECT * FROM PERFORMANCE'
cursor.execute(select_query)

performance_headers = ["PerformanceID",
    "TeamNumber",
    "MatchNumber",
    "Preload",
    "DriverStation",
    "FieldPosition",
    "AutoNotesMissed",
    "Leave",
    "AutoAmpNotes",
    "AutoAmpNotesMissed",
    "AutoAmpPercentage",
    "AutoSpeakerNotes",
    "AutoSpeakerNotesMissed",
    "AutoSpeakerPercentage",
    "AutoComments",
    "TeleAmpNotes",
    "TeleAmpNotesMissed",
    "TeleAmpPercentage",
    "TeleSpeakerNotes",
    "TeleSpeakerNotesMissed",
    "TeleSpeakerPercentage",
    "Died",
    "Broke",
    "Defense",
    "TeleComments",
    "Cycles",
    "Passes",
    "StageLevel",
    "Harmony",
    "Trap",
    "StageComments",
    "ScoutName"]

results = cursor.fetchall()

for row in results:
    for i in range(len(performance_headers)):
        print(performance_headers[i]+": {"+str(row[i]), end='} ')
    print("\n\n")


    

update_team = '''
UPDATE PERFORMANCE
SET PerformanceID = ?
WHERE ScoutName = ?
'''

#data = (2, 'Isaac ')
#cursor.execute(update_team, data)
#connection.commit()

#delete_team = 'DELETE FROM TEAMS WHERE TeamID = ?'
#cursor.execute(delete_team, (1,))
#connection.commit()

cursor.close()
connection.close()