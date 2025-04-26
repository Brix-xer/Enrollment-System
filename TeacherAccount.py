import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Label, Canvas, Frame, Button, RIGHT, Y, LEFT, X, GROOVE, BOTH
from tkinter import ttk
import mysql.connector
from fpdf import FPDF
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from tkcalendar import DateEntry
import calendar
from datetime import datetime, date
import scheduling_calendar
from PIL import Image, ImageTk, ImageChops, ImageEnhance
import io
import subprocess
import tkinter.simpledialog as simpledialog
import random, string 
import tkinter as tk
from tkinter import ttk, font
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import PhotoImage
#=======================================================SQL CONNECETION====================================
connection=mysql.connector.connect(
        host="145.223.108.159",
        user="u507702827_hiholc",
        password="Hiholearningcenter123",
        database="u507702827_hihodatabase"
    )

cursor = connection.cursor()

def ensure_connection():
    global connection, cursor
    try:
        if connection.is_connected():
            connection.ping(reconnect=True)
        else:
            raise mysql.connector.Error
    except mysql.connector.Error:
        try:
            connection = mysql.connector.connect(
                host="145.223.108.159",
                user="u507702827_hiholc",
                password="Hiholearningcenter123",
                database="u507702827_hihodatabase"
            )
            cursor = connection.cursor()
            print("Database connection re-established.")
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            exit(1)  # Terminate program if connection fails 

def close_connection():
    try:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
        print("Database connection closed.")
    except mysql.connector.Error as err:
        print(f"Error closing the database connection: {err}")


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

    

def open_main_gui():
#==================================================LOAD OF DATA FROM SQL=================================
    def load_data(year_filter=None):
        global cursor
        for row in tree_table.get_children():
            tree_table.delete(row)

        ensure_connection()  # Ensure database connection is active
        connection.commit()  # Force MySQL to refresh

        # Close old cursor safely before reassigning
        if cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error:
                pass  # Ignore if cursor is already closed

        cursor = connection.cursor(buffered=True)  # Create a new cursor

        # Setup base query
        query = """
            SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                    father_age, father_email, father_occupation, father_contact, father_company, 
                    mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                    parents_status, date_enrolled, year, special_needs
            FROM student_history
        """

        if year_filter:
            query += " WHERE year = %s"

        cursor.execute(query, (year_filter,) if year_filter else ())

        for row in cursor.fetchall():
            table_insert_student_data(row)

    def update_year_label(year):
        year_label.config(text=f"YEAR: {year}")

    def load_studentml_data():
        global cursor  # Explicitly declare cursor as global

        # Clear the current treeview data
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)

        ensure_connection()  # Ensure database connection is active
        connection.commit()  # Force MySQL to refresh

        # Close old cursor safely before reassigning
        if cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error:
                pass  # Ignore if cursor is already closed

        cursor = connection.cursor(buffered=True)  # Create a new cursor

        # Get the current date and determine the school year range
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        # Calculate the start and end years based on the school year (June to March)
        if current_month >= 6:  # If June or later, the school year starts this year
            start_year = current_year
            end_year = current_year + 1
        else:  # If before June, the school year started last year
            start_year = current_year - 1
            end_year = current_year

        # Clear the full_data list
        full_data.clear()

        # Define the SQL query dynamically for the school year range
        query = """
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture, date_enrolled
            FROM studentinfo
            WHERE 
                (
                    (MONTH(date_enrolled) BETWEEN 6 AND 12 AND YEAR(date_enrolled) = %s) OR 
                    (MONTH(date_enrolled) BETWEEN 1 AND 3 AND YEAR(date_enrolled) = %s)
                );
        """

        # Execute the query with the dynamic year parameters
        cursor.execute(query, (start_year, end_year))

        # Fetch all matching rows
        student_info_rows = cursor.fetchall()

        # Add the data to full_data and insert into the treeview
        for row in student_info_rows:
            full_data.append(row)
            insert_student_data(row)

    def load_previous_year_students():
        global cursor  

        # Clear the Treeview before loading new data
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)

        ensure_connection()  
        connection.commit()  

        if cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error:
                pass  

        cursor = connection.cursor(buffered=True)  

        # Get the previous school year range
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        if current_month >= 5:
            last_start_year = current_year - 1
        else:
            last_start_year = current_year - 2  # If before May, go back two years

        last_end_year = last_start_year + 1  # Previous school year (May - April)

        # Update the YEAR label
        year_label.config(text=f"{last_start_year}-{last_end_year}")

        # Clear the full_data list
        full_data.clear()

        # Query to fetch students from the previous school year
        query = """
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture, date_enrolled
            FROM studentinfo
            WHERE 
                (
                    (MONTH(date_enrolled) >= 5 AND YEAR(date_enrolled) = %s)  -- May to December of last year
                    OR 
                    (MONTH(date_enrolled) <= 4 AND YEAR(date_enrolled) = %s)  -- January to April of this year
                );
        """

        cursor.execute(query, (last_start_year, last_end_year))  # Fetch previous year

        student_info_rows = cursor.fetchall()

        # Add data to full_data and insert into the Treeview
        for row in student_info_rows:
            full_data.append(row)
            insert_student_data(row)

        messagebox.showinfo("Success", f"Now viewing students from {last_start_year}-{last_end_year}.")


    def load_balance_data():
        finance_data.clear()

        # Get the current date
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        # Determine the current school year
        if current_month >= 5:
            start_year = current_year
        else:
            start_year = current_year - 1  # If before May, consider the previous year as the start

        end_year = start_year + 1  # School year runs from May of start_year to April of end_year

        query = """
            SELECT * FROM student_balance 
            WHERE student_id = %s 
            AND (
                (MONTH(date_enrolled) >= 5 AND YEAR(date_enrolled) = %s)  -- May to December of start_year
                OR 
                (MONTH(date_enrolled) <= 4 AND YEAR(date_enrolled) = %s)  -- January to April of end_year
            )
        """

        cursor.execute(query, (selected_student[0], start_year, end_year))
        finance_info_rows = cursor.fetchall()

        for finance_row in finance_info_rows:
            finance_data.append(finance_row)

    def load_special_needs_data():
        special_needs_data.clear()

        cursor.execute("SELECT student_id, special_needs FROM studentinfo WHERE student_id = %s", (selected_student[0],))
        special_needs_info_rows = cursor.fetchall()
        for special_needs_row in special_needs_info_rows:
            special_needs_data.append(special_needs_row)
#========================================================================================================

#================================================NAV BAR NAVIGATION COMMANDS=========================
    def show_dashboard_panel():
        dashboard_frame.tkraise()

    def show_table_panel():
        table_frame.tkraise()
        load_data()

    def show_studentmasterlist_panel():
        studentml_frame.tkraise()
        load_studentml_data()

    def logout():
        response = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if response:
            close_connection()  # <-- Add this
            main_root.destroy()
            subprocess.run(["python", "login.py"])

#============================================UPDATE DATAGIRDVIEW CODE======================================

    def load_requirement_checklist(student_id, checklist_frame):
        # Fetch student's grade level from studentinfo table
        cursor.execute("SELECT grade_level FROM studentinfo WHERE student_id = %s", (student_id,))
        result = cursor.fetchone()
        grade_level = result[0].strip() if result else None  # Remove extra spaces

        # Clear previous checklist items
        for widget in checklist_frame.winfo_children():
            widget.destroy()

        # Define checklist items (Display Name → Database Column Mapping)
        checklist_items = {
            "PSA": "PSA",
            "SF9/ECCD": "SF9/ECCD",
            "SF10": "SF10",
            "MC": "MC",
            "ACR": "ACR",
            "P/E-C": "P/E-C",
            "Proof of Billing": "proof_of_billing"
        }

        # Show "Baby Book" only for Kindergarten, Senior Nursery, and Junior Nursery
        if grade_level in ["Kindergarten", "Senior Nursery", "Junior Nursery"]:
            checklist_items["Baby Book"] = "baby_book"

        # Fetch column names dynamically
        cursor.execute("SHOW COLUMNS FROM requirement_checklist")  
        columns = [col[0] for col in cursor.fetchall()]  # Extract column names

        # Fetch current checklist status from the database
        cursor.execute("SELECT * FROM requirement_checklist WHERE id = %s", (student_id,))
        row = cursor.fetchone()

        # Convert fetched data into a dictionary for correct column mapping
        requirements = dict(zip(columns, row)) if row else {}

        # Title Label for Checklist
        title_label = tk.Label(
            checklist_frame, text="Requirement Checklist", font=('Arial', 14, 'bold'), 
            bg="#34495e", fg="white", pady=5
        )
        title_label.grid(row=0, column=0, columnspan=len(checklist_items), sticky="ew", pady=10)

        # Create labels in a horizontal layout
        for index, (display_name, db_column) in enumerate(checklist_items.items()):
            status = "✔" if requirements.get(db_column, 0) else "✘"  # Check or cross mark
            lbl = tk.Label(
                checklist_frame, text=f"{display_name}: {status}", font=('Arial', 12), 
                bg="#ecf0f1", padx=5, pady=5
            )
            lbl.grid(row=1, column=index, padx=10, pady=5, sticky="w")  # Horizontal layout

        # Ensure labels expand properly
        checklist_frame.grid_columnconfigure(tuple(range(len(checklist_items))), weight=1)



    def on_row_double_click(event):
        selected_item = tree_studentml.focus()
        if not selected_item:
            messagebox.showinfo("No Selection", "No student selected.")
            return

        selected_student = tree_studentml.item(selected_item)['values']
        if not selected_student:
            messagebox.showinfo("No Data", "No student data found.")
            return
        
        show_student_profile_panel()
        load_balance_data()



    def show_student_profile_panel():
        global id_entry, grade_entry, name_entry, address_text, selected_student, checkbox_vars
        global fathers_name_entry, fathers_occupation_entry
        global mothers_name_entry, mothers_occupation_entry, contact_number_entry

        checkbox_vars = {}

        student_profile_frame = tk.Frame(content_frame, bg="#f4f4f4")  # Light gray background
        student_profile_frame.grid(row=0, column=0, sticky="nsew")

        for widget in student_profile_frame.winfo_children():
            widget.destroy()

        selected_item = tree_studentml.focus()
        if not selected_item:
            messagebox.showinfo("No Selection", "No student selected.")
            return

        selected_student = tree_studentml.item(selected_item)['values']
        if not selected_student:
            messagebox.showinfo("No Data", "No student data found.")
            return

        # Create the info frame with padding and background styling
        info_frame = tk.Frame(student_profile_frame, bg="#ffffff", bd=2, relief="solid", padx=20, pady=20)
        info_frame.grid(row=0, column=0, sticky='nsew')

        # Fetch the profile picture from the database
        try:
            cursor = connection.cursor()

            # Query the profile_picture column for the selected student
            student_id = selected_student[0]  # Assuming selected_student[0] is the student ID
            query = "SELECT profile_picture FROM studentinfo WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()

            if result and result[0]:  # Check if the profile picture exists
                profile_picture_data = result[0]  # Binary data of the profile picture

                # Convert binary data to a file-like object
                profile_image_file = io.BytesIO(profile_picture_data)

                # Load the image from the file-like object
                profile_image = Image.open(profile_image_file)
                profile_image = profile_image.resize((120, 90), Image.Resampling.LANCZOS)  # Resize the image
                profile_photo = ImageTk.PhotoImage(profile_image)

                # Create a label to display the image
                profile_label = tk.Label(info_frame, image=profile_photo, bg="#ffffff")
                profile_label.image = profile_photo  # Keep a reference to avoid garbage collection
                profile_label.place(x=880, y=65)  # Adjust x and y values as needed
            else:
                # If no profile picture is available, display a placeholder
                placeholder_label = tk.Label(info_frame, text="No Image", bg="#ffffff", fg="#000000", font=('Arial', 12))
                placeholder_label.place(x=900, y=65)  # Adjust position as needed

        except mysql.connector.Error as err:
            print(f"Error fetching profile picture: {err}")
            # If there's an error, display a placeholder
            placeholder_label = tk.Label(info_frame, text="No Image", bg="#ffffff", fg="#000000", font=('Arial', 12))
            placeholder_label.place(x=250, y=20)  # Adjust position as needed


        # Rest of your existing code remains unchanged...
        tk.Label(info_frame, text="STUDENT DETAILS", font=('Arial', 18, 'bold'), bg="#3498db", fg="white", padx=30, pady=10).grid(row=0, column=0, columnspan=4, pady=10, sticky='ew')
        # Style for Labels and Entry Widgets
        label_font = ('Arial', 12, 'bold')
        entry_font = ('Arial', 12)

        # Create and place student ID and Grade Level labels and entries
        tk.Label(info_frame, text="Student ID:", font=label_font, bg="#ffffff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        id_entry = tk.Entry(info_frame, width=40, font=entry_font, bd=2, relief="solid", bg="#ecf0f1")
        id_entry.grid(row=2, column=0, padx=5, pady=5)
        id_entry.insert(0, selected_student[0])  # Auto-fill the ID
        id_entry.config(state='readonly')  # Making Student ID read-only

        tk.Label(info_frame, text="Grade Lvl:", font=label_font, bg="#ffffff").grid(row=1, column=1, sticky='w', padx=5, pady=5)
        grade_entry = tk.Entry(info_frame, width=40, font=entry_font, bd=2, relief="solid", bg="#ecf0f1")
        grade_entry.grid(row=2, column=1, padx=5, pady=5)
        grade_entry.insert(0, selected_student[5])  # Auto-fill the Grade Level
        grade_entry.config(state='readonly')  # Making Grade Level read-only

        load_balance_data()

        selected_student_finance_data = next((row for row in finance_data if row[1] == selected_student[0]), None)

        tk.Label(info_frame, text="", font=label_font, bg="#ffffff").grid(row=3, column=1, sticky='w', padx=5, pady=5)

        notebook = ttk.Notebook(info_frame)
        notebook.grid(row=4, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

        details_tab = tk.Frame(notebook, bg="#ffffff")
        notebook.add(details_tab, text="Student Details")

        tk.Label(details_tab, text="LRN:", font=label_font, bg="#ffffff").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        lrn_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        lrn_entry.grid(row=0, column=1, padx=5, pady=5)
        lrn_entry.insert(0, selected_student[1])
        lrn_entry.config(state='readonly')

        tk.Label(details_tab, text="Last Name:", font=label_font, bg="#ffffff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        name_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        name_entry.insert(0, selected_student[2])
        name_entry.config(state='readonly')

        tk.Label(details_tab, text="First Name:", font=label_font, bg="#ffffff").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        first_name_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        first_name_entry.grid(row=2, column=1, padx=5, pady=5)
        first_name_entry.insert(0, selected_student[3])
        first_name_entry.config(state='readonly')

        tk.Label(details_tab, text="Nickname:", font=label_font, bg="#ffffff").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        nickname_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        nickname_entry.grid(row=3, column=1, padx=5, pady=5)
        nickname_entry.insert(0, selected_student[4])
        nickname_entry.config(state='readonly')

        tk.Label(details_tab, text="Age:", font=label_font, bg="#ffffff").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        age_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        age_entry.grid(row=4, column=1, padx=5, pady=5)
        age_entry.insert(0, selected_student[6])
        age_entry.config(state='readonly')

        tk.Label(details_tab, text="Gender:", font=label_font, bg="#ffffff").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        gender_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        gender_entry.grid(row=5, column=1, padx=5, pady=5)
        gender_entry.insert(0, selected_student[7])
        gender_entry.config(state='readonly')

        tk.Label(details_tab, text="Date of Birth:", font=label_font, bg="#ffffff").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        birthday_entry = DateEntry(details_tab, width=40, font=entry_font, background='darkblue', foreground='white', borderwidth=2)
        birthday_entry.grid(row=6, column=1, padx=5, pady=5)

        birthday_value = selected_student[8]
        if birthday_value and isinstance(birthday_value, str):
            try:
                birthday_entry.set_date(datetime.strptime(birthday_value, '%Y-%m-%d'))
                birthday_entry.config(state='disabled')
            except ValueError as ve:
                messagebox.showerror("Date Format Error", f"This student has no Birthdate, please update immediately")
                birthday_entry.set_date(datetime.now())
                birthday_entry.config(state='disabled')
        else:
            birthday_entry.set_date(datetime.now())
            birthday_entry.config(state='disabled')

        tk.Label(details_tab, text="Address:", font=label_font, bg="#ffffff").grid(row=7, column=0, sticky='w', padx=5, pady=5)
        address_text = tk.Text(details_tab, font=entry_font, height=4, width=40, bg="#ecf0f1")
        address_text.grid(row=7, column=1, padx=5, pady=5)
        address_text.insert('1.0', selected_student[9])
        address_text.config(state='disabled')

        parents_tab = tk.Frame(notebook, bg="#ffffff")
        notebook.add(parents_tab, text="Parents Info")

        tk.Label(parents_tab, text="Father's Name:", font=label_font, bg="#ffffff").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        fathers_name_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_name_entry.grid(row=0, column=1, padx=5, pady=5)
        fathers_name_entry.insert(0, selected_student[10])
        fathers_name_entry.config(state='readonly')

        tk.Label(parents_tab, text="Father's Age:", font=label_font, bg="#ffffff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        fathers_age_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_age_entry.grid(row=1, column=1, padx=5, pady=5)
        fathers_age_entry.insert(0, selected_student[11])
        fathers_age_entry.config(state='readonly')

        tk.Label(parents_tab, text="Father's Email:", font=label_font, bg="#ffffff").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        fathers_email_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_email_entry.grid(row=2, column=1, padx=5, pady=5)
        fathers_email_entry.insert(0, selected_student[12])
        fathers_email_entry.config(state='readonly')

        tk.Label(parents_tab, text="Father's Occupation:", font=label_font, bg="#ffffff").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        fathers_occupation_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_occupation_entry.grid(row=3, column=1, padx=5, pady=5)
        fathers_occupation_entry.insert(0, selected_student[13])
        fathers_occupation_entry.config(state='readonly')

        tk.Label(parents_tab, text="Father's Contact Number:", font=label_font, bg="#ffffff").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        fathers_contact_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_contact_entry.grid(row=4, column=1, padx=5, pady=5)
        fathers_contact_entry.insert(0, selected_student[14])
        fathers_contact_entry.config(state='readonly')

        tk.Label(parents_tab, text="Father's Company:", font=label_font, bg="#ffffff").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        fathers_company_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_company_entry.grid(row=5, column=1, padx=5, pady=5)
        fathers_company_entry.insert(0, selected_student[15])
        fathers_company_entry.config(state='readonly')

        tk.Label(parents_tab, text="Mother's Name:", font=label_font, bg="#ffffff").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        mothers_name_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_name_entry.grid(row=0, column=3, padx=5, pady=5)
        mothers_name_entry.insert(0, selected_student[16])
        mothers_name_entry.config(state='readonly')

        tk.Label(parents_tab, text="Mother's Age:", font=label_font, bg="#ffffff").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        mothers_age_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_age_entry.grid(row=1, column=3, padx=5, pady=5)
        mothers_age_entry.insert(0, selected_student[17])
        mothers_age_entry.config(state='readonly')

        tk.Label(parents_tab, text="Mother's Email:", font=label_font, bg="#ffffff").grid(row=2, column=2, sticky='w', padx=5, pady=5)
        mothers_email_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_email_entry.grid(row=2, column=3, padx=5, pady=5)
        mothers_email_entry.insert(0, selected_student[18])
        mothers_email_entry.config(state='readonly')

        tk.Label(parents_tab, text="Mother's Occupation:", font=label_font, bg="#ffffff").grid(row=3, column=2, sticky='w', padx=5, pady=5)
        mothers_occupation_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_occupation_entry.grid(row=3, column=3, padx=5, pady=5)
        mothers_occupation_entry.insert(0, selected_student[19])
        mothers_occupation_entry.config(state='readonly')

        tk.Label(parents_tab, text="Mother's Contact Number:", font=label_font, bg="#ffffff").grid(row=4, column=2, sticky='w', padx=5, pady=5)
        mothers_contact_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_contact_entry.grid(row=4, column=3, padx=5, pady=5)
        mothers_contact_entry.insert(0, selected_student[20])
        mothers_contact_entry.config(state='readonly')

        tk.Label(parents_tab, text="Mother's Company:", font=label_font, bg="#ffffff").grid(row=5, column=2, sticky='w', padx=5, pady=5)
        mothers_company_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_company_entry.grid(row=5, column=3, padx=5, pady=5)
        mothers_company_entry.insert(0, selected_student[21])
        mothers_company_entry.config(state='readonly')

        educational_bg_tab = tk.Frame(notebook, bg="#ffffff")
        notebook.add(educational_bg_tab, text="Educational Background")

        current_grade_level = selected_student[5]
        prev_grade_level = ""

        if current_grade_level == "Junior Nursery":
            prev_grade_level = "No History of school"
        elif current_grade_level == "Senior Nursery":
            prev_grade_level = "Junior Nursery"
        elif current_grade_level == "Kindergarten":
            prev_grade_level = "Senior Nursery"
        elif current_grade_level == "Grade 1":
            prev_grade_level = "Kindergarten"
        elif current_grade_level == "Grade 2":
            prev_grade_level = "Grade 1"
        elif current_grade_level == "Grade 3":
            prev_grade_level = "Grade 2"
        elif current_grade_level == "Grade 4":
            prev_grade_level = "Grade 3"
        elif current_grade_level == "Grade 5":
            prev_grade_level = "Grade 4"
        elif current_grade_level == "Grade 6":
            prev_grade_level = "Grade 5"
        else:
            prev_grade_level = "No Record of school history"

        tk.Label(educational_bg_tab, text="Previous Grade Level:", font=label_font, bg="#ffffff").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        prev_grade_entry = tk.Entry(educational_bg_tab, width=40, font=entry_font, bg="#ecf0f1")
        prev_grade_entry.grid(row=0, column=1, padx=5, pady=5)
        prev_grade_entry.insert(0, prev_grade_level)
        prev_grade_entry.config(state='readonly')
      
        load_special_needs_data()

        selected_student_special_needs_data = next((row for row in special_needs_data if row[0] == selected_student[0]), None)        

        tk.Label(educational_bg_tab, text="Special Needs:", font=label_font, bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky='nw')
        special_needs_text = tk.Text(educational_bg_tab, font=entry_font, height=4, width=80, bg="#ecf0f1")
        special_needs_text.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        special_needs_text.insert('1.0', selected_student_special_needs_data[1])
        special_needs_text.config(state='disabled')
    
        additional_info_tab = tk.Frame(notebook, bg="#ffffff")
        notebook.add(additional_info_tab, text="Additional Information")

        tk.Label(additional_info_tab, text="Remarks:", font=label_font, bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky='nw')
        remarks_text = tk.Text(additional_info_tab, font=entry_font, height=4, width=80, bg="#ecf0f1")
        remarks_text.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        view_remarks_button = tk.Button(additional_info_tab, text="View All Remarks", font=('Arial', 12), command=lambda: view_student_remarks(selected_student[0]), bg="#3498db", fg="white")
        view_remarks_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        tk.Label(additional_info_tab, text="Student Status:", font=label_font, bg="#ffffff").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        global student_status_combo
        student_status_combo = ttk.Combobox(additional_info_tab, values=["Active", "Inactive"], state='readonly', font=entry_font)
        student_status_combo.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        student_status_combo.set(selected_student[23])

        upload_button = tk.Button(additional_info_tab, text="Upload GRADES", font=('Arial', 12), command=upload_pdf_to_db, bg="#3498db", fg="white")
        upload_button.grid(row=6, column=1, padx=5, pady=10, sticky='w')

        view_button = tk.Button(additional_info_tab, text="Uploaded GRADES", font=('Arial', 12), 
                                command=lambda: view_uploaded_grades(selected_student[0]), bg="#2ecc71", fg="white")

        # Position the button using .place()
        view_button.place(x=280, y=272, width=160, height=33)  # Adjust x, y, width, and height as needed


        load_balance_data()

        selected_student_finance_data = next((row for row in finance_data if row[2] == selected_student[0]), None)

        tk.Label(additional_info_tab, text="Payment Type:", font=label_font, bg="#ffffff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        payment_type_var = tk.StringVar()
        payment_type_combobox = ttk.Combobox(additional_info_tab, textvariable=payment_type_var, font=entry_font, state='readonly')
        payment_type_combobox['values'] = ("Annual", "Semestral", "Quarterly", "Monthly")
        payment_type_combobox.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        if selected_student_finance_data and len(selected_student_finance_data) > 2:
            payment_type_combobox.set(selected_student_finance_data[8])
            payment_type_combobox.config(state='disabled')
        else:
            payment_type_combobox.set("Not Available")
            payment_type_combobox.config(state='disabled')

        def on_combobox_select(event):
            selected_value = payment_type_var.get()

        payment_type_combobox.bind("<<ComboboxSelected>>", on_combobox_select)

        tk.Label(additional_info_tab, text="Balance:", font=label_font, bg="#ffffff").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        balance_entry = tk.Entry(additional_info_tab, width=40, font=entry_font, bg="#ecf0f1")
        balance_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        

        if selected_student_finance_data and len(selected_student_finance_data) >= 4:
            balance_entry.insert(0, selected_student_finance_data[19])
            balance_entry.config(state='readonly')
        else:
            balance_entry.insert(0, "Not Available")
            balance_entry.config(state='readonly')

        tk.Label(additional_info_tab, text="Amount Paid:", font=label_font, bg="#ffffff").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        amount_paying_entry = tk.Entry(additional_info_tab, width=40, font=entry_font, bg="#ecf0f1")
        amount_paying_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        amount_paying_entry.config(state='readonly')

        tk.Label(additional_info_tab, text="Due Date:", font=label_font, bg="#ffffff").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        due_date_entry = DateEntry(additional_info_tab, width=40, font=entry_font, background='darkblue', 
                                foreground='white', borderwidth=2, date_pattern="yyyy-MM-dd")  
        due_date_entry.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        if selected_student_finance_data and len(selected_student_finance_data) >= 5:
            try:
                stored_due_date = datetime.strptime(str(selected_student_finance_data[10]), "%Y-%m-%d")  
                due_date_entry.set_date(stored_due_date)
                due_date_entry.config(state='disabled')
            except:
                due_date_entry.set_date(datetime.now()) 
                due_date_entry.config(state='disabled')
        else:
            due_date_entry.set_date(datetime.now())  
            due_date_entry.config(state='disabled')


        checklist_tab = tk.Frame(notebook, bg="#ffffff")
        notebook.add(checklist_tab, text="Requirement Checklist")

        tk.Label(checklist_tab, text="Requirement Checklist", font=('Arial', 18, 'bold'), bg="#ffffff").pack(pady=10)

        # Load the requirement checklist items for the selected student
        load_requirement_checklist(selected_student[0], checklist_tab)

        # Create Save and Back buttons
        button_frame = tk.Frame(student_profile_frame, bg="#f4f4f4")  # Container for buttons
        button_frame.grid(row=4, column=0, columnspan=4, pady=20)  # Position them below the info

        save_button = tk.Button(button_frame, text="Send Remark", command=lambda: save_student_data(selected_student[0]), font=('Arial', 12), bg="#27ae60", fg="#ffffff")
        save_button.pack(side=tk.LEFT, padx=10, pady=5)

        back_button = tk.Button(button_frame, text="Back", command=lambda: show_studentmasterlist_panel(), font=('Arial', 12), bg="#c0392b", fg="#ffffff")
        back_button.pack(side=tk.LEFT, padx=10, pady=5)


        def view_student_remarks(student_id):
            """Opens a new window displaying all remarks and their notification times for the selected student."""
            remarks_window = tk.Toplevel()
            remarks_window.title("Student Remarks History")
            remarks_window.geometry("500x400")

            tk.Label(remarks_window, text=f"Remarks History for Student ID: {student_id}", font=('Arial', 14, 'bold')).pack(pady=10)

            remarks_tree = ttk.Treeview(remarks_window, columns=("Notification Time", "Remarks"), show="headings", height=10)
            remarks_tree.pack(expand=True, fill="both", padx=10, pady=10)

            remarks_tree.heading("Notification Time", text="Notification Time")
            remarks_tree.heading("Remarks", text="Remarks")

            remarks_tree.column("Notification Time", width=150)
            remarks_tree.column("Remarks", width=350)

            # Fetch remarks from the database
            cursor.execute("SELECT notification_time, remarks FROM student_remarks WHERE student_id = %s ORDER BY notification_time DESC", (student_id,))
            remarks = cursor.fetchall()

            for row in remarks:
                remarks_tree.insert("", "end", values=row)

            close_button = tk.Button(remarks_window, text="Close", command=remarks_window.destroy, font=('Arial', 12), bg="#c0392b", fg="white")
            close_button.pack(pady=10)


        def save_student_data(student_id):
            remarks = remarks_text.get("1.0", tk.END).strip()
            upload_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  

            notification_for_remark = "You have a new Remark from one of the teachers"

            try:
                cursor.execute("""
                    INSERT student_remarks (student_id, remarks, update_reject, notification_time)
                               VALUES (%s, %s, %s, %s)
                """, (student_id, remarks, notification_for_remark, upload_timestamp))

                connection.commit()
                messagebox.showinfo("Success", "Remarks for student has been uploaded.")

                load_studentml_data()  

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error updating student data: {err}")


    def upload_pdf_to_db():
            # Open a file dialog for selecting a PDF file
            file_path = filedialog.askopenfilename(
                title="Select a PDF file",
                filetypes=[("PDF files", "*.pdf")]
            )

            if file_path:
                try:
                    cursor = connection.cursor()

                    # Get the PDF file name (basename) and remove the .pdf extension
                    pdf_filename = os.path.splitext(os.path.basename(file_path))[0]  # Remove the extension
                    upload_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp in YYYY-MM-DD HH:MM:SS format

                    # Open the file and read it as binary data
                    with open(file_path, 'rb') as file:
                        pdf_data = file.read()

                    # Assuming 'selected_student' is defined and contains the student's ID
                    query = "INSERT INTO upload_grading (student_id, files, file_name, upload_date) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (selected_student[0], pdf_data, pdf_filename, upload_timestamp))  # Include the file name and upload timestamp
                    connection.commit()

                    messagebox.showinfo("Success", "PDF file uploaded successfully.")
                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", f"Error: {e}")
                except Exception as e:
                    messagebox.showerror("File Error", f"Error reading file: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
            else:
                messagebox.showwarning("No File Selected", "Please select a PDF file to upload.")


    def view_uploaded_grades(student_id):
        grades_window = tk.Toplevel()
        grades_window.title("Uploaded Grades")
        grades_window.geometry("700x400")  # Adjusted width and height

        tk.Label(grades_window, text="Uploaded Grades", font=('Arial', 14, 'bold')).pack(pady=10)

        # Create Treeview
        grades_tree = ttk.Treeview(grades_window, columns=("ID", "File Name", "Upload Date"), show="headings")
        grades_tree.pack(expand=True, fill="both", padx=10, pady=10)

        grades_tree.heading("ID", text="ID")
        grades_tree.heading("File Name", text="File Name")
        grades_tree.heading("Upload Date", text="Upload Date")

        grades_tree.column("ID", width=100)  # Adjusted width
        grades_tree.column("File Name", width=350)  # Adjusted width
        grades_tree.column("Upload Date", width=200)  # Adjusted width

        # Fetch files from DB
        cursor.execute("SELECT id, file_name, upload_date FROM upload_grading WHERE student_id = %s", (student_id,))
        rows = cursor.fetchall()

        for row in rows:
            grades_tree.insert("", "end", values=row, iid=row[0])  # Use row ID for deletion

        # Delete Button
        def delete_selected_file():
            selected_item = grades_tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a file to delete.")
                return

            file_id = selected_item[0]  # Get selected file ID
            cursor.execute("DELETE FROM upload_grading WHERE id = %s", (file_id,))
            connection.commit()
            grades_tree.delete(selected_item)
            messagebox.showinfo("Success", "File deleted successfully.")

        delete_button = tk.Button(grades_window, text="Delete Selected", font=('Arial', 12), bg="#e74c3c", fg="white",
                                command=delete_selected_file)
        delete_button.pack(pady=10)

#=======================================================WINDOW + FRAMES + LAYOUT================================================
    main_root = tk.Toplevel()
    main_root.attributes('-fullscreen', True)  # Make it full screen
    main_root.title("Student Management System")
    width = 1300
    height = 700
    center_window(main_root, width, height)
    main_root.protocol("WM_DELETE_WINDOW", logout)
    main_root.resizable(False, False)
    

    main_root.columnconfigure(1, weight=1)
    main_root.rowconfigure(0, weight=1)

    nav_frame = tk.Frame(main_root, width=200, bg="#e81c1c")
    nav_frame.grid(row=0, column=0, sticky="ns")
    nav_frame.grid_propagate(False) 

    content_frame = tk.Frame(main_root, bg="#E81C1C")
    content_frame.grid(row=0, column=1, sticky="nsew")

    content_frame.columnconfigure(0, weight=1)
    content_frame.rowconfigure(0, weight=1)
    
    def add_top_right_label(parent_frame):
        """Adds an icon and a 'Welcome, Admin' label to the top right of the given frame."""
        bottom_margin = 20
        left_margin = -15
        top_right_frame = tk.Frame(parent_frame, bg="#0f1074")
        top_right_frame.place(relx=1.0, x=left_margin, rely=0.0, anchor="ne",y=bottom_margin)

        try:
            # Load and resize icon
            image_path = "images/man.png"  # Make sure this file exists
            original_image = Image.open(image_path)
            resized_image = original_image.resize((30, 30), Image.LANCZOS)
            icon = ImageTk.PhotoImage(resized_image)

            icon_label = tk.Label(top_right_frame, image=icon, bg="#0f1074")
            icon_label.image = icon  # Keep reference to prevent garbage collection
            icon_label.pack(side="top", padx=5)
        except Exception as e:
            print(f"Error loading icon: {e}")

        welcome_label = tk.Label(top_right_frame, text="TEACHER", font=('Arial', 14, 'bold'), bg="#0f1074", fg="#E4E6C9")
        welcome_label.pack(side="left")
#=======================================================BUTTON NAVIGATION PLUS STYLE============================
    # Function to load and resize the icon
    def load_icon(icon_path, size=(30, 30)):
        try:
            img = Image.open(icon_path)
            img = img.resize(size, Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            return img
        except Exception as e:
            print(f"Error loading image {icon_path}: {e}")
            return None

    # Try loading the main logo (hiho.png)
    try:
        img1 = Image.open("images/hiho.png")
        img1 = img1.resize((100, 100), Image.LANCZOS)
        img1 = ImageTk.PhotoImage(img1)
        image_label1 = tk.Label(nav_frame, image=img1, bg="#9f0000")
        image_label1.pack(padx=10, pady=10)
    except Exception as e:
        print(f"Error loading first image: {e}")

    # Load the icons for each button
    dashboard_icon = load_icon("images/dashboard.png")
    enrollment_icon = load_icon("images/enrollment.png")
    logout_icon = load_icon("images/logout.png")


    # Updated button styles
    btn_style = {
        'font': ('Arial', 12, 'bold'),
        'fg': '#FFFFFF',
        'bg': '#9f0000',  # Set same as nav background (or use 'SystemButtonFace' for full transparency)
        'bd': 0,
        'activebackground': '#3498DB',  # Background visible on click
        'activeforeground': '#FFFFFF',
        'relief': 'flat',
        'cursor': 'hand2',
        'compound': 'left',  # Align icon and text vertically
        'anchor': 'w',  # Align text sa kaliwa kasama ng icon
        'padx': 10,  
        'pady': 5
    }

    dropdown_btn_style = btn_style.copy()
    dropdown_btn_style.update({'bg': '#1ABC9C', 'activebackground': '#16A085'})

    active_button = None

    def on_enter(event):
        global active_button  # Ensure it's accessible globally

        if 'active_button' not in globals():
            active_button = None  # Initialize if not defined

        if event.widget != active_button:  # Only change background for non-active buttons
            event.widget.config(bg="lightgray")

    def on_leave(event):
        global active_button
        if event.widget != active_button:
            event.widget['background'] = '#9f0000'  # Revert background when mouse leaves
            
    def on_click(event):
        global active_button
        if active_button:  # Revert the background of the previously active button
            active_button['background'] = '#9f0000'  # Reset the old active button to its normal color
        active_button = event.widget  # Set clicked button as active
        event.widget['background'] = '#34495E'  # Active button background

    # Create main navigation buttons with icons
    nav_buttons = [
        ("Dashboard", dashboard_icon, show_dashboard_panel),
    ]

    for text, icon, command in nav_buttons:
        btn = tk.Button(nav_frame, text=text, image=icon, command=command, **btn_style)
        btn.pack(fill='x', pady=5, padx=10)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_click)  # Bind left mouse click

    # Enrollment dropdown definition (moved before Logout)
    def toggle_enrollment_dropdown():
        if enrollment_expanded.get():
            for btn in enrollment_buttons:
                btn.pack_forget()
            enrollment_expanded.set(False)
        else:
            for btn in enrollment_buttons:
                btn.pack(fill='x', pady=2, padx=20)
            enrollment_expanded.set(True)

    enrollment_expanded = tk.BooleanVar(value=False)

    enrollment_frame = tk.Frame(nav_frame, bg='#770000', highlightbackground='#9f0000', highlightthickness=1)
    enrollment_frame.pack(fill='x', pady=5, padx=10)

    # Add icon to Enrollment button
    enrollment_menubutton = tk.Button(enrollment_frame, text="Enrollment", image=enrollment_icon, **btn_style, command=toggle_enrollment_dropdown)
    enrollment_menubutton.pack(fill='x', pady=5, padx=10)

    enrollment_buttons = [
        tk.Button(enrollment_frame, text="Enrollment History", command=show_table_panel, **dropdown_btn_style),
        tk.Button(enrollment_frame, text="Enrolled Students", command=show_studentmasterlist_panel, **dropdown_btn_style),
    ]

    # Spacer to push the Logout button to the bottom
    spacer = tk.Frame(nav_frame, bg="#9f0000")  # Invisible spacer
    spacer.pack(expand=True, fill="both")  # Takes up remaining space to push Logout down

    # Add icon to Logout button
    logout_button = tk.Button(nav_frame, text="Logout", image=logout_icon, command=logout, **btn_style)
    logout_button.pack(fill='x', pady=10, padx=10)  # Logout placed last, below spacer
    logout_button.bind("<Enter>", on_enter)
    logout_button.bind("<Leave>", on_leave)

    # Adjust navigation panel aesthetics
    nav_frame.config(bg="#9f0000", width=500)

#=======================================================DASHBOARD===============================================
    # Set uniform card size (keep original values)
    BOX_WIDTH = 220
    BOX_HEIGHT = 110

    # Function to load icons (keep original)
    def load_icon(path, size=(50, 50)):
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    # Load Icons (keep original)
    student_icon = load_icon("images/total.png")
    updates_icon = load_icon("images/help.png")
    admission_icon = load_icon("images/new.png")
    nursery_junior_icon = load_icon("images/junior.png")
    nursery_senior_icon = load_icon("images/senior.png")
    kindergarten_icon = load_icon("images/kinder.png")
    grade1_icon = load_icon("images/g1.png")
    grade2_icon = load_icon("images/2.png")
    grade3_icon = load_icon("images/3.png")
    grade4_icon = load_icon("images/4.png")
    grade5_icon = load_icon("images/5.png")
    grade6_icon = load_icon("images/6.png")

    # Function to create a card (keep original)
    def create_card(parent, text, icon, count="0"):
        frame = tk.Frame(parent, bg="#2980b9", width=BOX_WIDTH, height=BOX_HEIGHT, bd=3, relief="ridge")
        frame.pack(side="left", padx=15, pady=10)
        frame.pack_propagate(False)

        # Grid layout for alignment
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Count Label (Large number on top)
        count_label = tk.Label(frame, text=count, font=("Arial", 24, "bold"), bg="#2980b9", fg="white")
        count_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        # Text Label (Below the number)
        text_label = tk.Label(frame, text=text, font=("Arial", 16, "bold"), bg="#2980b9", fg="white")
        text_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 10))

        # Icon Label (Right Side, bigger size)
        icon_label = tk.Label(frame, image=icon, bg="#2980b9")
        icon_label.image = icon  # Keep reference
        icon_label.grid(row=0, column=1, rowspan=2, sticky="e", padx=10, pady=10)

        return count_label

    def update_student_count():
        cursor.execute("SELECT COUNT(*) FROM studentinfo")
        total_count = cursor.fetchone()[0]
       
        grade_counts = {}
        for grade in ["Junior Nursery", "Senior Nursery", "Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"]:
            cursor.execute("SELECT COUNT(*) FROM studentinfo WHERE grade_level = %s", (grade,))
            grade_counts[grade] = cursor.fetchone()[0]
        
        nursery_junior_label.config(text=f"{grade_counts['Junior Nursery']}")
        nursery_senior_label.config(text=f"{grade_counts['Senior Nursery']}")
        kindergarten_label.config(text=f"{grade_counts['Kindergarten']}")
        grade1_label.config(text=f"{grade_counts['Grade 1']}")
        grade2_label.config(text=f"{grade_counts['Grade 2']}")
        grade3_label.config(text=f"{grade_counts['Grade 3']}")
        grade4_label.config(text=f"{grade_counts['Grade 4']}")
        grade5_label.config(text=f"{grade_counts['Grade 5']}")
        grade6_label.config(text=f"{grade_counts['Grade 6']}")

    # MODIFIED BACKGROUND FUNCTION - Now responsive
    def set_background():
        global bg_image, bg_label
        
        try:
            # Load the image but don't resize yet
            bg_image_original = Image.open("images/canva.png")
            
            # Create label first
            bg_label = tk.Label(dashboard_frame, bg="#004aad")
            bg_label.place(relwidth=1, relheight=1)
            
            # Function to resize background on window change
            def resize_bg(event):
                try:
                    # Resize the original image to current window size
                    resized = bg_image_original.resize((event.width, event.height), Image.LANCZOS)
                    new_bg = ImageTk.PhotoImage(resized)
                    bg_label.config(image=new_bg)
                    bg_label.image = new_bg  # Keep reference
                except:
                    bg_label.config(bg="#004aad")
            
            # Bind the resize function
            dashboard_frame.bind("<Configure>", resize_bg)
            
            # Initial resize
            resize_bg(type('obj', (object,), {'width': dashboard_frame.winfo_width(), 
                                            'height': dashboard_frame.winfo_height()}))
        except:
            # Fallback if image fails to load
            dashboard_frame.config(bg="#004aad")

    # Dashboard Frame (keep original)
    dashboard_frame = tk.Frame(content_frame, bg="#004aad")
    dashboard_frame.grid(row=0, column=0, sticky="nsew")

    # Set background (now responsive)
    set_background()

    # Title Frame (keep original)
    title_frame = tk.Frame(dashboard_frame, bg="#0f1074", height=100)
    title_frame.pack(fill="x", side="top")
    title_frame.pack_propagate(False)

    # Dashboard Icon (keep original)
    icon_image = tk.PhotoImage(file="images/dash.png")
    icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
    icon_label.image = icon_image
    icon_label.pack(side="left", padx=10, pady=10)

    # Title Label (keep original)
    title_label = tk.Label(title_frame, text="Student Enrollment Dashboard", font=("Arial", 30, "bold"), bg="#0f1074", fg="#E8E4C9")
    title_label.pack(side="left", padx=10)

    # Card Frame (keep original)
    card_frame = tk.Frame(dashboard_frame, bg="#000A2E")
    card_frame.pack(pady=10)

    # Fetch counts from database (keep original)
    cursor.execute("SELECT COUNT(*) FROM studentinfo")
    total_students = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM updates")
    total_updates = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM admission")
    total_admission = cursor.fetchone()[0]

    # Admission Count Card (keep original)
    admission_label = create_card(card_frame, "New Admissions", admission_icon, count=str(total_admission))
    
    # Total Students Card (keep original)
    student_label = create_card(card_frame, "Total Students", student_icon, count=str(total_students))
    
    # Updates Count Card (keep original)
    updates_label = create_card(card_frame, "Request Updates", updates_icon, count=str(total_updates))

    # Nursery Section (keep original)
    nursery_frame = tk.Frame(dashboard_frame, bg="#000A2E")
    nursery_frame.pack(pady=0)

    nursery_junior_label = create_card(nursery_frame, "Junior Nursery", nursery_junior_icon)
    nursery_senior_label = create_card(nursery_frame, "Senior Nursery", nursery_senior_icon)
    kindergarten_label = create_card(nursery_frame, "Kindergarten", kindergarten_icon)

    # Grades 1-3 Section (keep original)
    grades_1_3_frame = tk.Frame(dashboard_frame, bg="#000A2E")
    grades_1_3_frame.pack(pady=10)

    grade1_label = create_card(grades_1_3_frame, "Grade 1", grade1_icon)
    grade2_label = create_card(grades_1_3_frame, "Grade 2", grade2_icon)
    grade3_label = create_card(grades_1_3_frame, "Grade 3", grade3_icon)

    # Grades 4-6 Section (keep original)
    grades_4_6_frame = tk.Frame(dashboard_frame, bg="#000A2E")
    grades_4_6_frame.pack(pady=10)

    grade4_label = create_card(grades_4_6_frame, "Grade 4", grade4_icon)
    grade5_label = create_card(grades_4_6_frame, "Grade 5", grade5_icon)
    grade6_label = create_card(grades_4_6_frame, "Grade 6", grade6_icon)
    
    # Update student count (keep original)
    update_student_count()

#=======================================================TABLE PANEL===============================================
    def on_year_selected(event):
        """Load data for the selected school year from the Combobox."""
        selected_year = year_combobox.get()
        if selected_year and "-" in selected_year:
            load_data(selected_year)  # Pass the selected school year range
        else:
            load_data()  # Load all data if no valid school year is selected

    def search_records(search_text):
        """Filters Treeview based on search text"""
        for row in tree_table.get_children():
            tree_table.delete(row)  # Clear current rows

        selected_year = year_combobox.get()
        
        query = """
            SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
            father_age, father_email, father_occupation, father_contact, father_company, 
            mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
            parents_status, date_enrolled, year, special_needs  
            FROM student_history 
            WHERE (student_id LIKE %s OR LRN LIKE %s OR last_name LIKE %s OR first_name LIKE %s OR nickname LIKE %s)
        """
        
        params = tuple(f"%{search_text}%" for _ in range(5))  # Wildcards for partial match
        
        if selected_year and "-" in selected_year:
            start_year, end_year = map(int, selected_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
            query += " AND date_enrolled BETWEEN %s AND %s"
            params += (start_date, end_date)
        
        cursor.execute(query, params)
        fetched_data = cursor.fetchall()
        
        for row in fetched_data:
            table_insert_student_data(row)


    def table_insert_student_data(row):
        """Insert row data into the Treeview, allowing duplicate student IDs."""
        try:
            current_row_index = len(tree_table.get_children())
            tag = "evenrow" if current_row_index % 2 == 0 else "oddrow"

            # Insert row without enforcing a unique ID
            tree_table.insert("", "end", values=row, tags=(tag,))
            
        except Exception as e:
            print(f"An error occurred: {e}") 

            
    def table_select_junior_nursery():
        for row in tree_table.get_children():
            tree_table.delete(row)

        selected_year = year_combobox.get()
        if selected_year and "-" in selected_year:
            start_year, end_year = map(int, selected_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
            
            cursor.execute("""
                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history 
                WHERE grade_level = 'Junior Nursery' 
                AND date_enrolled BETWEEN %s AND %s
            """, (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM student_history WHERE grade_level = 'Junior Nursery'")

        fetched_data = cursor.fetchall()
        for row in fetched_data:
            table_insert_student_data(row)

    def table_select_senior_nursery():
        for row in tree_table.get_children():
            tree_table.delete(row)

        selected_year = year_combobox.get()
        if selected_year and "-" in selected_year:
            start_year, end_year = map(int, selected_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
            
            cursor.execute("""
                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history 
                WHERE grade_level = 'Senior Nursery' 
                AND date_enrolled BETWEEN %s AND %s
            """, (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM student_history WHERE grade_level = 'Senior Nursery'")

        fetched_data = cursor.fetchall()
        for row in fetched_data:
            table_insert_student_data(row)


    def table_select_kindergarten():
        for row in tree_table.get_children():
            tree_table.delete(row)

        selected_year = year_combobox.get()
        if selected_year and "-" in selected_year:
            start_year, end_year = map(int, selected_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
            
            cursor.execute("""
                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history 
                WHERE grade_level = 'Kindergarten' 
                AND date_enrolled BETWEEN %s AND %s
            """, (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM student_history WHERE grade_level = 'Kindergarten'")

        fetched_data = cursor.fetchall()
        for row in fetched_data:
            table_insert_student_data(row)


    def table_select_grade_1():
        for row in tree_table.get_children():
            tree_table.delete(row)

        selected_year = year_combobox.get()
        if selected_year and "-" in selected_year:
            start_year, end_year = map(int, selected_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
            
            cursor.execute("""
                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history 
                WHERE grade_level = 'Grade 1' 
                AND date_enrolled BETWEEN %s AND %s
            """, (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM student_history WHERE grade_level = 'Grade 1'")

        fetched_data = cursor.fetchall()
        for row in fetched_data:
            table_insert_student_data(row)

    def table_select_grade_2():
        for row in tree_table.get_children():
            tree_table.delete(row)

        selected_year = year_combobox.get()
        if selected_year and "-" in selected_year:
            start_year, end_year = map(int, selected_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
            
            cursor.execute("""
                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history 
                WHERE grade_level = 'Grade 2' 
                AND date_enrolled BETWEEN %s AND %s
            """, (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM student_history WHERE grade_level = 'Grade 2'")

        fetched_data = cursor.fetchall()
        for row in fetched_data:
            table_insert_student_data(row)

    def table_select_grade_3():
        for row in tree_table.get_children():
            tree_table.delete(row)

        selected_year = year_combobox.get()
        if selected_year and "-" in selected_year:
            start_year, end_year = map(int, selected_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
            
            cursor.execute("""
                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history 
                WHERE grade_level = 'Grade 3' 
                AND date_enrolled BETWEEN %s AND %s
            """, (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM student_history WHERE grade_level = 'Grade 3'")

        fetched_data = cursor.fetchall()
        for row in fetched_data:
            table_insert_student_data(row)

    def table_select_grade_4():
        for row in tree_table.get_children():
            tree_table.delete(row)

        selected_year = year_combobox.get()
        if selected_year and "-" in selected_year:
            start_year, end_year = map(int, selected_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
            
            cursor.execute("""
                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history 
                WHERE grade_level = 'Grade 4' 
                AND date_enrolled BETWEEN %s AND %s
            """, (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM student_history WHERE grade_level = 'Grade 4'")

        fetched_data = cursor.fetchall()
        for row in fetched_data:
            table_insert_student_data(row)


    def table_select_grade_5():
        for row in tree_table.get_children():
            tree_table.delete(row)

        selected_year = year_combobox.get()
        if selected_year and "-" in selected_year:
            start_year, end_year = map(int, selected_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
            
            cursor.execute("""
                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history 
                WHERE grade_level = 'Grade 5' 
                AND date_enrolled BETWEEN %s AND %s
            """, (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM student_history WHERE grade_level = 'Grade 5'")

        fetched_data = cursor.fetchall()
        for row in fetched_data:
            table_insert_student_data(row)


    def table_select_grade_6():
        for row in tree_table.get_children():
            tree_table.delete(row)

        selected_year = year_combobox.get()
        if selected_year and "-" in selected_year:
            start_year, end_year = map(int, selected_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
            
            cursor.execute("""
                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history  FROM student_history 
                WHERE grade_level = 'Grade 6' 
                AND date_enrolled BETWEEN %s AND %s
            """, (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM student_history WHERE grade_level = 'Grade 6'")

        fetched_data = cursor.fetchall()
        for row in fetched_data:
            table_insert_student_data(row)


            # Selection for active and inactive students
    def table_select_active():
                for row in tree_table.get_children():
                    tree_table.delete(row)

                cursor.execute("""SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history 
                                FROM student_history WHERE student_status = 'Active'""")
                full_data.clear()
                for row in cursor.fetchall():
                    full_data.append(row)
    
    def table_select_inactive():
                for row in tree_table.get_children():
                    tree_table.delete(row)

                cursor.execute("""SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs  FROM student_history 
                                FROM student_history WHERE student_status = 'Inactive'""")
                full_data.clear()
                for row in cursor.fetchall():
                    full_data.append(row)
    # Table Frame
    table_frame = tk.Frame(content_frame, bg="#ecf0f1")
    table_frame.grid(row=0, column=0, sticky="nsew")

    # Title Frame
    title_frame = tk.Frame(table_frame, bg="#0f1074", height=100)
    title_frame.pack(fill="x")
    title_frame.pack_propagate(False)

    icon_image = tk.PhotoImage(file="images/elearning.png")
    icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
    icon_label.image = icon_image
    icon_label.pack(side="left", padx=10)

    title_label = tk.Label(
        title_frame, text="Student Records", font=("Arial", 30, "bold"), bg="#0f1074", fg="#E8E4C9"
    )
    title_label.pack(side="left", padx=10)

    # Search & Filter Frame
    search_frame = tk.Frame(table_frame, bg="#ecf0f1")
    search_frame.pack(fill="x", pady=5)

    tk.Label(search_frame, text="Search:", font=('Arial', 12), bg="#ecf0f1").pack(side='left', padx=5)
    search_entry = tk.Entry(search_frame, font=('Arial', 12), width=20)
    search_entry.pack(side='left', padx=5)

    tk.Button(search_frame, text="Search", font=('Arial', 12), bg="#0f1074", fg="white", command=lambda: search_records(search_entry.get())).pack(side='left', padx=5)

    tk.Label(search_frame, text="Filter by Year:", font=('Arial', 12), bg="#ecf0f1").pack(side='left', padx=5)

    years = [f"{y}-{y+1}" for y in range(2020, 2031)]
    year_combobox = ttk.Combobox(search_frame, values=years, font=('Arial', 12), state='readonly')
    year_combobox.pack(side='left', padx=5)

    year_combobox.bind("<<ComboboxSelected>>", on_year_selected)

        # Filter Frame (Contains Grade Levels and Status on the same row)
    filter_frame = tk.Frame(table_frame, bg="#ecf0f1")
    filter_frame.pack(fill="x", pady=5)

    # Grade Level Frame
    grade_level_frame = tk.Frame(filter_frame, bg="#ecf0f1")
    grade_level_frame.pack(side="left", padx=10, pady=5)

    tk.Label(grade_level_frame, text="Grade Levels:", font=('Arial', 14, 'bold'), 
            bg="#ecf0f1", fg="#34495e").pack(side="left", padx=5)  # Label next to buttons

    grade_buttons = [
        ("JN", table_select_junior_nursery, "#ff5733"),  
        ("SN", table_select_senior_nursery, "#ff8c1a"),  
        ("K", table_select_kindergarten, "#f4c542"),  
        ("G1", table_select_grade_1, "#3cb371"),  
        ("G2", table_select_grade_2, "#3498db"),  
        ("G3", table_select_grade_3, "#8e44ad"),  
        ("G4", table_select_grade_4, "#2c3e50"),  
        ("G5", table_select_grade_5, "#e74c3c"),  
        ("G6", table_select_grade_6, "#27ae60"),  
        ("All", load_data, "#34495e"),  
    ]

    for grade, command, color in grade_buttons:
        tk.Button(grade_level_frame, text=grade, font=('Arial', 8, 'bold'), bg=color, fg="white",
                width=6, command=command).pack(side="left", padx=3)

    # Status Frame
    status_frame = tk.Frame(filter_frame, bg="#ecf0f1")
    status_frame.pack(side="left", padx=10, pady=5)

    tk.Label(status_frame, text="Status:", font=('Arial', 14, 'bold'), 
            bg="#ecf0f1", fg="#34495e").pack(side="left", padx=5)  # Label next to buttons

    tk.Button(status_frame, text="Active", command=table_select_active, font=('Arial', 12), 
            bg="#2ecc71", fg="white", width=10).pack(side="left", padx=5)

    tk.Button(status_frame, text="Inactive", command=table_select_inactive, font=('Arial', 12), 
            bg="#e74c3c", fg="white", width=10).pack(side="left", padx=5)

    # Treeview Table with Scrollbars
    tree_frame = tk.Frame(table_frame)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

    tree_columns = ("Student ID", "LRN", "Last Name", "First Name", "Nickname", 
                    "Grade Level", "Age", "Gender", "Birthday", "Address", 
                    "Father", "Father's Age", "Father's Email", "Father's Occupation", "Father's Contact", "Father's Company",
                    "Mother", "Mother's Age", "Mother's Email", "Mother's Occupation", "Mother's Contact", "Mother's Company",
                    "Parent Status", "Date Enrolled", "Year", "Special Needs")

    # Create Treeview
    tree_table = ttk.Treeview(tree_frame, columns=tree_columns, show="headings", height=7)
    tree_table.grid(row=0, column=0, sticky="nsew")

    # Vertical and Horizontal Scrollbars
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_table.yview)
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree_table.xview)

    tree_table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    # Make sure tree_frame expands correctly
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    # Set column headings
    for col in tree_columns:
        tree_table.heading(col, text=col)
        tree_table.column(col, width=120, anchor='center')


        # Configure row colors
    tree_table.tag_configure("evenrow", background="#ffbb00")  
    tree_table.tag_configure("oddrow", background="#F5F5DC")   

    
#==================================================== STUDENT MASTERLIST PANEL =====================================
    def search_studentml_students():
        search_query = search_entry.get().lower().strip()  # Trim whitespace and convert to lower case
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)  # Clear existing entries

        # If the search entry is empty, load all students
        if not search_query:
            load_studentml_data()  # Fetch and show all records if search query is empty
            return

        try:
            # Fetch matching results using the LIKE clause
            cursor.execute("""
                SELECT * FROM studentinfo 
                WHERE LOWER(last_name) LIKE %s 
                OR LOWER(first_name) LIKE %s 
                OR LOWER(nickname) LIKE %s
            """, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))

            results = cursor.fetchall()  # Retrieve the results

            # Check if results are found
            if results:
                for row in results:
                    insert_student_data(row)  # Use insert function to populate the tree
            else:
                messagebox.showinfo("No Results", "No students found matching your search.")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error executing search: {err}")

    def insert_student_data(row):
        """Insert row data into the student masterlist treeview, ensuring unique iids."""
        try:

            student_id = row[0]  
            unique_iid = f"{student_id}-{row[1]}" 
            if not tree_studentml.exists(unique_iid):
                current_row_index = len(tree_studentml.get_children())
                tag = "evenrow" if current_row_index % 2 == 0 else "oddrow"
                tree_studentml.insert("", "end", iid=unique_iid, values=row, tags=(tag,))
            else:
                print(f"Warning: Duplicate ID found in data: {student_id}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def select_junior_nursery():
        tree_studentml.current_grade = 'Junior Nursery'
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)
        
        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE grade_level = 'Junior Nursery' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row)  

        update_year_label(f"{start_year}-{end_year}")

    def select_senior_nursery():
        tree_studentml.current_grade = 'Senior Nursery'
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)
        
        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE grade_level = 'Senior Nursery' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row) 

        update_year_label(f"{start_year}-{end_year}")

    def select_kindergarten():
        tree_studentml.current_grade = 'Kindergarten'
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)
        
        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE grade_level = 'Kindergarten' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row) 

        update_year_label(f"{start_year}-{end_year}") 

    def select_grade_1():
        tree_studentml.current_grade = 'Grade 1'
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)
        
        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE grade_level = 'Grade 1' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row)  # Use insert function for striped rows

        update_year_label(f"{start_year}-{end_year}")
                
    def select_grade_2():
        tree_studentml.current_grade = 'Grade 2'
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)
        
        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE grade_level = 'Grade 2' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row)  # Use insert function for striped rows

        update_year_label(f"{start_year}-{end_year}")

    def select_grade_3():
        tree_studentml.current_grade = 'Grade 3'
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)
        
        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE grade_level = 'Grade 3' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row)  # Use insert function for striped rows

        update_year_label(f"{start_year}-{end_year}")

    def select_grade_4():
        tree_studentml.current_grade = 'Grade 4'
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)
        
        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE grade_level = 'Grade 4' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row)  # Use insert function for striped rows

        update_year_label(f"{start_year}-{end_year}")

    def select_grade_5():
        tree_studentml.current_grade = 'Grade 5'
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)
        
        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE grade_level = 'Grade 5' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row)  # Use insert function for striped rows

        update_year_label(f"{start_year}-{end_year}")

    def select_grade_6():
        tree_studentml.current_grade = 'Grade 6'
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)
        
        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE grade_level = 'Grade 6' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row)  # Use insert function for striped rows

        update_year_label(f"{start_year}-{end_year}")

    def select_active():
        tree_studentml.current_filter = 'active'
        tree_studentml.current_grade = None
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)

        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE student_status = 'Active' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row)  

    def select_inactive():
        tree_studentml.current_filter = 'inactive'
        tree_studentml.current_grade = None
        for row in tree_studentml.get_children():
            tree_studentml.delete(row)

        cursor.execute("""
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture
            FROM studentinfo WHERE student_status = 'Inactive' AND year BETWEEN %s AND %s 
            """, (start_year, end_year))
        full_data.clear()
        for row in cursor.fetchall():
            full_data.append(row)
            insert_student_data(row)  
            
    def create_studentml_view():
        global studentml_frame, tree_studentml, year_label, start_year, end_year
        global full_data, finance_data, special_needs_data
        full_data = [] 
        finance_data = []
        special_needs_data = []

        studentml_frame = tk.Frame(content_frame, bg="#ecf0f1")
        studentml_frame.grid(row=0, column=0, sticky="nsew")

        # Title Frame
        title_frame = tk.Frame(studentml_frame, bg="#0f1074", height=100)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        icon_image = tk.PhotoImage(file="images/master.png")
        icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
        icon_label.image = icon_image  
        icon_label.pack(side="left", padx=10, pady=10)

        title_label = tk.Label(title_frame, text="Student Masterlist",
                            font=("Arial", 30, "bold"), bg="#0f1074", fg="#E8E4C9")
        title_label.pack(side="left", padx=10)

        # Year Label
        current_year = datetime.now().year
        current_month = datetime.now().month
        start_year = current_year if current_month >= 6 else current_year - 1
        end_year = start_year + 1
        academic_year = f"{start_year}-{end_year}"

        year_label = tk.Label(studentml_frame, text=f"YEAR: {academic_year}",
                            font=('Arial', 14, 'bold'), bg="#ecf0f1", fg="#34495e")
        year_label.pack(pady=5)

        # Control Frame
        control_frame = tk.Frame(studentml_frame, bg="#ecf0f1")
        control_frame.pack(fill="x", pady=5)

        tk.Label(control_frame, text="Search:", font=('Arial', 12, 'bold'), bg="#ecf0f1", fg="#34495e").pack(side='left', padx=5)
        
        search_entry = tk.Entry(control_frame, font=('Arial', 12), fg="#34495e", width=20)
        search_entry.pack(side='left', padx=3)

        search_button = tk.Button(control_frame, text="Search", command=search_studentml_students,
                                font=('Arial', 10), bg="#0a49a7", fg="white", width=10)
        search_button.pack(side='left', padx=3)

        refresh_button = tk.Button(control_frame, text="Refresh", command=load_studentml_data,
                                font=('Arial', 10), bg="#3498db", fg="white", width=10)
        refresh_button.pack(side='left', padx=3)

        print_button = tk.Button(control_frame, text="Print List", command=print_studentml_data,
                                font=('Arial', 10), bg="#9b59b6", fg="white", width=10)
        print_button.pack(side="left", padx=3)

        prev_year_button = tk.Button(control_frame, text="View Prev Year", command=load_previous_year_students,
                                    font=("Arial", 10), fg="white", bg="#e67e22",
                                    padx=5, pady=3, relief="raised", bd=2, width=14)
        prev_year_button.pack(side='left', padx=3, pady=3)

                        
        # Levels & Status Frame (Container for Grade Levels, Nursery Levels, and Status)
        levels_status_frame = tk.Frame(studentml_frame, bg="#ecf0f1")
        levels_status_frame.pack(fill="x", pady=5)

        # Grade Level Frame
        grade_level_frame = tk.Frame(levels_status_frame, bg="#ecf0f1")
        grade_level_frame.pack(side="left", padx=10, pady=5)

        tk.Label(grade_level_frame, text="Grade Levels:", font=('Arial', 12, 'bold'), 
                bg="#ecf0f1", fg="#34495e").pack(side="left", padx=5)  # Label next to buttons

        grade_buttons = [
            ("G1", select_grade_1, "#3cb371"),
            ("G2", select_grade_2, "#3498db"),
            ("G3", select_grade_3, "#8e44ad"),
            ("G4", select_grade_4, "#2c3e50"),
            ("G5", select_grade_5, "#e74c3c"),
            ("G6", select_grade_6, "#27ae60"),
            ("All", load_studentml_data, "#34495e"),
        ]

        for grade, command, color in grade_buttons:
            tk.Button(grade_level_frame, text=grade, font=('Arial', 8, 'bold'), bg=color, fg="white",
                    width=5, command=command).pack(side="left", padx=2)

        # Nursery Level Frame
        nursery_level_frame = tk.Frame(levels_status_frame, bg="#ecf0f1")
        nursery_level_frame.pack(side="left", padx=10, pady=5)

        tk.Label(nursery_level_frame, text="Nursery Levels:", font=('Arial', 12, 'bold'), 
                bg="#ecf0f1", fg="#34495e").pack(side="left", padx=5)  # Label next to buttons

        nursery_buttons = [
            ("JN", select_junior_nursery, "#ff5733"),
            ("SN", select_senior_nursery, "#ff8c1a"),
            ("K", select_kindergarten, "#f4c542"),
        ]

        for nursery, command, color in nursery_buttons:
            tk.Button(nursery_level_frame, text=nursery, font=('Arial', 8, 'bold'), bg=color, fg="white",
                    width=5, command=command).pack(side="left", padx=2)

        # Status Frame
        status_frame = tk.Frame(levels_status_frame, bg="#ecf0f1")
        status_frame.pack(side="left", padx=10, pady=5)

        tk.Label(status_frame, text="Status:", font=('Arial', 12, 'bold'), 
                bg="#ecf0f1", fg="#34495e").pack(side="left", padx=5)  # Label next to buttons

        active_button = tk.Button(status_frame, text="Active", command=select_active,
                                font=('Arial', 10), bg="#2ecc71", fg="white", width=10)
        active_button.pack(side='left', padx=3)

        inactive_button = tk.Button(status_frame, text="Inactive", command=select_inactive,
                                    font=('Arial', 10), bg="#e74c3c", fg="white", width=10)
        inactive_button.pack(side='left', padx=3)


        # Treeview Frame
        tree_frame = tk.Frame(studentml_frame, bg="#ecf0f1")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        studentml_tree_columns = ("Student ID", "LRN", "Last Name", "First Name", "Nickname",
                                "Grade Level", "Age", "Gender", "Birthday", "Address")

        tree_studentml = ttk.Treeview(tree_frame, columns=studentml_tree_columns, show="headings", height=15)

        for col in studentml_tree_columns:
            tree_studentml.heading(col, text=col)
            tree_studentml.column(col, anchor='center', width=120)

        tree_studentml.bind("<Double-1>", on_row_double_click)

        # Treeview Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_studentml.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree_studentml.xview)
        tree_studentml.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree_studentml.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        tree_studentml.tag_configure("oddrow", background="#ffbb00")  # Light gray
        tree_studentml.tag_configure("evenrow", background="#F5F5DC")  # White


    def print_studentml_data():
        """Export student data to PDF with school logo and colored indicators"""
        try:
            # Get current academic year
            academic_year = year_label.cget('text').replace('YEAR: ', '')
            
            # Determine current filter from the treeview
            current_filter = getattr(tree_studentml, 'current_filter', None)
            current_grade = getattr(tree_studentml, 'current_grade', None)
            
            # Prepare base query with specified columns
            base_query = """
                SELECT
                    student_id, LRN, last_name, first_name, nickname, 
                    grade_level, age, gender, birthday, date_enrolled,
                    student_status
                FROM studentinfo
                WHERE year BETWEEN %s AND %s
            """
            
            # Add filters based on current view
            params = [start_year, end_year]
            if current_grade:
                base_query += " AND grade_level = %s"
                params.append(current_grade)
            elif current_filter == 'active':
                base_query += " AND student_status = 'Active'"
            elif current_filter == 'inactive':
                base_query += " AND student_status = 'Inactive'"
            
            base_query += " ORDER BY grade_level, last_name, first_name"
            
            # Execute query with parameters
            cursor.execute(base_query, tuple(params))
            students = cursor.fetchall()
            
            if not students:
                messagebox.showinfo("No Data", "No student data to export")
                return

            # Ask user for save location
            save_path = filedialog.asksaveasfilename(
                title="Save Student Data As PDF",
                initialfile=f"Student_List_{current_grade if current_grade else current_filter if current_filter else 'All'}_{academic_year.replace('/', '-')}",
                defaultextension='.pdf',
                filetypes=[('PDF Files', '*.pdf')]
            )
            
            if not save_path:  # User cancelled
                return

            # Create PDF (landscape A4)
            pdf = FPDF(orientation='L', unit='mm', format='A4')
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # Add school logo (adjust path and position as needed)
            try:
                logo_path = "images/hiho.png"  # Update with your actual logo path
                pdf.image(logo_path, x=10, y=8, w=20)  # Position at top left
            except:
                pass  # Skip if logo not found
            
            # Title with filter indicator
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "STUDENT MASTERLIST", 0, 1, 'C')
            
            # Add colored filter indicator
            pdf.set_font("Arial", 'B', 14)
            if current_grade:
                pdf.set_text_color(0, 100, 0)  # Dark green for grade level
                pdf.cell(0, 10, f"{current_grade} Students", 0, 1, 'C')
            elif current_filter:
                if current_filter == 'active':
                    pdf.set_text_color(0, 100, 0)  # Dark green for active
                else:
                    pdf.set_text_color(200, 0, 0)  # Red for inactive
                pdf.cell(0, 10, f"{current_filter.title()} Students Only", 0, 1, 'C')
            else:
                pdf.set_text_color(0, 0, 0)  # Black for all students
                pdf.cell(0, 10, "All Students", 0, 1, 'C')
            pdf.set_text_color(0, 0, 0)  # Reset to black
            
            # Academic year and date
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, f"Academic Year: {academic_year}", 0, 1, 'C')
            pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C')
            pdf.ln(10)

            # Prepare headers
            headers = [
                "ID", "LRN", "Last Name", "First Name", "Nickname", 
                "Grade Level", "Age", "Gender", "Birthday", "Enrolled", "Status"
            ]

            # Calculate column widths (total width = 297mm - 20mm margins = 277mm)
            total_width = 277
            weights = [1, 2, 3, 3, 1.5, 2, 1, 1.5, 2, 2, 1.5]
            col_widths = [total_width * (w/sum(weights)) for w in weights]
            
            # Header row
            pdf.set_font("Arial", 'B', 9)
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, header, border=1, align='C')
            pdf.ln()
            
            # Data rows with colored status
            pdf.set_font("Arial", size=8)
            for student in students:
                for i in range(len(headers)-1):  # Regular columns
                    value = str(student[i]) if student[i] is not None else ""
                    
                    # Format dates
                    if headers[i] in ["Birthday", "Enrolled"] and value:
                        try:
                            value = datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
                        except:
                            pass
                    
                    # Special coloring for grade level column
                    if headers[i] == "Grade Level":
                        pdf.set_text_color(0, 100, 0)  # Dark green for grade level
                    else:
                        pdf.set_text_color(0, 0, 0)  # Black for other columns
                    
                    # Adjust text length
                    max_chars = int(col_widths[i]/2)
                    display_value = (value[:max_chars] + '..') if len(value) > max_chars else value
                    pdf.cell(col_widths[i], 8, display_value, border=1)
                
                # Status column with color coding
                status = student[10] if len(student) > 10 else ""
                if status and status.lower() == 'active':
                    pdf.set_text_color(0, 100, 0)  # Dark green for active
                    pdf.set_fill_color(230, 255, 230)  # Light green background
                else:
                    pdf.set_text_color(200, 0, 0)  # Red for inactive
                    pdf.set_fill_color(255, 230, 230)  # Light red background
                
                pdf.cell(col_widths[-1], 8, status if status else "", border=1, align='C', fill=True)
                pdf.set_text_color(0, 0, 0)  # Reset to black
                pdf.set_fill_color(255, 255, 255)  # Reset background
                pdf.ln()
            
            # Save PDF
            pdf.output(save_path)
            messagebox.showinfo("Export Successful", 
                            f"Student data successfully saved to:\n{save_path}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")



#=====================================================LOAD DATA ON TABLE===========================================        
    create_studentml_view()
    add_top_right_label(dashboard_frame)
    add_top_right_label(table_frame)
    add_top_right_label(studentml_frame)

    show_dashboard_panel()
    def auto_refresh():
        ensure_connection()
        if dashboard_frame.winfo_viewable():
            update_student_count()
        elif table_frame.winfo_viewable():
            load_data()
        elif studentml_frame.winfo_viewable():
            load_studentml_data()
        main_root.after(5000, auto_refresh)

    auto_refresh()
    main_root.mainloop()

    

