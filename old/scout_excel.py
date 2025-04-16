import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook, load_workbook
import os
import platform

def save_to_excel(formatted_data):
    # Split the data based on the '*' separator
    data_list = formatted_data.split('*')

    # Check if the file exists
    file_path = "scouting_data2.xlsx"
    if os.path.exists(file_path):
        try:
            # Open the existing workbook
            wb = load_workbook(file_path)
            ws = wb.active
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the file: {e}")
            return
    else:
        # Create a new workbook if it doesn't exist
        wb = Workbook()
        ws = wb.active
        ws.title = "Scouting Data"
        # Add a header row if the file is new
        headers = [
            "Match Number", "Team Number", "Preload", "Dropdown Value", "Field Position", "Leave Value", "Auto", 
            "Died Value", "Broke Value", "Defense Value", "Tele L4 Count", "Tele L3 Count", "Tele L2 Count", 
            "Tele Trough Count", "Tele Processor Count", "Tele Net Count", "Tele Take Off Count", "Tele Missed Count", 
            "Level", "Comments", "Coral Cycles", "Effective Cycles", "Scout Name"
        ]
        # Write headers in the first row
        for col_num, header in enumerate(headers, 1):
            ws.cell(row=1, column=col_num, value=header)

    # Find the next available row
    next_row = ws.max_row + 1

    # Write the data to the next available row
    for i, data in enumerate(data_list):
        ws.cell(row=next_row, column=i + 1, value=data.strip())

    # Save the workbook to the file
    try:
        wb.save(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

def open_excel():
    try:
        # Open the Excel file based on the operating system
        if platform.system() == "Windows":
            os.startfile("scouting_data2.xlsx")
        elif platform.system() == "Darwin":  # macOS
            os.system("open scouting_data2.xlsx")
        else:  # Linux
            os.system("xdg-open scouting_data2.xlsx")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening the file: {e}")

def on_submit():
    # Get the formatted data from the input field
    formatted_data = formatted_data_entry.get()
    if formatted_data:
        save_to_excel(formatted_data)
        formatted_data_entry.delete(0, tk.END)  # Clear the input box
    else:
        messagebox.showwarning("Input Error", "Please enter the formatted data.")

# Set up the UI
root = tk.Tk()
root.title("Scouting Data to Excel")

# Create a label for the input field
label = tk.Label(root, text="Enter Formatted Data:")
label.pack(padx=10, pady=10)

# Create an entry field to input the formatted data
formatted_data_entry = tk.Entry(root, width=100)
formatted_data_entry.pack(padx=10, pady=10)

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(padx=10, pady=10)

# Create a button to open the saved spreadsheet
open_button = tk.Button(root, text="Open Spreadsheet", command=open_excel)
open_button.pack(padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()
