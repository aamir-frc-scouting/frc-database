import customtkinter
from tkinter import ttk
import sqlite3

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Performance Database Viewer")
        self.geometry("1000x600")  # Increased window size to fit the side menu

        # Create a left side menu
        self.create_side_menu()

        # Main content frame
        self.frame_table = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.frame_table.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        # Treeview columns
        self.performance_headers = [
            "PerformanceID", "TeamNumber", "MatchNumber", "Preload", "DriverStation",
            "FieldPosition", "Leave", "AutoTrough", "AutoL2", "AutoL3", "AutoL4",
            "AutoProcessor", "AutoNet", "AutoComments", "TeleTrough", "TeleL2",
            "TeleL3", "TeleL4", "TeleProcessor", "TeleNet", "TeleComments",
            "BargeLevel", "BargeComments", "ScoutName"
        ]

        # Treeview widget
        self.table = ttk.Treeview(
            master=self.frame_table,
            columns=self.performance_headers,
            show="headings",
            height=20
        )

        # Configure columns and headings
        for col in self.performance_headers:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="w", minwidth=100, width=150)

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbars
        scrollbar_x = ttk.Scrollbar(self.frame_table, orient="horizontal", command=self.table.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y = ttk.Scrollbar(self.frame_table, orient="vertical", command=self.table.yview)
        scrollbar_y.pack(side="right", fill="y")

        self.table.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

        # Load data from database
        self.load_data()

    def create_side_menu(self):
        # Side menu frame
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.pack(side="left", fill="y", padx=20, pady=20)

        # Side menu items
        self.menu_title = customtkinter.CTkLabel(self.frame_left, text="Menu", font=("Arial", 16))
        self.menu_title.pack(pady=10)

        self.btn_view_data = customtkinter.CTkButton(self.frame_left, text="View Data", command=self.view_data)
        self.btn_view_data.pack(pady=5)

        self.btn_update_data = customtkinter.CTkButton(self.frame_left, text="Update Data", command=self.update_data)
        self.btn_update_data.pack(pady=5)

        self.btn_delete_data = customtkinter.CTkButton(self.frame_left, text="Delete Data", command=self.delete_data)
        self.btn_delete_data.pack(pady=5)

    def load_data(self):
        # Connect to SQLite database
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Fetch all rows from PERFORMANCE table
        select_query = 'SELECT * FROM PERFORMANCE'
        cursor.execute(select_query)
        results = cursor.fetchall()

        # Insert data into the Treeview
        for row in results:
            self.table.insert("", "end", values=row)

        cursor.close()
        connection.close()

    def view_data(self):
        print("View Data Button Pressed")
        popup = customtkinter.CTkToplevel(self)
        popup.title("Popup Window")
        popup.geometry("300x200")

        # Add a label to the popup
        label = customtkinter.CTkLabel(popup, text="This is a popup!")
        label.pack(pady=20)

        # Add a close button to the popup
        close_button = customtkinter.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)
        # Logic to view data, refresh or open a new window, etc.

    def update_data(self):
        print("Update Data Button Pressed")
        # Logic to update data

    def delete_data(self):
        print("Delete Data Button Pressed")
        # Logic to delete data


app = App()
app.mainloop()