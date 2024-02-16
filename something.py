
#-------------Final Availability Module--------------------
from datetime import date as dt_date
import sqlite3
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk

# Function Definitions
def check_availability():
    selected_date = date_picker.get()
    hall_name = hall_combobox.get()
    
    query = "SELECT COUNT(*) FROM booking WHERE program_date = ? AND hall_name = ?"
    cursor.execute(query, (selected_date, hall_name))
    result = cursor.fetchone()

    if result and result[0] > 0:
        availability_status.config(text="Not available", foreground="red")
    else:
        availability_status.config(text="Available", foreground="green")

def clear_table():
    # Clear existing data from the table
    for item in upcoming_events_table.get_children():
        upcoming_events_table.delete(item)

def load_upcoming_events():
    from datetime import datetime
    selected_date = date_picker.get()
    hall_name = hall_combobox.get()

    # Convert selected_date to the format used in the database
    formatted_date = datetime.strptime(selected_date, "%m/%d/%y").strftime("%m/%d/%y")
    

    today = dt_date.today()
    format_date = today.strftime("%m/%d/%y")
    clear_table()  # Clear existing data from the table

    #soc
    # Make sure the limit_value is not mistakenly set to 10000000
    limit_value = 5

    
    query = "SELECT * FROM booking ORDER BY program_date DESC LIMIT 5;"
    cursor.execute(query)# (format_date, hall_name, limit_value))
    #soc

    # Query with the same date format as stored in the database
    # query = "SELECT * FROM booking WHERE program_date >= ? AND hall_name = ? ORDER BY program_date  LIMIT 5;"
    # cursor.execute(query, (format_date, hall_name))
    upcoming_events = cursor.fetchall()

    for event in upcoming_events:
        upcoming_events_table.insert('', 'end', values=event)


def on_date_or_hall_change(event):
    clear_table()  # Clear existing data from the table
    load_upcoming_events()  # Reload upcoming events based on new date or hall


# Initialize Tkinter window
root = tk.Tk()
root.geometry("600x400")
root.title("Hall Booking System")

# Database connection
try:
    conn = sqlite3.connect("hall_data.db")
    cursor = conn.cursor()
except sqlite3.Error as e:
    print("Database connection error:", e)

# Widgets
date_label = ttk.Label(root, text="Select Date:")
date_label.pack()

date_picker = DateEntry(root, width=12, background="lightyellow2")
date_picker.pack()

hall_label = ttk.Label(root, text="Select Hall:")
hall_label.pack()

hall_list = ["Rukmini Auditorium", "Aryabhatta Hall", "Vinobha Bhave Hall", "Einstein Hall", "Exhibition Hall"]
hall_combobox = ttk.Combobox(root, values=hall_list)
hall_combobox.set(hall_list[0])
hall_combobox.pack()

availability_btn = ttk.Button(root, text="Check Availability", command=check_availability)
availability_btn.pack()

availability_status = ttk.Label(root, text="", font=("Arial", 20))
availability_status.pack()

# Label for Upcoming Bookings
upcoming_label = ttk.Label(root, text="Upcoming Bookings", font=("Arial", 15))
upcoming_label.pack()

# Upcoming Events Table
upcoming_events_table = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings", height=7)

# Set widths for columns individually
column_names = ["ID", "Name", "Mobile no.", "Email-Id", "Book date", "From", "To", "Hall Name"]
column_widths = [100, 150, 120, 160, 100, 80, 80, 120]  # Adjust widths as needed

for idx, col_name in enumerate(column_names):
    upcoming_events_table.column(idx + 1, width=column_widths[idx])
    upcoming_events_table.heading(idx + 1, text=col_name)

upcoming_events_table.pack()

# Bind the on_date_or_hall_change function to DateEntry and Combobox events
date_picker.bind("<<DateEntrySelected>>", on_date_or_hall_change)
hall_combobox.bind("<<ComboboxSelected>>", on_date_or_hall_change)

# Load Upcoming Events initially
load_upcoming_events()

root.mainloop()

#---------------------- End of code -------------------------