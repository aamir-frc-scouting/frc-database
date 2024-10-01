import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

select_query = 'SELECT * FROM PERFORMANCE'
cursor.execute(select_query)

results = cursor.fetchall()
for row in results:
    print(row)

    

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