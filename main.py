import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

select_query = 'SELECT * FROM MATCHES'
cursor.execute(select_query)

results = cursor.fetchall()
for row in results:
    print(row)

    

#update_team = '''
#UPDATE TEAMS
#SET TeamNumber = ?
#WHERE TeamID = ?
#'''

#data = (254, 4)
#cursor.execute(update_team, data)
#connection.commit()

#delete_team = 'DELETE FROM TEAMS WHERE TeamID = ?'
#cursor.execute(delete_team, (1,))
#connection.commit()

cursor.close()
connection.close()