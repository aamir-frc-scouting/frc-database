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
            "PerformanceID", "MatchNumber", "TeamNumber", "Preload", "DriverStation",
            "FieldPosition", "Leave", "AutoL4", "AutoL3", "AutoL2", "AutoTrough",
            "AutoProcessor", "AutoNet", "AutoRemove", "ReefPlacements", "Died", "Broke",
            "Defense", "TeleL4", "TeleL3", "TeleL2", "TeleTrough", "TeleProcessor",
            "TeleNet", "TeleRemove", "BargeLevel", "Comments", "ScoutName"
        ]

        self.active_filters = []

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

        self.btn_filter_data = customtkinter.CTkButton(self.frame_left, text="Filter Data", command=self.filter_data)
        self.btn_filter_data.pack(pady=5)

        self.btn_add_filter = customtkinter.CTkButton(self.frame_left, text="Add Filter", command=self.add_filter)
        self.btn_add_filter.pack(pady=5)

        self.btn_clear_filters = customtkinter.CTkButton(self.frame_left, text="Clear Filters", command=self.clear_filters)
        self.btn_clear_filters.pack(pady=5)

        self.btn_view_active_filters = customtkinter.CTkButton(self.frame_left, text="View Active Filters", command=self.view_active_filters)
        self.btn_view_active_filters.pack(pady=5)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        select_query = 'SELECT * FROM PERFORMANCE'
        cursor.execute(select_query)
        results = cursor.fetchall()
        self.table.delete(*self.table.get_children())
        for row in results:
            self.table.insert("", "end", values=row)
        cursor.close()
        connection.close()

    def filter_data(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Filter Data")
        popup.geometry("400x400")
        label = customtkinter.CTkLabel(popup, text="Select Columns to Display:")
        label.pack(pady=10)
        selected_columns = {}

        def select_all():
            for var in selected_columns.values():
                var.set(1)

        def apply_filter():
            visible_columns = [col for col, var in selected_columns.items() if var.get() == 1]
            self.table['displaycolumns'] = visible_columns if visible_columns else self.performance_headers
            popup.destroy()

        for col in self.performance_headers:
            var = customtkinter.IntVar()
            selected_columns[col] = var
            checkbox = customtkinter.CTkCheckBox(popup, text=col, variable=var)
            checkbox.pack(anchor="w", padx=10)

        btn_select_all = customtkinter.CTkButton(popup, text="Select All", command=select_all)
        btn_select_all.pack(pady=10)

        btn_apply = customtkinter.CTkButton(popup, text="Apply Filter", command=apply_filter)
        btn_apply.pack(pady=10)

        close_button = customtkinter.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def add_filter(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Add Filter")
        popup.geometry("400x200")
        label = customtkinter.CTkLabel(popup, text="Select Field and Enter Value:")
        label.pack(pady=10)
        field_var = customtkinter.StringVar()
        field_dropdown = customtkinter.CTkComboBox(popup, variable=field_var, values=self.performance_headers)
        field_dropdown.pack(pady=5)
        value_entry = customtkinter.CTkEntry(popup)
        value_entry.pack(pady=5)

        def apply_filter():
            field = field_var.get()
            value = value_entry.get()
            if field and value:
                self.active_filters.append((field, value))
                self.load_filtered_data()
            popup.destroy()

        btn_apply = customtkinter.CTkButton(popup, text="Apply Filter", command=apply_filter)
        btn_apply.pack(pady=10)

    def clear_filters(self):
        self.active_filters.clear()
        self.load_data()

    def view_active_filters(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Active Filters")
        popup.geometry("400x300")
        label = customtkinter.CTkLabel(popup, text="Current Active Filters:")
        label.pack(pady=10)
        for field, value in self.active_filters:
            filter_label = customtkinter.CTkLabel(popup, text=f"{field}: {value}")
            filter_label.pack(anchor="w")
        close_button = customtkinter.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def view_data(self):
        print("View Data Button Pressed")

    def update_data(self):
        print("Update Data Button Pressed")

    def delete_data(self):
        print("Delete Data Button Pressed")

app = App()
app.mainloop()
