import customtkinter
import sqlite3

class PitScoutingApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Pit Scouting Data Entry")
        self.geometry("700x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Database setup
        self.connection = sqlite3.connect('pit_scouting.db')
        self.cursor = self.connection.cursor()
        self.initialize_database()

        # UI Components
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter pit data (use * to separate fields):")
        self.entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.button = customtkinter.CTkButton(self, text="Save Data", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.status_label = customtkinter.CTkLabel(self, text="")
        self.status_label.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def initialize_database(self):
        try:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS PitScouting (
                ScoutingID INTEGER PRIMARY KEY,
                TeamName TEXT,
                TeamNumber TEXT,
                Weight TEXT,
                Dimensions TEXT,
                Cycles TEXT,
                Mechanisms TEXT,
                DrivetrainMotors TEXT,
                Hotswappable TEXT,
                ClimbTime TEXT,
                AutoStart TEXT,
                VisionTracking TEXT,
                ProgrammingLanguage TEXT,
                AutoInfo TEXT,
                BestAt TEXT,
                Comments TEXT,
                DrivetrainValue TEXT,
                SwerveValue TEXT,
                SDSValue TEXT,
                WCPValue TEXT,
                ThriftyBotValue TEXT,
                TroughValue TEXT,
                L2Value TEXT,
                L3Value TEXT,
                L4Value TEXT,
                NetValue TEXT,
                ProcessorValue TEXT,
                TakeOffAlgaeValue TEXT,
                GroundPickUpValue TEXT,
                StationPickUpValue TEXT,
                Level TEXT,
                AutoScoreAlgaeValue TEXT,
                AutoScoreCoralValue TEXT,
                LeaveValue TEXT,
                AutoTakeOffAlgae TEXT,
                ProcessorHPValue TEXT,
                StationHPValue TEXT,
                DefenseValue TEXT,
                DriveTeamSwitchValue TEXT,
                PictureValue TEXT
            )
            '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except Exception as e:
            print(f"Error initializing database: {str(e)}")

    def get_next_scouting_id(self):
        try:
            select_query = 'SELECT MAX(ScoutingID) FROM PitScouting'
            self.cursor.execute(select_query)
            result = self.cursor.fetchone()
            return 0 if result[0] is None else result[0] + 1
        except sqlite3.Error as e:
            self.status_label.configure(text=f"Database Error: {e}", fg_color="red")
            return None

    def button_callback(self):
        entry_text = self.entry.get().strip()
        if not entry_text:
            self.status_label.configure(text="Please enter data.", fg_color="red")
            return

        data_fields = entry_text.split('*')
        if len(data_fields) != 39:  # Expecting 40 fields
            self.status_label.configure(
                text=f"Incorrect number of fields ({len(data_fields)}). Expected 39 fields.", fg_color="red"
            )
            return

        scouting_id = self.get_next_scouting_id()
        if scouting_id is None:
            return

        data_fields.insert(0, scouting_id)  # Add ScoutingID

        insert_query = '''
INSERT INTO PitScouting (
    ScoutingID, TeamName, TeamNumber, Weight, Dimensions, Cycles, Mechanisms, 
    DrivetrainMotors, Hotswappable, ClimbTime, AutoStart, VisionTracking, 
    ProgrammingLanguage, AutoInfo, BestAt, Comments, DrivetrainValue, 
    SwerveValue, SDSValue, WCPValue, ThriftyBotValue, TroughValue, L2Value, 
    L3Value, L4Value, NetValue, ProcessorValue, TakeOffAlgaeValue, 
    GroundPickUpValue, StationPickUpValue, Level, AutoScoreAlgaeValue, 
    AutoScoreCoralValue, LeaveValue, AutoTakeOffAlgae, ProcessorHPValue, 
    StationHPValue, DefenseValue, DriveTeamSwitchValue, PictureValue
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
'''
        try:
            self.cursor.execute(insert_query, data_fields)
            self.connection.commit()
            self.status_label.configure(text="Data saved successfully!", fg_color="green")
            self.entry.delete(0, 'end')
        except sqlite3.Error as e:
            self.status_label.configure(text=f"Error saving data: {e}", fg_color="red")

    def on_closing(self):
        self.connection.close()
        self.destroy()


app = PitScoutingApp()
app.mainloop()
