import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

create_teams_table = '''
CREATE TABLE IF NOT EXISTS TEAMS (
    TeamID INT PRIMARY KEY,
    TeamNumber INT
)
'''

cursor.execute(create_teams_table)
connection.commit()

insert_team = '''
INSERT INTO TEAMS (TeamID, TeamNumber)
VALUES (?, ?)
'''

data = [1, 1730]
#cursor.execute(insert_team, data)
connection.commit()

select_query = 'SELECT * FROM TEAMS'
#cursor.execute(select_query)

results = cursor.fetchall()
for row in results:
    print(row)

update_team = '''
UPDATE TEAMS
SET TeamNumber = ?
WHERE TeamID = ?
'''

data = (254, 4)
#cursor.execute(update_team, data)
connection.commit()

delete_team = 'DELETE FROM TEAMS WHERE TeamID = ?'
#cursor.execute(delete_team, (1,))
connection.commit()

cursor.close()
connection.close()