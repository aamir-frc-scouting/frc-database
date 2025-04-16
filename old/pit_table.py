import customtkinter
from tkinter import ttk
import sqlite3

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pit Scouting Database Viewer")
        self.geometry("1000x600")

        # Create a left side menu
        self.create_side_menu()

        # Main content frame
        self.frame_table = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.frame_table.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        # Treeview columns for pit scouting
        self.pit_headers = [
    "ScoutingID", "TeamName", "TeamNumber", "Weight", "Dimensions", "Cycles", "Mechanisms", 
    "DrivetrainMotors", "Hotswappable", "ClimbTime", "AutoStart", "VisionTracking", 
    "ProgrammingLanguage", "AutoInfo", "BestAt", "Comments", "DrivetrainValue", 
    "SwerveValue", "SDSValue", "WCPValue", "ThriftyBotValue", "TroughValue", 
    "L2Value", "L3Value", "L4Value", "NetValue", "ProcessorValue", "TakeOffAlgaeValue", 
    "GroundPickUpValue", "StationPickUpValue", "Level", "AutoScoreAlgaeValue", 
    "AutoScoreCoralValue", "LeaveValue", "AutoTakeOffAlgae", "ProcessorHPValue", 
    "StationHPValue", "DefenseValue", "DriveTeamSwitchValue", "PictureValue"
]

        self.columns_visibility = {col: True for col in self.pit_headers}
        self.active_filters = []

        # Treeview widget
        self.table = ttk.Treeview(
            master=self.frame_table,
            columns=self.pit_headers,
            show="headings",
            height=20
        )

        # Configure columns and headings
        for col in self.pit_headers:
            self.table.heading(col, text=col, anchor="w")
            self.table.column(col, anchor="w", width=150, stretch=False)

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbars
        scrollbar_x = ttk.Scrollbar(self.frame_table, orient="horizontal", command=self.table.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y = ttk.Scrollbar(self.frame_table, orient="vertical", command=self.table.yview)
        scrollbar_y.pack(side="right", fill="y")

        self.table.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

        # Load data from database
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect('pit_scouting.db')
        cursor = connection.cursor()
        select_query = 'SELECT * FROM PitScouting'

        # Apply filters to query if any are active
        if self.active_filters:
            filter_clauses = []
            filter_values = []
            for field, value in self.active_filters:
                filter_clauses.append(f"{field} LIKE ?")
                filter_values.append(f"%{value}%")
            select_query += " WHERE " + " AND ".join(filter_clauses)
            cursor.execute(select_query, filter_values)
        else:
            cursor.execute(select_query)

        results = cursor.fetchall()
        self.table.delete(*self.table.get_children())
        for row in results:
            self.table.insert("", "end", values=row)
        connection.close()

    def create_side_menu(self):
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.pack(side="left", fill="y", padx=20, pady=20)

        self.menu_title = customtkinter.CTkLabel(self.frame_left, text="Menu", font=("Arial", 16))
        self.menu_title.pack(pady=10)

        self.btn_columns = customtkinter.CTkButton(self.frame_left, text="Columns", command=self.columns_popup)
        self.btn_columns.pack(pady=5)

        self.btn_filters = customtkinter.CTkButton(self.frame_left, text="Filters", command=self.filters_popup)
        self.btn_filters.pack(pady=5)

    def columns_popup(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Select Columns")
        popup.geometry("400x500")

        label = customtkinter.CTkLabel(popup, text="Select Columns to Display:")
        label.pack(pady=10)

        checkbox_vars = {}

        def toggle_column_visibility(col):
            self.columns_visibility[col] = not self.columns_visibility[col]
            self.update_table_columns()

        for col in self.pit_headers:
            var = customtkinter.IntVar(value=1 if self.columns_visibility[col] else 0)
            checkbox_vars[col] = var
            checkbox = customtkinter.CTkCheckBox(popup, text=col, variable=var, command=lambda c=col: toggle_column_visibility(c))
            checkbox.pack(anchor="w", padx=10)

        close_button = customtkinter.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def update_table_columns(self):
        visible_columns = [col for col in self.pit_headers if self.columns_visibility[col]]
        self.table['displaycolumns'] = visible_columns

    def filters_popup(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Manage Filters")
        popup.geometry("400x400")

        label = customtkinter.CTkLabel(popup, text="Create Filter:")
        label.pack(pady=10)

        field_var = customtkinter.StringVar()
        field_dropdown = customtkinter.CTkComboBox(popup, variable=field_var, values=self.pit_headers)
        field_dropdown.pack(pady=5)

        value_entry = customtkinter.CTkEntry(popup)
        value_entry.pack(pady=5)

        def apply_filter():
            field = field_var.get()
            value = value_entry.get()
            if field and value:
                self.active_filters.append((field, value))
                self.load_data()
            popup.destroy()

        apply_button = customtkinter.CTkButton(popup, text="Apply Filter", command=apply_filter)
        apply_button.pack(pady=10)

        close_button = customtkinter.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

app = App()
app.mainloop()
