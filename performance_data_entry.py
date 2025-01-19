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
    Leave,
    AutoTrough,
    AutoL2,
    AutoL3,
    AutoL4,
    AutoProcessor,
    AutoNet,
    AutoComments,
    TeleTrough,
    TeleL2,
    TeleL3,
    TeleL4,
    TeleProcessor,
    TeleNet,
    TeleComments,
    BargeLevel,
    BargeComments,
    ScoutName
)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
'''

while True:
    if id == None:
        id = 0
    else:
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
        performance[6],  # Leave
        performance[7],  # AutoTrough
        performance[8],  # AutoL2
        performance[9],  # AutoL3
        performance[10], # AutoL4
        performance[11], # AutoProcessor
        performance[12], # AutoNet
        performance[13], # AutoComments
        performance[14], # TeleTrough
        performance[15], # TeleL2
        performance[16], # TeleL3
        performance[17], # TeleL4
        performance[18], # TeleProcessor
        performance[19], # TeleNet
        performance[20], # TeleComments
        performance[21], # BargeLevel
        performance[22], # BargeComments
        performance[23], # ScoutName
    ])
    connection.commit()