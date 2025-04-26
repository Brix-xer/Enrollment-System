import tkinter as tk
from tkinter import simpledialog, Menu, messagebox, Toplevel, Label, Entry, Button, Listbox, Scrollbar
import calendar
from datetime import datetime
import mysql.connector
from PIL import Image, ImageTk
from tkcalendar import DateEntry  # Import the DateEntry class

# Database connection functions
def get_db_connection():
    return mysql.connector.connect(
        host="145.223.108.159",
        user="u507702827_hiholc",
        password="Hiholearningcenter123",
        database="u507702827_hihodatabase"
    )

def save_event_to_db(date, title, time, name):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO calendar (date, title, time, Name) VALUES (%s, %s, %s, %s)"  # Note: Added Name
    cursor.execute(query, (date, title, time, name))  
    conn.commit()
    cursor.close()
    conn.close()


def load_events_from_db(year, month):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT date, title, time, Name FROM calendar WHERE YEAR(date) = %s AND MONTH(date) = %s"
    cursor.execute(query, (year, month))
    events = cursor.fetchall()
    cursor.close()
    conn.close()

    return events


def delete_event_from_db(date, title, time):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM calendar WHERE date = %s AND title = %s AND time = %s"
    cursor.execute(query, (date, title, time))
    conn.commit()
    cursor.close()
    conn.close()

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Functional Schedule Calendar")
        self.root.geometry("800x600")  # Setting the size of the main window
        self.root.configure(bg="#2C3E50")
        
        self.center_window(self.root, 800, 600)  # Centering the main window

        self.auto_refresh_interval = None
        self.selected_date = None  # Ensure this is initialized here

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.current_day = None

        # Dictionary to store events
        self.events = {}
        self.tooltip = None

        self.original_title = None
        self.original_time = None

        # Bind the close protocol to the custom handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()

    def center_window(self, dialog, width, height):
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate x and y coordinates for the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Set the geometry of the dialog
        dialog.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="High Horizons Learning Center", font=("Arial", 24, "bold"), bg="#34495e", fg="white")
        self.title_label.grid(row=0, column=0, columnspan=7, sticky="nsew")

        self.subtitle_label = tk.Label(self.root, text="SCHEDULE CALENDAR", font=("Arial", 16, "bold"), bg="#34495e", fg="white")
        self.subtitle_label.grid(row=1, column=0, columnspan=7, sticky="nsew")

        self.month_label = tk.Label(self.root, font=("Arial", 14, "bold"), bg="#34495e", fg="white", width=50, height=2)
        self.month_label.grid(row=2, column=0, columnspan=5, sticky="w", padx=10)

        # Date Picker
        self.date_picker = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.date_picker.grid(row=2, column=3, padx=10, pady=10)
        self.date_picker.bind("<<DateEntrySelected>>", self.on_date_selected)

       # Navigation buttons
        self.prev_button = tk.Button(self.root, text="<", font=("Arial", 12, "bold"), command=self.prev_month, bg="#3498DB", fg="white", relief="raised", borderwidth=2, width=3)
        self.prev_button.grid(row=2, column=5, sticky="e")  # Changed the column from 6 to 5

        self.next_button = tk.Button(self.root, text=">", font=("Arial", 12, "bold"), command=self.next_month, bg="#3498DB", fg="white", relief="raised", borderwidth=2, width=3)
        self.next_button.grid(row=2, column=6, sticky="w")  # Changed the column from 7 to 6

        # Hover effects
        self.next_button.bind("<Enter>", lambda e: self.next_button.config(bg="#2980B9"))
        self.next_button.bind("<Leave>", lambda e: self.next_button.config(bg="#3498DB"))

        self.prev_button.bind("<Enter>", lambda e: self.prev_button.config(bg="#2980B9"))
        self.prev_button.bind("<Leave>", lambda e: self.prev_button.config(bg="#3498DB"))

        # Days of the week labels
        self.days_of_week = ["SUN", "MON", "TUE", "WED", "THUR", "FRI", "SAT"]
        for idx, day in enumerate(self.days_of_week):
            day_label = tk.Label(self.root, text=day, font=("Arial", 12, "bold"), bg="#34495e", fg="white")
            day_label.grid(row=3, column=idx, sticky="nsew", padx=2, pady=2)

        self.create_calendar(self.current_year, self.current_month)


    def create_calendar(self, year, month):
        # Clear the existing calendar (if any)
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) > 3:
                widget.grid_forget()

        # Update the month label
        self.month_label.config(text=f"{calendar.month_name[month]} {year}")

        # Get the days for the current month
        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)

        # Load events from the database
        events_from_db = load_events_from_db(year, month)
        self.events = {}

        for date, title, time, name in events_from_db:  # Load four fields from DB
            day = int(date.split('-')[2])
            event_details = (title, time, name)
            if day in self.events:
                self.events[day].append(event_details)
            else:
                self.events[day] = [event_details]

        today = datetime.now()
        today_date_str = today.strftime("%Y-%m-%d")

        cell_width = 12
        cell_height = 5

        for row_idx, week in enumerate(month_days, start=4):
            for col_idx, day in enumerate(week):
                if day == 0:
                    day_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#3E5871", fg="white", width=cell_width, height=cell_height)
                else:
                    events_text = "\n".join(f"{title} at {time} by {name}" for title, time, name in self.events.get(day, []))

                    if len(events_text.splitlines()) > 3:
                        events_text = "\n".join(events_text.splitlines()[:3]) + "\n...more"

                    event_bg_color = "#3E5871" 
                    event_date_str = f"{year}-{month:02d}-{day:02d}"

                    if today_date_str > event_date_str and day in self.events:
                        event_bg_color = "red"
                    elif today_date_str < event_date_str and day in self.events:
                        event_bg_color = "orange"
                    elif day in self.events:
                        event_bg_color = "darkgreen"

                    highlight_color = event_bg_color
                    if day == today.day and self.current_year == today.year and self.current_month == today.month:
                        highlight_color = "lightgreen"
                    elif self.selected_date and day == self.selected_date.day and month == self.selected_date.month and year == self.selected_date.year:
                        highlight_color = "lightblue"  # Light blue for selected date

                    # Create the day button with the correct text and background color
                    day_label = tk.Button(
                        self.root,
                        text=f"{day}\n{events_text}",
                        font=("Arial", 12),
                        bg=highlight_color,
                        fg="white",
                        command=lambda d=day: self.add_event(d),
                        width=cell_width,
                        height=cell_height,
                        relief="flat"
                    )

                day_label.bind("<Button-3>", lambda e, d=day: self.show_context_menu(e, d))
                day_label.bind("<Enter>", lambda e, d=day: self.show_tooltip(e, d))
                day_label.bind("<Leave>", self.hide_tooltip)

                day_label.grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2)

        for i in range(7):
            self.root.columnconfigure(i, weight=1)
        for i in range(10):
            self.root.rowconfigure(i, weight=1)

    def on_date_selected(self, event):
        selected_date = self.date_picker.get_date()
        self.selected_date = selected_date  # Store the selected date
        self.current_year = selected_date.year
        self.current_month = selected_date.month
        self.create_calendar(self.current_year, self.current_month)

    def show_tooltip(self, event, day):
        if day in self.events:
            # Format the tooltip
            events_text = "\n".join(f"{title} at {time} for {name}" for title, time, name in self.events[day])
            self.tooltip = tk.Toplevel(self.root)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

            # Add a label with event details
            label = tk.Label(self.tooltip, text=events_text, background="yellow", borderwidth=1, relief="solid", padx=5, pady=5, font=("Arial", 10))
            label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def add_event(self, day):
        self.current_day = day
        self.open_event_dialog(action="add", day=day)

    def show_context_menu(self, event, day):
        # Create and show the context menu
        context_menu = Menu(self.root, tearoff=0, bg="#ECF0F1", fg="#2C3E50")
        context_menu.add_command(label="Edit Event", command=lambda: self.select_event(day), background="#BDC3C7", activebackground="#BDC3C7")
        context_menu.add_command(label="Delete Event", command=lambda: self.select_event_to_delete(day), background="#BDC3C7", activebackground="#BDC3C7")
        context_menu.post(event.x_root, event.y_root)
        
    def select_event_to_delete(self, day):
        if day in self.events:
            # Create and configure the dialog for deleting
            dialog = Toplevel(self.root)
            dialog.title("Select Event to Delete")
            dialog.geometry("400x300")
            dialog.configure(bg="#2C3E50")

            Label(dialog, text="Select Event to Delete:", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white").pack(padx=10, pady=10)

            # Create a frame to hold the listbox and scrollbar
            frame = tk.Frame(dialog, bg="#2C3E50")
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Create a listbox with a vertical scrollbar
            listbox = Listbox(frame, bg="#ECF0F1", fg="#2C3E50", selectmode=tk.SINGLE, font=("Arial", 12))
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar = Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox.config(yscrollcommand=scrollbar.set)

            # Function to populate the listbox with events
            def populate_listbox():
                listbox.delete(0, tk.END)  # Clear the listbox
                # Check if the day exists in the events dictionary
                if day in self.events:
                    for title, time, name in self.events[day]:  # Unpack all three values
                        listbox.insert(tk.END, f"{title} at {time} for {name}")  # Include name in the display
                else:
                    # Optionally add a message or do nothing if there are no events
                    listbox.insert(tk.END, "No events for this day.")

            # Initially populate the listbox when the dialog opens
            populate_listbox()

            # Create buttons to delete or cancel
            button_frame = tk.Frame(dialog, bg="#2C3E50")
            button_frame.pack(pady=10)

        # Update delete_event to refresh the listbox after deletion
        def delete_and_refresh():
            selected_event = listbox.get(tk.ACTIVE)
            if selected_event:  # Check if an event is selected
                # Parse the selected event to extract title and time
                try:
                    title_time, name = selected_event.rsplit(" for ", 1)  # Split into title+time and name
                    title, time = title_time.split(" at ")  # Split title and time
                    self.delete_event(day, (title, time, name))  # Pass all three values to delete_event
                except ValueError:
                    messagebox.showerror("Error", "Failed to parse the selected event.")
                populate_listbox()  # Refresh the listbox

        Button(button_frame, text="Delete", command=delete_and_refresh, bg="#E74C3C", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        Button(button_frame, text="Cancel", command=dialog.destroy, bg="#3498DB", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    def edit_event(self, day, event_details):
        # Parse the selected event details
        try:
            title_time, name = event_details.rsplit(" for ", 1) 
            title, time = title_time.split(" at ")  

            # Ensure current_day is set correctly
            self.current_day = day  # Set current_day to the day being edited
            self.original_title = title
            self.original_time = time

        except ValueError:
            print("Error parsing event details. Ensure the format is correct.")  
            return

        # Open the event dialog for editing, passing the original title and time
        self.open_event_dialog(action="edit", day=day, original_title=title, original_time=time, title=title, time=time, name=name)

    def select_event(self, day):
        if day in self.events and self.events[day]:  # Check if there are events for the day
            self.current_day = day  # Set the current day to the selected day
            self.dialog = Toplevel(self.root)
            self.dialog.title("Select Event to Edit")
            self.dialog.geometry("400x300")
            self.dialog.configure(bg="#2C3E50")

            Label(self.dialog, text="Select Event to Edit:", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white").pack(padx=10, pady=10)

            self.event_listbox = Listbox(self.dialog, bg="#ECF0F1", fg="#2C3E50", selectmode=tk.SINGLE, font=("Arial", 12))
            self.event_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.scrollbar = Scrollbar(self.dialog, orient=tk.VERTICAL, command=self.event_listbox.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.event_listbox.config(yscrollcommand=self.scrollbar.set)

            # Load the list of events for the selected day
            for title, time, name in self.events.get(day, []):
                entry = f"{title} at {time} for {name}"
                self.event_listbox.insert(tk.END, entry)  # Add each event to the listbox

            # Create buttons to edit or cancel
            button_frame = tk.Frame(self.dialog, bg="#2C3E50")
            button_frame.pack(pady=10)

            # Edit button
            Button(button_frame, text="Edit", 
                command=lambda: self.edit_event(day, self.event_listbox.get(tk.ACTIVE)), 
                bg="#3498DB", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

            # Cancel button
            Button(button_frame, text="Cancel", command=self.dialog.destroy, bg="#E74C3E", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        else:
            messagebox.showinfo("No Events", "No events found for this day.")

    def load_event_list(self, day):
        if self.event_listbox.winfo_exists():
            self.event_listbox.delete(0, tk.END)  # Clear the listbox

            # Reload events for the selected day
            events_from_db = load_events_from_db(self.current_year, self.current_month)
            self.events = {}

            for date, title, time, name in events_from_db:
                event_day = int(date.split('-')[2])
                event_details = (title, time, name)  # Store as a tuple
                if event_day in self.events:
                    # Append only if this isn't a duplicate
                    if event_details not in self.events[event_day]:
                        self.events[event_day].append(event_details)
                else:
                    self.events[event_day] = [event_details]  # Initialize with a new list

    def start_auto_refresh(self, day):
        if self.event_listbox.winfo_exists():  # Ensure the Listbox is still valid
            self.load_event_list(day)
            # Cancel any existing automatic refresh if in progress
            if self.auto_refresh_interval is not None:
                self.root.after_cancel(self.auto_refresh_interval)

            # Schedule the next call
            self.auto_refresh_interval = self.root.after(5000, self.start_auto_refresh, day)  # Refresh every 5000 ms

    def delete_event(self, day, event_details):
        title, time, name = event_details  # Unpack all three values
        delete_event_from_db(self.current_year, title, time)  # Pass title and time to the database function
        self.create_calendar(self.current_year, self.current_month)  # Refresh the calendar

    def open_event_dialog(self, action, day, original_title=None, original_time=None, title="", time="", name=""):
        dialog = Toplevel(self.root)
        dialog.title(f"{action.capitalize()} Event")

        # Center the dialog
        self.center_window(dialog, 400, 300)  # Width and height of the dialog

        dialog.configure(bg="#2C3E50")

        Label(dialog, text=f"{action.capitalize()} Event:", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white").grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        Label(dialog, text="Date:", bg="#2C3E50", fg="white", font=("Arial", 12)).grid(row=1, column=0, padx=10, sticky='e')  # Align right
        date_entry = DateEntry(dialog, font=("Arial", 12), date_pattern='y-mm-dd')  # New date entry field
        date_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')  # Fill horizontally

        # Set date for editing correctly
        try:
            edit_date = datetime(self.current_year, self.current_month, day)  # Create datetime object
            date_entry.set_date(edit_date)
        except ValueError:
            messagebox.showerror("Date Error", f"The selected date is invalid: {self.current_year}-{self.current_month:02d}-{day:02d}")

        Label(dialog, text="Title:", bg="#2C3E50", fg="white", font=("Arial", 12)).grid(row=2, column=0, padx=10, sticky='e')  # Align right
        title_entry = Entry(dialog, font=("Arial", 12))
        title_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')  # Fill horizontally
        title_entry.insert(0, title)  # Pre-fill title

        Label(dialog, text="Time:", bg="#2C3E50", fg="white", font=("Arial", 12)).grid(row=3, column=0, padx=10, sticky='e')  # Align right
        time_entry = Entry(dialog, font=("Arial", 12))
        time_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')  # Fill horizontally
        time_entry.insert(0, time)  # Pre-fill time

        Label(dialog, text="Name:", bg="#2C3E50", fg="white", font=("Arial", 12)).grid(row=4, column=0, padx=10, sticky='e')  # Align right
        name_entry = Entry(dialog, font=("Arial", 12))
        name_entry.grid(row=4, column=1, padx=10, pady=5, sticky='ew')  # Fill horizontally
        name_entry.insert(0, name)  # Pre-fill name

        # Use lambda to call save_event and pass the parameters correctly
        Button(dialog, text=action.capitalize(), 
            command=lambda: self.save_event(dialog, action, date_entry.get_date(), title_entry.get(), time_entry.get(), name_entry.get()), 
            bg="#3498DB", fg="white", font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=10)

        Button(dialog, text="Cancel", command=dialog.destroy, bg="#E74C3C", fg="white", font=("Arial", 12)).grid(row=5, column=1, padx=5, pady=10)

    def save_event(self, dialog, action, date, title, time, name):
        # Convert the date to the correct format (YYYY-MM-DD)
        date_str = date.strftime("%Y-%m-%d") if isinstance(date, datetime) else date

        if action == "add":
            save_event_to_db(date_str, title, time, name)  # Include name when adding an event
        elif action == "edit":
            if self.current_day is None:
                messagebox.showerror("Error", "No current day set for editing.")
                return  # Exit if current_day is not set
                
            original_date = f"{self.current_year}-{self.current_month:02d}-{self.current_day:02d}"
            delete_event_from_db(original_date, self.original_title, self.original_time)  # Use stored values
            save_event_to_db(date_str, title, time, name)  # Save the edited event with the new date

        dialog.destroy()  # Close the dialog after saving
        self.create_calendar(self.current_year, self.current_month)  # Refresh the calendar to show updated events updated events

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.create_calendar(self.current_year, self.current_month)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.create_calendar(self.current_year, self.current_month)

    def on_close(self):
        # Cancel any ongoing auto_refresh
        if self.auto_refresh_interval is not None:
            self.root.after_cancel(self.auto_refresh_interval)
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()