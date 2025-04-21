import customtkinter
from tkinter import ttk
import sqlite3

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Performance Database Viewer")
        self.geometry("1000x600")

        # Create a left side menu
        self.create_side_menu()

        # Main content frame
        self.frame_table = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.frame_table.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        # Treeview columns
        self.performance_headers = [
    "PerformanceID", "MatchNumber", "TeamNumber", "Preload", "DriverStation",
    "FieldPosition", "Leave", "Auto", "Died", "Broke", "Defense",
    "TeleL4", "TeleL3", "TeleL2", "TeleTrough", "TeleProcessor",
    "TeleNet", "TeleTakeOff", "TeleMissed", "BargeLevel",
    "Comments", "CoralCycles", "EffectiveCycles", "ScoutName"
]

        self.columns_visibility = {col: True for col in self.performance_headers}  # Track column visibility
        self.active_filters = []  # Store active filters
        self.sort_orders = {col: True for col in self.performance_headers}  # Track sorting order

        # Treeview widget
        self.table = ttk.Treeview(
            master=self.frame_table,
            columns=self.performance_headers,
            show="headings",
            height=20
        )

        # Configure columns and headings
        for col in self.performance_headers:
            self.table.heading(col, text=col, anchor="w", command=lambda c=col: self.sort_column(c))
            self.table.column(col, anchor="w", width=150, stretch=False)  # Allow independent resizing

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbars
        scrollbar_x = ttk.Scrollbar(self.frame_table, orient="horizontal", command=self.table.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y = ttk.Scrollbar(self.frame_table, orient="vertical", command=self.table.yview)
        scrollbar_y.pack(side="right", fill="y")

        self.table.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

        # Load data from database
        self.load_data()

    def sort_column(self, col):
        self.sort_orders[col] = not self.sort_orders[col]  # Toggle sorting order
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        order = "ASC" if self.sort_orders[col] else "DESC"
        cursor.execute(f'SELECT * FROM PERFORMANCE ORDER BY {col} {order}')
        rows = cursor.fetchall()
        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", "end", values=row)
        connection.close()

    def update_table_columns(self):
        visible_columns = [col for col in self.performance_headers if self.columns_visibility[col]]
        self.table['displaycolumns'] = visible_columns if visible_columns else self.performance_headers

    def create_side_menu(self):
        # Side menu frame
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.pack(side="left", fill="y", padx=20, pady=20)

        # Side menu title
        self.menu_title = customtkinter.CTkLabel(self.frame_left, text="Menu", font=("Arial", 16))
        self.menu_title.pack(pady=10)

        # Columns button
        self.btn_columns = customtkinter.CTkButton(self.frame_left, text="Columns", command=self.columns_popup)
        self.btn_columns.pack(pady=5)

        # Filters button
        self.btn_filters = customtkinter.CTkButton(self.frame_left, text="Filters", command=self.filters_popup)
        self.btn_filters.pack(pady=5)

        # View Data button
        self.btn_view_data = customtkinter.CTkButton(self.frame_left, text="View Data", command=self.view_data_popup)
        self.btn_view_data.pack(pady=5)  # Add the button for viewing match data

    def load_data(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        select_query = 'SELECT * FROM PERFORMANCE'
        
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
        cursor.close()
        connection.close()

    def update_table_columns(self):
        visible_columns = [col for col in self.performance_headers if self.columns_visibility[col]]
        self.table['displaycolumns'] = visible_columns if visible_columns else self.performance_headers

    def display_results(self, title, results):
        results_popup = customtkinter.CTkToplevel(self)
        results_popup.title(title)
        results_popup.geometry("600x400")

        frame = customtkinter.CTkFrame(results_popup)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        table = ttk.Treeview(frame, columns=[str(i) for i in range(len(results[0]))], show="headings")
        
        for i in range(len(results[0])):
            table.heading(str(i), text=f"Column {i}", anchor="w")
            table.column(str(i), anchor="w", width=100, stretch=True)

        for row in results:
            table.insert("", "end", values=row)
        
        table.pack(fill="both", expand=True, padx=10, pady=10)
        
        close_button = customtkinter.CTkButton(results_popup, text="Close", command=results_popup.destroy)
        close_button.pack(pady=10)


    def show_max(self, popup):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        query = '''
        SELECT TeamNumber,
            MAX(TeleL4), MAX(TeleL3), MAX(TeleL2), MAX(TeleTrough), MAX(TeleProcessor), 
            MAX(TeleNet), MAX(TeleTakeOff), MAX(TeleMissed)
        FROM PERFORMANCE
        GROUP BY TeamNumber
        '''
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        popup.destroy()
        self.display_results("Max Per Team", results)
        
        connection.close()

    def show_averages(self, popup):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        query = '''
        SELECT TeamNumber,
            AVG(TeleL4), AVG(TeleL3), AVG(TeleL2), AVG(TeleTrough), AVG(TeleProcessor), 
            AVG(TeleNet), AVG(TeleTakeOff), AVG(TeleMissed)
        FROM PERFORMANCE
        GROUP BY TeamNumber
        '''
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        popup.destroy()
        self.display_results("Averages Per Team", results)
        
        connection.close()

    def show_all_matches(self, popup):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM PERFORMANCE")
        results = cursor.fetchall()
        
        popup.destroy()
        self.display_results("All Matches", results)
        
        connection.close()

    def view_data_popup(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("View Data")
        popup.geometry("400x300")

        label = customtkinter.CTkLabel(popup, text="Choose an option:", font=("Arial", 14))
        label.pack(pady=10)

        btn_all_matches = customtkinter.CTkButton(popup, text="Show All Matches", command=lambda: self.show_all_matches(popup))
        btn_all_matches.pack(pady=5)

        btn_avg_per_team = customtkinter.CTkButton(popup, text="Show Averages Per Team", command=lambda: self.show_averages(popup))
        btn_avg_per_team.pack(pady=5)

        btn_max_per_team = customtkinter.CTkButton(popup, text="Show Max Per Team", command=lambda: self.show_max(popup))
        btn_max_per_team.pack(pady=5)

        close_button = customtkinter.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def columns_popup(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Select Columns")
        popup.geometry("400x900")

        # Column selection
        label_columns = customtkinter.CTkLabel(popup, text="Select Columns to Display:")
        label_columns.pack(pady=10)

        # Create a dictionary to store the checkbox variables
        checkbox_vars = {}

        def toggle_column_visibility(col):
            self.columns_visibility[col] = not self.columns_visibility[col]
            self.update_table_columns()

        # Create checkboxes for each column
        for col in self.performance_headers:
            var = customtkinter.IntVar(value=1 if self.columns_visibility[col] else 0)
            checkbox_vars[col] = var
            checkbox = customtkinter.CTkCheckBox(popup, text=col, variable=var, command=lambda col=col: toggle_column_visibility(col))
            checkbox.pack(anchor="w", padx=10)

        # Buttons
        def select_all():
            # Set all checkbox values to 1 and update column visibility
            for col, var in checkbox_vars.items():
                var.set(1)
                self.columns_visibility[col] = True
            self.update_table_columns()

        def deselect_all():
            # Set all checkbox values to 0 and update column visibility
            for col, var in checkbox_vars.items():
                var.set(0)
                self.columns_visibility[col] = False
            self.update_table_columns()

        # Button to select all columns
        btn_select_all = customtkinter.CTkButton(popup, text="Select All", command=select_all)
        btn_select_all.pack(pady=10)

        # Button to deselect all columns
        btn_deselect_all = customtkinter.CTkButton(popup, text="Deselect All", command=deselect_all)
        btn_deselect_all.pack(pady=10)

        # Close button
        close_button = customtkinter.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def filters_popup(self):
        popup = customtkinter.CTkToplevel(self)
        popup.title("Manage Filters")
        popup.geometry("400x600")

        # Filter input section
        label_filter = customtkinter.CTkLabel(popup, text="Create Filter:")
        label_filter.pack(pady=10)

        field_var = customtkinter.StringVar()
        field_dropdown = customtkinter.CTkComboBox(popup, variable=field_var, values=self.performance_headers)
        field_dropdown.pack(pady=5)

        value_entry = customtkinter.CTkEntry(popup)
        value_entry.pack(pady=5)

        # Function to apply filter
        def apply_filter():
            field = field_var.get()
            value = value_entry.get()
            if field and value:
                self.active_filters.append((field, value))
                self.load_data()
            popup.destroy()

        # Button to apply filter
        btn_apply_filter = customtkinter.CTkButton(popup, text="Apply Filter", command=apply_filter)
        btn_apply_filter.pack(pady=10)

        # Active filters section
        label_active_filters = customtkinter.CTkLabel(popup, text="Active Filters:")
        label_active_filters.pack(pady=10)

        def delete_filter(field_to_delete):
            self.active_filters = [(field, value) for field, value in self.active_filters if field != field_to_delete]
            self.load_data()

        for field, value in self.active_filters:
            filter_frame = customtkinter.CTkFrame(popup)
            filter_frame.pack(pady=5)

            filter_label = customtkinter.CTkLabel(filter_frame, text=f"{field}: {value}")
            filter_label.pack(side="left", padx=10)

            # Button to delete filter
            btn_delete = customtkinter.CTkButton(filter_frame, text="Delete", command=lambda f=field: delete_filter(f))
            btn_delete.pack(side="right", padx=10)

        # Close button
        close_button = customtkinter.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

app = App()
app.mainloop()
