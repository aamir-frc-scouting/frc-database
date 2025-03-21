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
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close

    def initialize_database(self):
        try:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS PERFORMANCE (
                PerformanceID INTEGER PRIMARY KEY,
                MatchNumber TEXT,
                TeamNumber TEXT,
                Preload TEXT,
                DriverStation TEXT,
                FieldPosition TEXT,
                Leave TEXT,
                Auto TEXT,
                Died TEXT,
                Broke TEXT,
                Defense TEXT,
                TeleL4 TEXT,
                TeleL3 TEXT,
                TeleL2 TEXT,
                TeleTrough TEXT,
                TeleProcessor TEXT,
                TeleNet TEXT,
                TeleTakeOff TEXT,
                TeleMissed TEXT,
                BargeLevel TEXT,
                Comments TEXT,
                CoralCycles TEXT,
                EffectiveCycles TEXT,
                ScoutName TEXT
            )
            '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
    
    def get_next_performance_id(self):
        try:
            select_query = 'SELECT MAX(PerformanceID) FROM PERFORMANCE'
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
        
        performance = entry_text.split('*')
        if len(performance) != 27:
            self.status_label.configure(
                text=f"Incorrect number of fields ({len(performance)}). Expected 27 fields.", fg_color="red"
            )
            return
        
        if not performance[1].isdigit():
            self.status_label.configure(
                text="Invalid input: Team number must be numeric.", fg_color="red"
            )
            return
        
        performance_id = self.get_next_performance_id()
        if performance_id is None:
            return  # Error message already set in get_next_performance_id()
        
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
        except sqlite3.Error as e:
            self.status_label.configure(text=f"Error saving data: {e}", fg_color="red")
    
    def on_closing(self):
        self.connection.close()
        self.destroy()

app = App()
app.mainloop()