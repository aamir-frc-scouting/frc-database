import customtkinter
import sqlite3

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Data Entry")
        self.geometry("600x400")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Database setup
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.initialize_database()

        # UI Components
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter data (use * to separate fields):")
        self.entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.button = customtkinter.CTkButton(self, text="Save Data", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.status_label = customtkinter.CTkLabel(self, text="")
        self.status_label.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    def initialize_database(self):
        # Ensure the table exists
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS PERFORMANCE (
            PerformanceID INTEGER PRIMARY KEY,
            MatchNumber TEXT,
            TeamNumber TEXT,
            Preload TEXT,
            DriverStation TEXT,
            FieldPosition TEXT,
            Leave TEXT,
            AutoL4 TEXT,
            AutoL3 TEXT,
            AutoL2 TEXT,
            AutoTrough TEXT,
            AutoProcessor TEXT,
            AutoNet TEXT,
            AutoRemove TEXT,
            ReefPlacements TEXT,
            Died TEXT,
            Broke TEXT,
            Defense TEXT,
            TeleL4 TEXT,
            TeleL3 TEXT,
            TeleL2 TEXT,
            TeleTrough TEXT,
            TeleProcessor TEXT,
            TeleNet TEXT,
            TeleRemove TEXT,
            BargeLevel TEXT,
            Comments TEXT,
            ScoutName TEXT
        )
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def get_next_performance_id(self):
        select_query = 'SELECT MAX(PerformanceID) FROM PERFORMANCE'
        self.cursor.execute(select_query)
        result = self.cursor.fetchone()
        return 0 if result[0] is None else result[0] + 1

    def button_callback(self):
        entry_text = self.entry.get()
        if not entry_text:
            self.status_label.configure(text="Please enter data.", fg_color="red")
            return

        # Parse and insert data
        performance = entry_text.split('*')
        if len(performance) != 27:
            self.status_label.configure(
                text="Incorrect number of fields ("+str(len(performance))+"). Expected 27 fields.", fg_color="red"
            )
            return
        
        if not performance[1].isnumeric():
            self.status_label.configure(
                text="Incorrect type (String). Expected a team NUMBER.", fg_color="red"
            )
            return

        performance_id = self.get_next_performance_id()
        performance.insert(0, performance_id)  # Add PerformanceID to the data

        insert_performance_query = '''
        INSERT INTO PERFORMANCE (
            PerformanceID,
            MatchNumber,
            TeamNumber,
            Preload,
            DriverStation,
            FieldPosition,
            Leave,
            AutoL4,
            AutoL3,
            AutoL2,
            AutoTrough,
            AutoProcessor,
            AutoNet,
            AutoRemove,
            ReefPlacements,
            Died,
            Broke,
            Defense,
            TeleL4,
            TeleL3,
            TeleL2,
            TeleTrough,
            TeleProcessor,
            TeleNet,
            TeleRemove,
            BargeLevel,
            Comments,
            ScoutName
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''

        try:
            self.cursor.execute(insert_performance_query, performance)
            self.connection.commit()
            self.status_label.configure(text="Data saved successfully!", fg_color="green")
            self.entry.delete(0, 'end')  # Clear the entry field
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", fg_color="red")

app = App()
app.mainloop()
