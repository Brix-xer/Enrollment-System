import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Label, Canvas, Frame, Button, RIGHT, Y, LEFT, X, GROOVE, BOTH
from tkinter import messagebox
from tkinter import font as tkFont
from fpdf import FPDF
import tempfile
import mysql.connector
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
import sys
import tkinter.simpledialog as simpledialog
import random, string 
from tkinter import font
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import PhotoImage
import ctypes  
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
#===============================================================INSERT DATA===================================

    def clear_input_fields():
        last_name_entry.delete(0, tk.END)
        first_name_entry.delete(0, tk.END)
        nickname_entry.delete(0, tk.END)
        enrollment_grade_combo.set("")
        age_entry.delete(0, tk.END)
        gender_entry.delete(0, tk.END)
        birthday_entry.set_date(datetime.now())  # Reset to current date
        address_text.delete("1.0", tk.END)
        father_name_entry.delete(0, tk.END)
        father_age_entry.delete(0, tk.END)
        father_email_entry.delete(0, tk.END)
        father_occupation_entry.delete(0, tk.END)
        father_contact_entry.delete(0, tk.END)
        father_company_entry.delete(0, tk.END)
        mother_name_entry.delete(0, tk.END)
        mother_age_entry.delete(0, tk.END)
        mother_email_entry.delete(0, tk.END)
        mother_occupation_entry.delete(0, tk.END)
        mother_contact_entry.delete(0, tk.END)
        mother_company_entry.delete(0, tk.END)
        status_var.set("together")



    def insert_data():
        global enrollment_grade_combo  # Declare the variable as global

        try:
            # Retrieve data from input fields
            full_name = f"{last_name_entry.get()} {first_name_entry.get()}"
            lname = last_name_entry.get().strip()
            fname = first_name_entry.get().strip()
            nickname = nickname_entry.get().strip()
            gradelvl = enrollment_grade_combo.get().strip()
            age = int(age_entry.get().strip()) if age_entry.get().strip().isdigit() else None
            gender = gender_entry.get().strip()
            birthday = birthday_entry.get_date()  # Ensures it's in date format
            address = address_text.get("1.0", tk.END).strip()
            father_name = father_name_entry.get().strip()
            father_age = int(father_age_entry.get().strip()) if father_age_entry.get().strip().isdigit() else None
            father_email = father_email_entry.get().strip()
            father_occupation = father_occupation_entry.get().strip()
            father_contact = father_contact_entry.get().strip()
            father_company = father_company_entry.get().strip()
            mother_name = mother_name_entry.get().strip()
            mother_age = int(mother_age_entry.get().strip()) if mother_age_entry.get().strip().isdigit() else None
            mother_email = mother_email_entry.get().strip()
            mother_occupation = mother_occupation_entry.get().strip()
            mother_contact = mother_contact_entry.get().strip()
            mother_company = mother_company_entry.get().strip()
            parents_status = status_var.get()
            student_status = 'Active'


            # Get the current year and date
            current_year = datetime.now().year
            current_month = datetime.now().month
            date_enrolled = datetime.now().strftime('%Y-%m-%d')

            # Determine the school year
            school_year = current_year if current_month >= 6 else current_year - 1


            # Fetch or initialize the yearly counter
            cursor.execute("SELECT last_id FROM yearly_counter WHERE year = %s", (school_year,))
            result = cursor.fetchone()
            last_used_id = result[0] if result else 0
            new_student_id = last_used_id + 1

            # Update yearly counter
            cursor.execute("""
                INSERT INTO yearly_counter (year, last_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE last_id = %s
            """, (school_year, new_student_id, new_student_id))

            # Generate custom student_id
            custom_student_id = f"{school_year}-{new_student_id}"

            # Insert into studentinfo
            cursor.execute("""
                INSERT INTO studentinfo (
                    student_id, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                    father_age, father_email, father_occupation, father_contact, father_company, 
                    mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, parents_status, student_status, date_enrolled, year
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                custom_student_id, lname, fname, nickname, gradelvl, age, gender, birthday, address, father_name,
                father_age, father_email, father_occupation, father_contact, father_company,
                mother_name, mother_age, mother_email, mother_occupation, mother_contact, mother_company, parents_status, student_status, date_enrolled, school_year
            ))
            connection.commit()

                        # Insert into studentinfo
            cursor.execute("""
                INSERT INTO student_history (
                    student_id, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                    father_age, father_email, father_occupation, father_contact, father_company, 
                    mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, parents_status, student_status, date_enrolled, year
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                custom_student_id, lname, fname, nickname, gradelvl, age, gender, birthday, address, father_name,
                father_age, father_email, father_occupation, father_contact, father_company,
                mother_name, mother_age, mother_email, mother_occupation, mother_contact, mother_company, parents_status, student_status, date_enrolled, school_year
            ))
            connection.commit()

            cursor.execute("UPDATE logininfo SET info_no = %s WHERE info_no = %s", (custom_student_id, admitted_id_entry.get()))
            cursor.execute("UPDATE requirement_checklist SET id = %s WHERE id = %s", (custom_student_id, admitted_id_entry.get()))
            cursor.execute("UPDATE student_balance SET student_id = %s, grade_level = %s, date_enrolled = %s WHERE student_id = %s", 
                (custom_student_id, gradelvl, date_enrolled, admitted_id_entry.get()))


                        # **DELETE the student from admitted table**
            cursor.execute("DELETE FROM admitted WHERE Admission_ID = %s", (admitted_id_entry.get(),))

            connection.commit()


            load_data()
            load_studentml_data()
            messagebox.showinfo("Success", "Record inserted successfully.")
            clear_input_fields()


        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")



    def scheduling_insert_data():
        subject = subject_combo.get()
        time_from = f"{time_from_hour.get()}:{time_from_minute.get()} {time_from_period.get()}"
        time_to = f"{time_to_hour.get()}:{time_to_minute.get()} {time_to_period.get()}"
        day = get_selected_days()
        grade_level = grade_combo.get()
        section = section_combo.get()
        teacher = teacher_combo.get()

        if not all([subject, time_from, time_to, day, grade_level, section, teacher]):
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        time_range = f"{time_from} - {time_to}"
        sql = "INSERT INTO scheduling (Subject, Time, Day, Grade_level, Section, Teacher) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (subject, time_range, day, grade_level, section, teacher)
        try:
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            load_scheduling_data()  # Refresh the data
            messagebox.showinfo("Success", "Data inserted successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


    
    def submit_data(grade_level_combobox, section_combobox, adviser_entry, tree):
        
        grade_level = grade_level_combobox.get()
        section = section_combobox.get()
        adviser = adviser_entry.get()

        if not grade_level or not section or not adviser:
            messagebox.showerror("Input Error", "All fields are required")
            return

        try:
            query = ("INSERT INTO section (Grade_Level, Section, Adviser) "
                    "VALUES (%s, %s, %s)")
            cursor = connection.cursor()
            cursor.execute(query, (grade_level, section, adviser))
            connection.commit()
            cursor.close()  # Close cursor after query execution
            messagebox.showinfo("Success", "Data submitted successfully")
            # Refresh the data grid view
            section_display_data(tree)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Erroasdaesr", f"Error: {err}")

    def insert_subject():
            descriptive_title = subject_title_entry.get()
            subject_type = subject_type_combo.get()
            grade_level = subject_grade_combo.get()

            if descriptive_title and subject_type and grade_level:
                cursor.execute(
                    "INSERT INTO subject (Descriptive_Title, Type, Grade_Level) VALUES (%s, %s, %s)",
                    (descriptive_title, subject_type, grade_level)
                )
                cursor = connection.cursor()
                connection.commit()
                load_subject_data()  # Refresh the subject data
                subject_title_entry.delete(0, tk.END)
                subject_type_combo.set("")
                subject_grade_combo.set("")
                messagebox.showinfo("Success", "Subject added successfully")
            else:
                messagebox.showwarning("Input Error", "Please fill all fields")


    def add_teacher(id_no_entry, name_entry, address_entry, contact_entry, email_entry, picture_label, tree):
        id_no = id_no_entry.get()
        name = name_entry.get()
        address = address_entry.get()
        contact = contact_entry.get()
        email = email_entry.get()
        picture = picture_label.image_data if picture_label.image_data else None

        if id_no and name and address and contact and email:
            try:
                cursor.execute(
                    "INSERT INTO teacher (ID_NO, Name, Address, Contact, Email, Picture) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id_no, name, address, contact, email, picture)
                )
                connection.commit()

                # Clear the input fields
                id_no_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                address_entry.delete(0, tk.END)
                contact_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                picture_label.config(image='')
                picture_label.image_data = None

                # Reload the data in the Treeview
                load_teacher_data(tree)

                messagebox.showinfo("Success", "Teacher added successfully")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields and select a picture")


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

        # Insert rows with alternating colors
        for index, row in enumerate(cursor.fetchall()):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            tree_table.insert("", "end", values=row, tags=(tag,))

    def load_users():
        global cursor
        for row in user_table.get_children():
            user_table.delete(row)

        ensure_connection()  # Ensure database connection is active
        connection.commit()  # Force MySQL to refresh

        # Close old cursor safely before reassigning
        if cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error:
                pass  # Ignore if cursor is already closed

        cursor = connection.cursor(buffered=True)  # Create a new cursor
        
        cursor.execute("SELECT userid, username, permission FROM logininfo WHERE permission = 'admin' OR permission = 'registrar' OR permission = 'cashier' OR permission = 'interviewer' OR permission = 'teacher' ")
        for user in cursor.fetchall():
            user_table.insert("", "end", values=user)

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

        # Adjust school year to be from May of the current year to April of the next year
        if current_month >= 5:  
            start_year = current_year  # School year starts in May of this year
            end_year = current_year + 1  # Ends in April of the next year
        else:  
            start_year = current_year - 1  # If before May, last year's school year is still ongoing
            end_year = current_year  # Ends in April of this year

        # Clear the full_data list
        full_data.clear()

        # Define the SQL query dynamically for the May-to-April school year range
        query = """
            SELECT
                student_id, LRN, last_name, first_name, nickname, 
                grade_level, age, gender, birthday, address, father, 
                father_age, father_email, father_occupation, father_contact, father_company, 
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, student_status, year, profile_picture, date_enrolled
            FROM studentinfo
            WHERE student_status = 'Active' AND
                (
                    (MONTH(date_enrolled) >= 5 AND YEAR(date_enrolled) = %s)  -- May to December of the start year
                    OR 
                    (MONTH(date_enrolled) <= 4 AND YEAR(date_enrolled) = %s)  -- January to April of the end year
                );
        """

        cursor.execute(query, (start_year, end_year))

        student_info_rows = cursor.fetchall()

        for index, row in enumerate(student_info_rows):
            full_data.append(row)
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            tree_studentml.insert("", "end", values=row, tags=(tag,))

        update_year_label(f"{start_year}-{end_year}")

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

    def admitted_balance_data():
        finance_data.clear()
        query = """
            SELECT * FROM student_balance 
            WHERE student_id = %s 
        """

        cursor.execute(query, (admitted_selected_student[0],))
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
    def fetch_student_counts():
        """Fetch student count per grade level from the database."""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="hihodatabase"
            )
            cursor = connection.cursor()

            # Define grade levels
            grades = ["Junior Nursery", "Senior Nursery", "Kindergarten", 
                    "Grade 1", "Grade 2", "Grade 3", 
                    "Grade 4", "Grade 5", "Grade 6"]
            student_counts = []

            for grade in grades:
                cursor.execute("SELECT COUNT(*) FROM studentinfo WHERE grade_level = %s", (grade,))
                count = cursor.fetchone()[0]
                student_counts.append(count)

            cursor.close()
            connection.close()
            return grades, student_counts

        except mysql.connector.Error as err:
            return [], []

    def create_chart(parent_frame):
        """Embed a beautifully designed Matplotlib graph inside Tkinter."""
        grades, student_counts = fetch_student_counts()

        if not grades:  # If database fails, use placeholder data
            grades = ["Junior Nursery", "Senior Nursery", "Kindergarten", 
                    "Grade 1", "Grade 2", "Grade 3", 
                    "Grade 4", "Grade 5", "Grade 6"]
            student_counts = [5, 8, 10, 20, 18, 15, 12, 14, 10]

        fig, ax = plt.subplots(figsize=(9, 5))

        # Color Palette for bars
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#9b59b6", "#f1c40f", "#e67e22", "#1abc9c", "#34495e", "#95a5a6"]

        # Create bars with rounded edges and gradient
        bars = ax.bar(grades, student_counts, color=colors, edgecolor='black', linewidth=1.2)

        # Add shadows to bars for depth effect
        for bar in bars:
            bar.set_linewidth(1.5)
            bar.set_alpha(0.9)

        # Set Title and Labels with styling
        ax.set_title("Enrollment Count per Grade Level", fontsize=16, fontweight='bold', color="#2c3e50")
        ax.set_ylabel("Number of Students", fontsize=12, fontweight='bold', color="#34495e")
        ax.set_xlabel("Grade Levels", fontsize=12, fontweight='bold', color="#34495e")

        # Customize x-axis labels
        ax.set_xticks(range(len(grades)))
        ax.set_xticklabels(grades, rotation=45, ha="right", fontsize=10, color="#2c3e50")

         # Adjust margins to make labels more readable
        plt.subplots_adjust(bottom=0.2)  # Increased bottom margin

        # Add gridlines for clarity
        ax.yaxis.grid(True, linestyle="--", linewidth=0.7, alpha=0.6)

        # Add data labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 1, str(student_counts[i]),
                    ha='center', fontsize=11, fontweight='bold', color="#2c3e50")

        # Remove unnecessary spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Add background color for aesthetics
        ax.set_facecolor("#ecf0f1")
        fig.patch.set_facecolor("#ecf0f1")

        # Embed the chart into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
#======================================================================================================================================
    def load_admission_data():
        global tree_admission, cursor  # Ensure cursor is global

        for row in tree_admission.get_children():
            tree_admission.delete(row)
            
        ensure_connection()  # Ensure database connection is active
        connection.commit()  # Force MySQL to refresh

        try:
            # Close old cursor safely
            if cursor is not None:
                try:
                    cursor.close()
                except mysql.connector.Error:
                    pass  # Ignore if cursor is already closed

            cursor = connection.cursor(buffered=True)  # Create a new cursor

            cursor.execute("SELECT * FROM admission ORDER BY id DESC")
            fetched_rows = cursor.fetchall()

            for idx, row in enumerate(fetched_rows):
                student_id = row[0]
                unique_iid = f"{student_id}_{idx}"
                tree_admission.insert("", "end", iid=unique_iid, values=row)

                current_row_index = len(tree_admission.get_children())
                tag = "evenrow" if current_row_index % 2 == 0 else "oddrow"
                tree_admission.item(unique_iid, tags=(tag,))
            
            tree_admission.update_idletasks()  # Refresh the Treeview

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching admission data: {err}")



    def section_display_data(section_tree):
        try:    
            # Ensure connection is open
            cursor = connection.cursor()

            # Clear existing data in the Treeview
            for row in section_tree.get_children():
                section_tree.delete(row)

            # Fetch the data from the database
            cursor.execute("SELECT * FROM section")
            rows = cursor.fetchall()
            cursor.close()  # Close cursor after fetching data

            # Insert rows into the Treeview
            for row in rows:
                auto_id, grade_level, section, adviser = row
                section_tree.insert("", "end", iid=auto_id, values=(auto_id, grade_level, section, adviser))
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Function to select a picture
    def select_picture(picture_label):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            picture_label.config(image=photo)
            picture_label.image = photo

            # Save the image data to the picture_label.image_data attribute
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            picture_label.image_data = img_byte_arr.getvalue()


#===============SCHEDULING GET DATA===================================
    # Function to fetch subjects based on the selected grade level
    def get_subjects_by_grade_level(grade_level):
        if grade_level:
            with connection.cursor() as cursor:  # Use a context manager to ensure cursor is properly closed
                cursor.execute("SELECT Descriptive_Title FROM subject WHERE Grade_Level = %s", (grade_level,))
                return [s[0] for s in cursor.fetchall()]
        return []

    # Function to fetch grade levels from the 'subject' table
    def get_grade_levels():
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT Grade_Level FROM subject")
            return [s[0] for s in cursor.fetchall()]

    # Function to fetch sections from the 'section' table
    def get_sections():
        with connection.cursor() as cursor:
            cursor.execute("SELECT Section FROM section")
            return [s[0] for s in cursor.fetchall()]

    def get_grade_level_by_section(section):
        if section:
            with connection.cursor() as cursor:
                cursor.execute("SELECT Grade_Level FROM section WHERE Section = %s", (section,))
                result = cursor.fetchone()
                # Ensure any pending results are cleared
                cursor.fetchall()  # Fetch any remaining results to avoid "Unread result found" error
                return result[0] if result else None
        return None


    def get_adviser_by_section(section):
        if section:
            with connection.cursor() as cursor:
                cursor.execute("SELECT Adviser FROM section WHERE Section = %s", (section,))
                result = cursor.fetchone()
                # Ensure any pending results are cleared
                cursor.fetchall()  # Fetch any remaining results to avoid "Unread result found" error
                return result[0] if result else None
        return None


    # Function to fetch teachers from the 'teacher' table
    def get_teachers():
        with connection.cursor() as cursor:
            cursor.execute("SELECT Name FROM teacher")
            return [t[0] for t in cursor.fetchall()]

    def load_scheduling_data(grade_level=None):
        global cursor
        for item in scheduling_tree.get_children():
            scheduling_tree.delete(item)

        ensure_connection()  # Ensure database connection is active
        connection.commit()  # Force MySQL to refresh

        # Close old cursor safely before reassigning
        if cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error:
                pass  # Ignore if cursor is already closed

        cursor = connection.cursor(buffered=True)  # Create a new cursor

        with connection.cursor() as cursor:
            if grade_level:
                cursor.execute("SELECT * FROM scheduling WHERE Grade_level = %s", (grade_level,))
            else:
                cursor.execute("SELECT * FROM scheduling")

            rows = cursor.fetchall()

            for row in rows:
                scheduling_tree.insert("", "end", values=row)

    def refresh_data(event=None):
        grade_level = grade_combo.get()
        load_scheduling_data(grade_level)

    def load_teacher_data(tree):
        for item in tree.get_children():
            tree.delete(item)
        cursor.execute("SELECT ID, ID_NO, Name, Address, Contact, Email  FROM teacher")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)  

    def load_subject_data():
        for item in subject_tree.get_children():
            subject_tree.delete(item)

        cursor.execute("SELECT * FROM subject")
        rows = cursor.fetchall()

        for row in rows:
            subject_tree.insert("", tk.END, values=row)

#================================================PRINT CODE============================================
    def print_schedule():
        # Create a new print preview window
        print_window = tk.Toplevel()
        print_window.title("Print Preview")
        print_window.configure(bg="#ecf0f1")

        # Set initial size
        width = 600
        height = 600
        print_window.geometry(f"{width}x{height}")

        # Center the window
        print_window.update_idletasks()
        x = (print_window.winfo_screenwidth() // 2) - (print_window.winfo_width() // 2)
        y = (print_window.winfo_screenheight() // 2) - (print_window.winfo_height() // 2)
        print_window.geometry(f"{width}x{height}+{x}+{y}")

        # 🚀 Title Bar with Styling
        title_frame = tk.Frame(print_window, bg="#0f1074", height=80)
        title_frame.pack(fill="x", side="top")
        title_frame.pack_propagate(False)

        # Icon (Ensure 'print_icon.png' exists)
        icon_image = tk.PhotoImage(file="images/print_icon.png")  
        icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
        icon_label.image = icon_image  
        icon_label.pack(side="left", padx=10)

        # Title Label
        title_label = tk.Label(
            title_frame,
            text="Print Preview - Schedule",
            font=("Arial", 24, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10)

        # Main Content Frame
        print_frame = tk.Frame(print_window, bg="#ffffff", bd=2, relief="ridge", padx=20, pady=20)
        print_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Adviser and Section Info
        tk.Label(print_frame, text=f"Adviser: {adviser_entry.get()}", font=('Arial', 12), bg="#ffffff").pack(anchor='w')
        tk.Label(print_frame, text=f"Grade Level: {grade_combo.get()}", font=('Arial', 12), bg="#ffffff").pack(anchor='w')
        tk.Label(print_frame, text=f"Section: {section_combo.get()}", font=('Arial', 12), bg="#ffffff").pack(anchor='w')

        # Styled Treeview for Schedule Preview
        print_tree = ttk.Treeview(print_frame, columns=("Time", "Subject", "Day", "Teacher"), show="headings")
        print_tree.pack(side="left", fill="both", expand=True)

        # Define column headings and widths
        print_tree.heading("Time", text="Time")
        print_tree.heading("Subject", text="Subject")
        print_tree.heading("Day", text="Day")
        print_tree.heading("Teacher", text="Teacher")

        print_tree.column("Time", width=120)
        print_tree.column("Subject", width=120)
        print_tree.column("Day", width=80)
        print_tree.column("Teacher", width=150)

        # Insert data into the print Treeview
        for row in scheduling_tree.get_children():
            values = scheduling_tree.item(row)["values"]
            try:
                print_tree.insert("", "end", values=(values[2], values[1], values[3], values[6]))
            except IndexError as e:
                print(f"IndexError: {e} with values: {values}")  

        # ✅ Buttons Frame
        button_frame = tk.Frame(print_window, bg="#ecf0f1")
        button_frame.pack(pady=15)

        # Save as PDF Button
        def save_as_pdf():
            file_name = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
            if not file_name:
                return

            # Create PDF
            c = canvas.Canvas(file_name, pagesize=letter)
            width, height = letter

            # Header
            c.setFont("Helvetica", 16)
            c.drawString(1 * inch, height - 1 * inch, "High Horizons Learning Center")
            c.drawString(1 * inch, height - 1.25 * inch, "Schedule")

            # Adviser Info
            c.setFont("Helvetica", 12)
            c.drawString(1 * inch, height - 1.75 * inch, f"Adviser: {adviser_entry.get()}")
            c.drawString(1 * inch, height - 2.0 * inch, f"Grade Level: {grade_combo.get()}")
            c.drawString(1 * inch, height - 2.25 * inch, f"Section: {section_combo.get()}")

            # Table Headers
            y = height - 3 * inch
            c.setFont("Helvetica-Bold", 10)
            headers = ["Time", "Subject", "Day", "Teacher"]
            for i, header in enumerate(headers):
                c.drawString(1 * inch + i * 1.5 * inch, y, header)

            # Table Rows
            c.setFont("Helvetica", 10)
            y -= 0.5 * inch
            for row in scheduling_tree.get_children():
                values = scheduling_tree.item(row)["values"]
                row_data = (values[2], values[1], values[3], values[6])
                for i, value in enumerate(row_data):
                    c.drawString(1 * inch + i * 1.5 * inch, y, str(value))
                y -= 0.5 * inch

            c.save()
            messagebox.showinfo("Print", f"PDF saved as {file_name}. You can print it using any PDF viewer.")
            print_window.destroy()

        # Save PDF Button
        tk.Button(
            button_frame, text="Save as PDF", 
            command=save_as_pdf,
            font=('Arial', 12, 'bold'), bg="#3498db", fg="#ffffff", padx=15, pady=5
        ).grid(row=0, column=0, padx=10)

        # Close Button
        tk.Button(
            button_frame, text="Close", 
            command=print_window.destroy,
            font=('Arial', 12, 'bold'), bg="#e74c3c", fg="#ffffff", padx=15, pady=5
        ).grid(row=0, column=1, padx=10)


#================================================NAV BAR NAVIGATION COMMANDS=========================
    def show_dashboard_panel():
        dashboard_frame.tkraise()
        clear_input_fields()
        close_connection()
    
    def show_cashier_panel():
        cashier_frame.tkraise()
        load_cashier_data()
        clear_input_fields()
        close_connection()
        
    def show_admissions_panel():
        admission_frame.tkraise()
        load_admission_data()
        clear_input_fields()
        auto_refresh()
        close_connection()

    def show_new_user_panel():
        new_user_frame.tkraise()
        clear_input_fields()
        close_connection()

    def show_admitted_panel():
        admitted_frame.tkraise()
        load_admitted_data()
        clear_input_fields() 
        close_connection()

    def show_updates_panel():
        updates_frame.tkraise()
        load_updates_data()
        clear_input_fields()
        close_connection()

    def show_table_panel():
        table_frame.tkraise()
        load_data()
        clear_input_fields()
        close_connection()

    def show_studentmasterlist_panel():
        studentml_frame.tkraise()
        load_studentml_data()
        clear_input_fields()
        close_connection()

    def show_interview_panel():
        interview_frame.tkraise()
        load_interview_data("pending")
        clear_input_fields()
        close_connection()

    def show_scheduling_panel():
        scheduling_frame.tkraise()
        clear_input_fields()
        close_connection()

    def show_calendar_app():
        calendar_root = tk.Toplevel()  
        scheduling_calendar.CalendarApp(calendar_root)  

    def logout():
        response = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if response:
            close_connection()  # <-- Add this
            main_root.destroy()
            subprocess.run(["python", "login.py"])

#============================================UPDATE DATAGIRDVIEW CODE======================================

    # Create a function to be called on double click
    def start_admission_edit(event):
        # Get the selected item
        selected_item = tree_admission.selection()
        if selected_item:
            item_data = tree_admission.item(selected_item)
            values = item_data['values']

            # Open a new window to display the student details
            display_admission_details(values)
                        
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
            print("DEBUG: Adding Baby Book to checklist")  # Debugging
            checklist_items["Baby Book"] = "baby_book"

        # Fetch column names dynamically
        cursor.execute("SHOW COLUMNS FROM requirement_checklist")  
        columns = [col[0] for col in cursor.fetchall()]  # Extract column names

        # Fetch current checklist status from the database
        cursor.execute("SELECT * FROM requirement_checklist WHERE id = %s", (student_id,))
        row = cursor.fetchone()

        # Convert fetched data into a dictionary for correct column mapping
        requirements = dict(zip(columns, row)) if row else {}

        global checkbox_vars
        checkbox_vars.clear()

        # Title Label for Checklist
        title_label = tk.Label(
            checklist_frame, text="Requirement Checklist", font=('Arial', 14, 'bold'), 
            bg="#34495e", fg="white", pady=5
        )
        title_label.grid(row=0, column=0, columnspan=len(checklist_items), sticky="ew", pady=10)

        # Create checkboxes in a horizontal layout
        for index, (display_name, db_column) in enumerate(checklist_items.items()):
            var = tk.BooleanVar(value=bool(requirements.get(db_column, 0)))  # Fetch by column name

            chk = tk.Checkbutton(
                checklist_frame, text=display_name, variable=var, font=('Arial', 12), 
                bg="#ecf0f1", padx=5, pady=5, 
                command=lambda db_column=db_column, var=var: update_checklist_status(student_id, db_column, var)
            )
            chk.grid(row=1, column=index, padx=10, pady=5, sticky="w")  # Horizontal layout

            checkbox_vars[db_column] = var  

        # Ensure checkboxes expand properly
        checklist_frame.grid_columnconfigure(tuple(range(len(checklist_items))), weight=1)




    def update_checklist_status(student_id, item, var):
        try:
            # Update the database using the name of the checklist item
            cursor.execute(f"""
                UPDATE requirement_checklist 
                SET `{item}` = %s 
                WHERE id = %s
            """, (1 if var.get() else 0, student_id))  # 1 for checked, 0 for unchecked

            connection.commit()
            print(f"Updated {item} to {'Complete' if var.get() else 'Incomplete'} for student ID {student_id}.")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def on_admitted_row_double_click(event):
        admitted_selected_item = tree_admitted.focus()
        if not admitted_selected_item:
            messagebox.showinfo("No Selection", "No student selected.")
            return

        admitted_selected_student = tree_admitted.item(admitted_selected_item)['values']
        if not admitted_selected_student:
            messagebox.showinfo("No Data", "No student data found.")
            return
        
        show_admitted_profile_panel()
        admitted_balance_data()

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
        info_frame = tk.Frame(student_profile_frame, bg="#ffffff", padx=20, pady=20)
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

                                # Add a button to change the profile picture
                change_picture_button = tk.Button(
                    info_frame, text="Change Picture", font=('Arial', 7), bg="#3498db", fg="white", width=15,
                    command=lambda: change_profile_picture(selected_student[0], profile_label)
                )
                change_picture_button.place(x=890, y=160
                                            )  # Position just below the profile picture
            else:

                # If no profile picture is available, display a placeholder
                placeholder_label = tk.Label(info_frame, text="No Image", bg="#ffffff", fg="#000000", font=('Arial', 12))
                placeholder_label.place(x=900, y=65)  # Adjust position as needed
                                                # Add a button to change the profile picture
                change_picture_button = tk.Button(
                    info_frame, text="Add Picture", font=('Arial', 7), bg="#3498db", fg="white", width=15,
                    command=lambda: change_profile_picture(selected_student[0], profile_label)
                )
                change_picture_button.place(x=890, y=160
                                            ) 

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

        tk.Label(details_tab, text="Last Name:", font=label_font, bg="#ffffff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        name_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        name_entry.insert(0, selected_student[2])

        tk.Label(details_tab, text="First Name:", font=label_font, bg="#ffffff").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        first_name_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        first_name_entry.grid(row=2, column=1, padx=5, pady=5)
        first_name_entry.insert(0, selected_student[3])

        tk.Label(details_tab, text="Nickname:", font=label_font, bg="#ffffff").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        nickname_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        nickname_entry.grid(row=3, column=1, padx=5, pady=5)
        nickname_entry.insert(0, selected_student[4])

        tk.Label(details_tab, text="Age:", font=label_font, bg="#ffffff").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        age_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        age_entry.grid(row=4, column=1, padx=5, pady=5)
        age_entry.insert(0, selected_student[6])

        tk.Label(details_tab, text="Gender:", font=label_font, bg="#ffffff").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        gender_entry = tk.Entry(details_tab, width=40, font=entry_font, bg="#ecf0f1")
        gender_entry.grid(row=5, column=1, padx=5, pady=5)
        gender_entry.insert(0, selected_student[7])

        tk.Label(details_tab, text="Date of Birth:", font=label_font, bg="#ffffff").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        birthday_entry = DateEntry(details_tab, width=40, font=entry_font, background='darkblue', foreground='white', borderwidth=2)
        birthday_entry.grid(row=6, column=1, padx=5, pady=5)

        birthday_value = selected_student[8]
        if birthday_value and isinstance(birthday_value, str):
            try:
                birthday_entry.set_date(datetime.strptime(birthday_value, '%Y-%m-%d'))
            except ValueError as ve:
                messagebox.showerror("Date Format Error", f"This student has no Birthdate, please update immediately")
                birthday_entry.set_date(datetime.now())
        else:
            birthday_entry.set_date(datetime.now())

        tk.Label(details_tab, text="Address:", font=label_font, bg="#ffffff").grid(row=7, column=0, sticky='w', padx=5, pady=5)
        address_text = tk.Text(details_tab, font=entry_font, height=4, width=40, bg="#ecf0f1")
        address_text.grid(row=7, column=1, padx=5, pady=5)
        address_text.insert('1.0', selected_student[9])

        parents_tab = tk.Frame(notebook, bg="#ffffff")
        notebook.add(parents_tab, text="Parents Info")

        tk.Label(parents_tab, text="Father's Name:", font=label_font, bg="#ffffff").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        fathers_name_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_name_entry.grid(row=0, column=1, padx=5, pady=5)
        fathers_name_entry.insert(0, selected_student[10])

        tk.Label(parents_tab, text="Father's Age:", font=label_font, bg="#ffffff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        fathers_age_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_age_entry.grid(row=1, column=1, padx=5, pady=5)
        fathers_age_entry.insert(0, selected_student[11])

        tk.Label(parents_tab, text="Father's Email:", font=label_font, bg="#ffffff").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        fathers_email_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_email_entry.grid(row=2, column=1, padx=5, pady=5)
        fathers_email_entry.insert(0, selected_student[12])

        tk.Label(parents_tab, text="Father's Occupation:", font=label_font, bg="#ffffff").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        fathers_occupation_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_occupation_entry.grid(row=3, column=1, padx=5, pady=5)
        fathers_occupation_entry.insert(0, selected_student[13])

        tk.Label(parents_tab, text="Father's Contact Number:", font=label_font, bg="#ffffff").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        fathers_contact_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_contact_entry.grid(row=4, column=1, padx=5, pady=5)
        fathers_contact_entry.insert(0, selected_student[14])

        tk.Label(parents_tab, text="Father's Company:", font=label_font, bg="#ffffff").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        fathers_company_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        fathers_company_entry.grid(row=5, column=1, padx=5, pady=5)
        fathers_company_entry.insert(0, selected_student[15])

        tk.Label(parents_tab, text="Mother's Name:", font=label_font, bg="#ffffff").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        mothers_name_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_name_entry.grid(row=0, column=3, padx=5, pady=5)
        mothers_name_entry.insert(0, selected_student[16])

        tk.Label(parents_tab, text="Mother's Age:", font=label_font, bg="#ffffff").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        mothers_age_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_age_entry.grid(row=1, column=3, padx=5, pady=5)
        mothers_age_entry.insert(0, selected_student[17])

        tk.Label(parents_tab, text="Mother's Email:", font=label_font, bg="#ffffff").grid(row=2, column=2, sticky='w', padx=5, pady=5)
        mothers_email_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_email_entry.grid(row=2, column=3, padx=5, pady=5)
        mothers_email_entry.insert(0, selected_student[18])

        tk.Label(parents_tab, text="Mother's Occupation:", font=label_font, bg="#ffffff").grid(row=3, column=2, sticky='w', padx=5, pady=5)
        mothers_occupation_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_occupation_entry.grid(row=3, column=3, padx=5, pady=5)
        mothers_occupation_entry.insert(0, selected_student[19])

        tk.Label(parents_tab, text="Mother's Contact Number:", font=label_font, bg="#ffffff").grid(row=4, column=2, sticky='w', padx=5, pady=5)
        mothers_contact_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_contact_entry.grid(row=4, column=3, padx=5, pady=5)
        mothers_contact_entry.insert(0, selected_student[20])

        tk.Label(parents_tab, text="Mother's Company:", font=label_font, bg="#ffffff").grid(row=5, column=2, sticky='w', padx=5, pady=5)
        mothers_company_entry = tk.Entry(parents_tab, width=20, font=entry_font, bg="#ecf0f1")
        mothers_company_entry.grid(row=5, column=3, padx=5, pady=5)
        mothers_company_entry.insert(0, selected_student[21])

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
      
        load_special_needs_data()

        selected_student_special_needs_data = next((row for row in special_needs_data if row[0] == selected_student[0]), None)        

        tk.Label(educational_bg_tab, text="Special Needs:", font=label_font, bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky='nw')
        special_needs_text = tk.Text(educational_bg_tab, font=entry_font, height=4, width=80, bg="#ecf0f1")
        special_needs_text.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        special_needs_text.insert('1.0', selected_student_special_needs_data[1])
    
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
        upload_button.grid(row=6, column=1, padx=5, pady=5, sticky='w')

        view_button = tk.Button(additional_info_tab, text="Uploaded GRADES", font=('Arial', 12), 
                                command=lambda: view_uploaded_grades(selected_student[0]), bg="#2ecc71", fg="white")

        # Position the button using .place()
        view_button.place(x=280, y=272, width=160, height=33)  # Adjust x, y, width, and height as needed


            # Add the "Login Credentials" button next to the "Upload GRADES" button
        login_credentials_button = tk.Button(additional_info_tab, text="Login Credentials", font=('Arial', 12), command=lambda: show_login_credentials(selected_student[0]), bg="#2ecc71", fg="white")
        login_credentials_button.grid(row=5, column=2, padx=5, pady=5, sticky='w')

        load_balance_data()

        selected_student_finance_data = next((row for row in finance_data if row[2] == selected_student[0]), None)

        tk.Label(additional_info_tab, text="Payment Type:", font=label_font, bg="#ffffff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        payment_type_var = tk.StringVar()
        payment_type_combobox = ttk.Combobox(additional_info_tab, textvariable=payment_type_var, font=entry_font, state='readonly')
        payment_type_combobox['values'] = ("Annual", "Semestral", "Quarterly", "Monthly")
        payment_type_combobox.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        if selected_student_finance_data and len(selected_student_finance_data) > 2:
            payment_type_combobox.set(selected_student_finance_data[8])
        else:
            payment_type_combobox.set("Not Available")

        def on_combobox_select(event):
            selected_value = payment_type_var.get()

        payment_type_combobox.bind("<<ComboboxSelected>>", on_combobox_select)

        tk.Label(additional_info_tab, text="Balance:", font=label_font, bg="#ffffff").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        balance_entry = tk.Entry(additional_info_tab, width=40, font=entry_font, bg="#ecf0f1")
        balance_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        if selected_student_finance_data and len(selected_student_finance_data) >= 4:
            balance_entry.insert(0, selected_student_finance_data[19])
        else:
            balance_entry.insert(0, "Not Available")

        tk.Label(additional_info_tab, text="Amount Paid:", font=label_font, bg="#ffffff").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        amount_paying_entry = tk.Entry(additional_info_tab, width=40, font=entry_font, bg="#ecf0f1")
        amount_paying_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)

        tk.Label(additional_info_tab, text="Due Date:", font=label_font, bg="#ffffff").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        due_date_entry = DateEntry(additional_info_tab, width=40, font=entry_font, background='darkblue', 
                                foreground='white', borderwidth=2, date_pattern="yyyy-MM-dd")  
        due_date_entry.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        if selected_student_finance_data and len(selected_student_finance_data) >= 5:
            try:
                stored_due_date = datetime.strptime(str(selected_student_finance_data[10]), "%Y-%m-%d")  
                due_date_entry.set_date(stored_due_date)
            except:
                due_date_entry.set_date(datetime.now()) 
        else:
            due_date_entry.set_date(datetime.now())  


        checklist_tab = tk.Frame(notebook, bg="#ffffff")
        notebook.add(checklist_tab, text="Requirement Checklist")

        tk.Label(checklist_tab, text="Requirement Checklist", font=('Arial', 18, 'bold'), bg="#ffffff").pack(pady=10)

        # Load the requirement checklist items for the selected student
        load_requirement_checklist(selected_student[0], checklist_tab)

        # Create Save and Back buttons
        button_frame = tk.Frame(student_profile_frame, bg="#f4f4f4")  # Container for buttons
        button_frame.grid(row=4, column=0, columnspan=4, pady=20, sticky="w")  # Align frame to the left

        # Save Button
        save_button = tk.Button(button_frame, text="Save", command=lambda: save_student_data(selected_student[0]), 
                                font=('Arial', 12, 'bold'), bg="#27ae60", fg="#ffffff", height=2, width=12)
        save_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Align left

        # Re-enroll Button
        re_enroll_button = tk.Button(button_frame, text="Re-enroll", command=lambda: re_enroll_student(selected_student[0]), 
                                    font=('Arial', 12, 'bold'), bg="#2980b9", fg="#ffffff", height=2, width=12)
        re_enroll_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")  # Align left

        # Back Button
        back_button = tk.Button(button_frame, text="Back", command=lambda: show_studentmasterlist_panel(), 
                                font=('Arial', 12, 'bold'), bg="#c0392b", fg="#ffffff", height=2, width=12)
        back_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")  # Align left


        def change_profile_picture(student_id, profile_label):
            """Allow the user to select and update the profile picture."""
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
            
            if file_path:
                try:
                    # Open the selected image
                    image = Image.open(file_path)
                    image = image.resize((100, 100), Image.Resampling.LANCZOS)
                    profile_photo = ImageTk.PhotoImage(image)

                    # Update the profile label
                    profile_label.config(image=profile_photo)
                    profile_label.image = profile_photo  # Keep a reference

                    # Convert image to binary for database storage
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    profile_picture_data = img_byte_arr.getvalue()

                    # Update the database
                    cursor = connection.cursor()
                    query = "UPDATE studentinfo SET profile_picture = %s WHERE student_id = %s"
                    cursor.execute(query, (profile_picture_data, student_id))
                    query = "UPDATE student_history SET profile_picture = %s WHERE student_id = %s"
                    cursor.execute(query, (profile_picture_data, student_id))

                    connection.commit()

                    messagebox.showinfo("Success", "Profile picture updated successfully!")

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update profile picture: {e}")

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
            """Update the student data in the database."""
            lrn = lrn_entry.get()
            last_name = name_entry.get()
            first_name = first_name_entry.get()
            nickname = nickname_entry.get()
            age = age_entry.get()
            gender = gender_entry.get()
            birthday = birthday_entry.get_date()
            address = address_text.get("1.0", tk.END).strip()

            father_name = fathers_name_entry.get()
            father_age = fathers_age_entry.get()
            father_email = fathers_email_entry.get()
            father_occupation = fathers_occupation_entry.get()
            father_contact = fathers_contact_entry.get()
            father_company = fathers_company_entry.get()

            special_needs = special_needs_text.get("1.0", tk.END).strip()

            mother_name = mothers_name_entry.get()
            mother_age = mothers_age_entry.get()
            mother_email = mothers_email_entry.get()
            mother_occupation = mothers_occupation_entry.get()
            mother_contact = mothers_contact_entry.get()
            mother_company = mothers_company_entry.get().strip()
            student_status = student_status_combo.get().strip()
            parents_status = status_var.get()

            payment_type = payment_type_combobox.get().strip()
            balance_value = balance_entry.get().strip()
            amount_paid_value = amount_paying_entry.get().strip()

            # Ensure balance values are numeric
            balance_value = int(balance_value) if balance_value.isdigit() else 0
            amount_paid_value = int(amount_paid_value) if amount_paid_value.isdigit() else 0
            current_date_updated_sb = datetime.now().strftime('%Y-%m-%d')
            due_date = due_date_entry.get_date().strftime('%Y-%m-%d')

            remaining_balance = balance_value - amount_paid_value

            # Get the current school year range (May to April)
            current_date = datetime.now()
            current_year = current_date.year
            current_month = current_date.month

            if current_month >= 5:  # If May or later, the school year starts this year
                start_year = current_year
                end_year = current_year + 1
            else:  # If before May, the school year started last year
                start_year = current_year - 1
                end_year = current_year

            # Validate inputs
            if not last_name or not first_name:
                messagebox.showerror("Input Error", "Last Name and First Name are required.")
                return

            try:
                cursor.execute("""
                    UPDATE studentinfo 
                    SET LRN = %s, last_name = %s, first_name = %s, nickname = %s, age = %s, 
                        gender = %s, birthday = %s, address = %s, 
                        father = %s, father_age = %s, father_email = %s, 
                        father_occupation = %s, father_contact = %s, father_company = %s, 
                        mother = %s, mother_age = %s, mother_email = %s, 
                        mother_occupation = %s, mother_contact = %s, mother_company = %s, 
                        parents_status = %s, student_status = %s, special_needs = %s
                    WHERE student_id = %s
                """, (lrn, last_name, first_name, nickname, age, gender, birthday, address,
                    father_name, father_age, father_email, father_occupation, father_contact, father_company,
                    mother_name, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                    parents_status, student_status, special_needs, student_id))

                connection.commit()

                cursor.execute("""
                    UPDATE student_history 
                    SET LRN = %s, last_name = %s, first_name = %s, nickname = %s, age = %s, 
                        gender = %s, birthday = %s, address = %s, 
                        father = %s, father_age = %s, father_email = %s, 
                        father_occupation = %s, father_contact = %s, father_company = %s, 
                        mother = %s, mother_age = %s, mother_email = %s, 
                        mother_occupation = %s, mother_contact = %s, mother_company = %s, 
                        parents_status = %s, student_status = %s, special_needs = %s
                    WHERE student_id = %s
                """, (lrn, last_name, first_name, nickname, age, gender, birthday, address,
                    father_name, father_age, father_email, father_occupation, father_contact, father_company,
                    mother_name, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                    parents_status, student_status, special_needs, student_id))

                connection.commit()

                # Updated query to ensure date_enrolled is within May-April school year
                cursor.execute("""
                    UPDATE student_balance 
                    SET date_added = %s, payment_status = %s, due_date = %s, 
                        amount_paid = %s, balance = %s 
                    WHERE student_id = %s 
                """, (current_date_updated_sb, payment_type, due_date, 
                    amount_paid_value, remaining_balance, student_id))

                connection.commit()

                messagebox.showinfo("Success", "Student data updated successfully.")
                studentml_frame.tkraise()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error updating student data: {err}")

            student_profile_frame.tkraise()


        def re_enroll_student(student_id):
            """Re-enroll a student by updating their grade level and re-inserting all data into student_history."""
            try:
                # Get the current date for date_enrolled
                current_date = datetime.now().strftime('%Y-%m-%d')

                # Determine the school year
                current_year = datetime.now().year
                current_month = datetime.now().month
                school_year = current_year if current_month >= 6 else current_year - 1

                # Fetch the student's current data
                cursor.execute("""SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, profile_picture, special_needs 
                               FROM studentinfo WHERE student_id = %s""", (student_id,))
                result = cursor.fetchone()

                if result is None:
                    messagebox.showerror("Error", "Student not found.")
                    return

                # Extract values safely
                (student_id, lrn, last_name, first_name, nickname, grade_level, age, gender, birthday, address,
                father, father_age, father_email, father_occupation, father_contact, father_company,
                mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                parents_status, date_enrolled, year, profile_picture, special_needs) = result[:27]  # Ensure correct slicing

                # Define grade progression
                grade_progression = {
                    "Junior Nursery": "Senior Nursery",
                    "Senior Nursery": "Kindergarten",
                    "Kindergarten": "Grade 1",
                    "Grade 1": "Grade 2",
                    "Grade 2": "Grade 3",
                    "Grade 3": "Grade 4",
                    "Grade 4": "Grade 5",
                    "Grade 5": "Grade 6"
                }

                # Determine new grade level
                new_grade_level = grade_progression.get(grade_level, grade_level)  # Keep grade level if at max

                # Update studentinfo
                cursor.execute("""
                    UPDATE studentinfo 
                    SET grade_level = %s, date_enrolled = %s, year = %s
                    WHERE student_id = %s
                """, (new_grade_level, current_date, school_year, student_id))
                connection.commit()

                current_date_added_sb = datetime.now().strftime('%Y-%m-%d')  
                cursor.execute("""
                    INSERT INTO student_balance (date_added, student_id, name, grade_level, date_enrolled) 
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE date_added = VALUES(date_added)
                """, (current_date_added_sb, student_id, first_name + " " + last_name, new_grade_level, date_enrolled))
                connection.commit()

                # Re-insert into student_history
                cursor.execute("""
                    INSERT INTO student_history (
                        student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                        father_age, father_email, father_occupation, father_contact, father_company, 
                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                        parents_status, date_enrolled, year, profile_picture, special_needs
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    student_id, lrn, last_name, first_name, nickname, new_grade_level, age, gender, birthday, address, father, 
                    father_age, father_email, father_occupation, father_contact, father_company, 
                    mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                    parents_status, current_date, school_year, profile_picture, special_needs
                ))
                connection.commit()


                messagebox.showinfo("Success", f"Student successfully re-enrolled for {school_year}.")

                # Refresh UI
                load_studentml_data()
                clear_input_fields()

            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")


        def show_login_credentials(student_id):
            """Fetch and display the student's login credentials."""
            try:
                cursor = connection.cursor()
                query = "SELECT username, pass FROM logininfo WHERE info_no = %s"
                cursor.execute(query, (student_id,))
                result = cursor.fetchone()

                if result:
                    username, password = result
                    credentials_window = tk.Toplevel()
                    credentials_window.title("Student Login Credentials")
                    credentials_window.geometry("300x150")

                    tk.Label(credentials_window, text="Username:", font=('Arial', 12)).pack(pady=5)
                    tk.Label(credentials_window, text=username, font=('Arial', 12, 'bold')).pack()

                    tk.Label(credentials_window, text="Password:", font=('Arial', 12)).pack(pady=5)
                    tk.Label(credentials_window, text=password, font=('Arial', 12, 'bold')).pack()

                else:
                    messagebox.showinfo("No Credentials", "No login credentials found for this student.")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error fetching login credentials: {err}")
                
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


    def show_admitted_profile_panel():
        global admitted_selected_student
        global admitted_id_entry, grade_entry, name_entry, address_text, selected_student, checkbox_vars
        label_font = tkFont.Font(family="Arial", size=12)
        entry_font = tkFont.Font(family="Arial", size=11)

        checkbox_vars = {}

        # Configure content_frame to allow expansion
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        admitted_profile_frame = tk.Frame(content_frame, bg="#f4f4f4", bd=2, relief="ridge")
        admitted_profile_frame.grid(row=0, column=0, sticky="nsew")  # Expands fully

        # Allow it to stretch inside content_frame
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        admitted_profile_frame.grid_rowconfigure(0, weight=1)
        admitted_profile_frame.grid_columnconfigure(0, weight=1)


        for widget in admitted_profile_frame.winfo_children():
            widget.destroy()

        admitted_selected_item = tree_admitted.focus()
        if not admitted_selected_item:
            messagebox.showinfo("No Selection", "No student selected.")
            return

        admitted_selected_student = tree_admitted.item(admitted_selected_item)['values']
        if not admitted_selected_student or len(admitted_selected_student) < 20:
            messagebox.showerror("Data Error", "Incomplete student data.")
            return
            
        admitted_info_frame = tk.Frame(admitted_profile_frame, bg="#ffffff", bd=2, relief="solid")
        admitted_info_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Ensure it expands inside the parent
        admitted_profile_frame.grid_rowconfigure(0, weight=1)
        admitted_profile_frame.grid_columnconfigure(0, weight=1)

        admitted_info_frame.grid_rowconfigure(0, weight=1)
        admitted_info_frame.grid_columnconfigure(0, weight=1)


        tk.Label(admitted_info_frame, text="STUDENT DETAILS", font=('Arial', 16, 'bold'), 
                bg="#34495e", fg="white", padx=30, pady=10).grid(row=0, column=0, columnspan=4, pady=10, sticky='ew')

        # Admission ID
        tk.Label(admitted_info_frame, text="Admission ID:", font=('Arial', 14, 'bold'), bg="#ffffff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        admitted_id_entry = tk.Entry(admitted_info_frame, width=40, font=('Arial', 14), relief="solid", bd=1, bg="#ecf0f1")
        admitted_id_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        admitted_id_entry.insert(0, admitted_selected_student[0])
        admitted_id_entry.config(state='readonly')

        # Notebook Tabs (Student Details, etc.)
        admitted_notebook = ttk.Notebook(admitted_info_frame)
        admitted_notebook.grid(row=3, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

        admitted_details_tab = tk.Frame(admitted_notebook, bg="#ecf0f1")
        admitted_notebook.add(admitted_details_tab, text="Student Details")

        tk.Label(admitted_details_tab, text="Last Name:", font=('Arial', 14), bg="#ecf0f1").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        name_entry = tk.Entry(admitted_details_tab, width=40, font=('Arial', 14))
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        name_entry.insert(0, admitted_selected_student[1])  

        tk.Label(admitted_details_tab, text="First Name:", font=('Arial', 14), bg="#ecf0f1").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        first_name_entry = tk.Entry(admitted_details_tab, width=40, font=('Arial', 14))
        first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        first_name_entry.insert(0, admitted_selected_student[2])  

        tk.Label(admitted_details_tab, text="Nickname:", font=('Arial', 14), bg="#ecf0f1").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        nickname_entry = tk.Entry(admitted_details_tab, width=40, font=('Arial', 14))
        nickname_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        nickname_entry.insert(0, admitted_selected_student[3])  

        tk.Label(admitted_details_tab, text="Age:", font=('Arial', 14), bg="#ecf0f1").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        age_entry = tk.Entry(admitted_details_tab, width=40, font=('Arial', 14))
        age_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        age_entry.insert(0, admitted_selected_student[5])  

        tk.Label(admitted_details_tab, text="Gender:", font=('Arial', 14), bg="#ecf0f1").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        gender_entry = tk.Entry(admitted_details_tab, width=40, font=('Arial', 14))
        gender_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        gender_entry.insert(0, admitted_selected_student[6])  

        tk.Label(admitted_details_tab, text="Date of Birth:", font=('Arial', 14), bg="#ecf0f1").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        birthday_entry = DateEntry(admitted_details_tab, width=40, font=('Arial', 14), background='darkblue', foreground='white', borderwidth=2)
        birthday_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        birthday_value = admitted_selected_student[4]  
        if birthday_value and isinstance(birthday_value, str):  
            try:
                birthday_entry.set_date(datetime.strptime(birthday_value, '%Y-%m-%d'))
            except ValueError as ve:
                messagebox.showerror("Date Format Error", "This student has no Birthdate, please update immediately")
                birthday_entry.set_date(datetime.now())  
        else:
            birthday_entry.set_date(datetime.now())  

        tk.Label(admitted_details_tab, text="Address:", font=('Arial', 14), bg="#ecf0f1").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        address_text = tk.Text(admitted_details_tab, font=('Arial', 12), height=4, width=40)
        address_text.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        address_text.insert('1.0', admitted_selected_student[7]) 

        admitted_parents_tab = tk.Frame(admitted_notebook, bg="#ecf0f1")
        admitted_notebook.add(admitted_parents_tab, text="Parents Info")

        tk.Label(admitted_parents_tab, text="Father's Name:", font=('Arial', 14), bg="#ecf0f1").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        a_fathers_name_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_fathers_name_entry.grid(row=0, column=1, padx=5, pady=5)
        a_fathers_name_entry.insert(0, admitted_selected_student[8])

        tk.Label(admitted_parents_tab, text="Father's Age:", font=('Arial', 14), bg="#ecf0f1").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        a_fathers_age_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_fathers_age_entry.grid(row=1, column=1, padx=5, pady=5)
        a_fathers_age_entry.insert(0, admitted_selected_student[9])  

        tk.Label(admitted_parents_tab, text="Father's Email:", font=('Arial', 14), bg="#ecf0f1").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        a_fathers_email_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_fathers_email_entry.grid(row=2, column=1, padx=5, pady=5)
        a_fathers_email_entry.insert(0, admitted_selected_student[10])  

        tk.Label(admitted_parents_tab, text="Father's Number:", font=('Arial', 14), bg="#ecf0f1").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        a_fathers_contact_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_fathers_contact_entry.grid(row=3, column=1, padx=5, pady=5)
        a_fathers_contact_entry.insert(0, admitted_selected_student[11])  

        tk.Label(admitted_parents_tab, text="Father's Occupation:", font=('Arial', 14), bg="#ecf0f1").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        a_fathers_occupation_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_fathers_occupation_entry.grid(row=4, column=1, padx=5, pady=5)
        a_fathers_occupation_entry.insert(0, admitted_selected_student[12])  

        tk.Label(admitted_parents_tab, text="Father's Company:", font=('Arial', 14), bg="#ecf0f1").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        a_fathers_company_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_fathers_company_entry.grid(row=5, column=1, padx=5, pady=5)
        a_fathers_company_entry.insert(0, admitted_selected_student[13])  

        tk.Label(admitted_parents_tab, text="Mother's Name:", font=('Arial', 14), bg="#ecf0f1").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        a_mothers_name_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_mothers_name_entry.grid(row=0, column=3, padx=5, pady=5)
        a_mothers_name_entry.insert(0, admitted_selected_student[14])  

        tk.Label(admitted_parents_tab, text="Mother's Age:", font=('Arial', 14), bg="#ecf0f1").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        a_mothers_age_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_mothers_age_entry.grid(row=1, column=3, padx=5, pady=5)
        a_mothers_age_entry.insert(0, admitted_selected_student[15])  

        tk.Label(admitted_parents_tab, text="Mother's Email:", font=('Arial', 14), bg="#ecf0f1").grid(row=2, column=2, sticky='w', padx=5, pady=5)
        a_mothers_email_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_mothers_email_entry.grid(row=2, column=3, padx=5, pady=5)
        a_mothers_email_entry.insert(0, admitted_selected_student[16])  

        tk.Label(admitted_parents_tab, text="Mother's Number:", font=('Arial', 14), bg="#ecf0f1").grid(row=3, column=2, sticky='w', padx=5, pady=5)
        a_mothers_contact_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_mothers_contact_entry.grid(row=3, column=3, padx=5, pady=5)
        a_mothers_contact_entry.insert(0, admitted_selected_student[17])

        tk.Label(admitted_parents_tab, text="Mother's Occupation:", font=('Arial', 14), bg="#ecf0f1").grid(row=4, column=2, sticky='w', padx=5, pady=5)
        a_mothers_occupation_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_mothers_occupation_entry.grid(row=4, column=3, padx=5, pady=5)
        a_mothers_occupation_entry.insert(0, admitted_selected_student[18]) 
        
        tk.Label(admitted_parents_tab, text="Mother's Company:", font=('Arial', 14), bg="#ecf0f1").grid(row=5, column=2, sticky='w', padx=5, pady=5)
        a_mothers_company_entry = tk.Entry(admitted_parents_tab, width=20, font=('Arial', 14))
        a_mothers_company_entry.grid(row=5, column=3, padx=5, pady=5)
        a_mothers_company_entry.insert(0, admitted_selected_student[19])  

        # Set styles
        style = ttk.Style()
        style.configure("Custom.TNotebook", background="#f4f4f4", borderwidth=0)
        style.configure("Custom.Treeview", font=('Arial', 12), background="white", rowheight=25)
        admitted_notebook.configure(style="Custom.TNotebook")

        # Buttons frame (expands horizontally)
        button_frame = tk.Frame(admitted_profile_frame, bg="#f4f4f4")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky="ew")

        enroll_button = tk.Button(button_frame, text="Enroll Student", command=lambda: enroll_student(admitted_selected_student[0]),
                                font=('Arial', 12, 'bold'), bg="#2ecc71", fg="white", relief="raised", bd=2, padx=15, pady=5)
        enroll_button.grid(row=0, column=0, padx=10)

        back_button = tk.Button(button_frame, text="Back", command=lambda: show_admitted_panel(),
                                font=('Arial', 12, 'bold'), bg="#e74c3c", fg="white", relief="raised", bd=2, padx=15, pady=5)
        back_button.grid(row=0, column=1, padx=10)

            # Ensure expansion of inner elements
        admitted_info_frame.grid_rowconfigure(3, weight=1)
        admitted_info_frame.grid_columnconfigure(0, weight=1)

        admitted_notebook.grid_rowconfigure(0, weight=1)
        admitted_notebook.grid_columnconfigure(0, weight=1)

        admitted_details_tab.grid_rowconfigure(0, weight=1)
        admitted_details_tab.grid_columnconfigure(1, weight=1)
        
        admitted_additional_info_tab = tk.Frame(admitted_notebook, bg="#ecf0f1")
        admitted_notebook.add(admitted_additional_info_tab, text="Additional Information")

        admitted_balance_data()
        print(finance_data)

        selected_student_finance_data = next((row for row in finance_data if row[2] == str(admitted_selected_student[0])), None)

        tk.Label(admitted_additional_info_tab, text="Payment Type:", font=label_font, bg="#ffffff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        payment_type_var = tk.StringVar()
        payment_type_combobox = ttk.Combobox(admitted_additional_info_tab, textvariable=payment_type_var, font=entry_font, state='readonly')
        payment_type_combobox['values'] = ("Annual", "Semestral", "Quarterly", "Monthly")
        payment_type_combobox.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        if selected_student_finance_data and len(selected_student_finance_data) > 2:
            payment_type_combobox.set(selected_student_finance_data[8])
        else:
            payment_type_combobox.set("Not Available")

        def on_combobox_select(event):
            selected_value = payment_type_var.get()

        payment_type_combobox.bind("<<ComboboxSelected>>", on_combobox_select)

        tk.Label(admitted_additional_info_tab, text="Balance:", font=label_font, bg="#ffffff").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        balance_entry = tk.Entry(admitted_additional_info_tab, width=40, font=entry_font, bg="#ecf0f1")
        balance_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        if selected_student_finance_data and len(selected_student_finance_data) >= 4:
            balance_entry.insert(0, selected_student_finance_data[19])
        else:
            balance_entry.insert(0, "Not Available")

        tk.Label(admitted_additional_info_tab, text="Amount Paid:", font=label_font, bg="#ffffff").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        amount_paying_entry = tk.Entry(admitted_additional_info_tab, width=40, font=entry_font, bg="#ecf0f1")
        amount_paying_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)

        tk.Label(admitted_additional_info_tab, text="Due Date:", font=label_font, bg="#ffffff").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        due_date_entry = DateEntry(admitted_additional_info_tab, width=40, font=entry_font, background='darkblue', 
                                foreground='white', borderwidth=2, date_pattern="yyyy-MM-dd")  
        due_date_entry.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        if selected_student_finance_data and len(selected_student_finance_data) >= 5:
            try:
                stored_due_date = datetime.strptime(str(selected_student_finance_data[10]), "%Y-%m-%d")  
                due_date_entry.set_date(stored_due_date)
            except:
                due_date_entry.set_date(datetime.now()) 
        else:
            due_date_entry.set_date(datetime.now())  

        admitted_checklist_tab = tk.Frame(admitted_notebook, bg="#ecf0f1")
        admitted_notebook.add(admitted_checklist_tab, text="Requirement Checklist")
        

        tk.Label(admitted_checklist_tab, text="Requirement Checklist", font=('Arial', 18, 'bold'), bg="#ecf0f1").pack(pady=10)

        load_requirement_checklist(admitted_selected_student[0], admitted_checklist_tab)

    def update_subject_combo(grade_level):
        subjects = get_subjects_by_grade_level(grade_level)
        subject_combo['values'] = subjects
        if subjects:
            subject_combo.set(subjects[0]) 

    def update_section(event):
        section = section_combo.get()
        adviser = get_adviser_by_section(section)
        grade_level = get_grade_level_by_section(section)

        if adviser:
            adviser_entry.config(state=tk.NORMAL)  
            adviser_entry.delete(0, tk.END) 
            adviser_entry.insert(0, adviser)
            adviser_entry.config(state=tk.DISABLED)  

        if grade_level:
            grade_combo.set(grade_level) 
            update_subject_combo(grade_level)  

    def get_selected_days():
        days = []
        if mon_var.get():
            days.append("M")
        if tue_var.get():
            days.append("T")
        if wed_var.get():
            days.append("W")
        if thu_var.get():
            days.append("TH")  
        if fri_var.get():
            days.append("F")
        return "-".join(days) 

#=======================================================WINDOW + FRAMES + LAYOUT================================================
    main_root = tk.Toplevel()
    main_root.attributes('-fullscreen', True)  # Make it full screen
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

        welcome_label = tk.Label(top_right_frame, text="ADMIN", font=('Arial', 14, 'bold'), bg="#0f1074", fg="#E4E6C9")
        welcome_label.pack(side="left")

    def open_section_window():
        section_window = tk.Toplevel()
        section_window.title("Add Section")
        section_window.resizable(False, False)

        window_width = 900  
        window_height = 600  

        screen_width = section_window.winfo_screenwidth()
        screen_height = section_window.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        section_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Create main frame with padding
        section_frame = tk.Frame(section_window, bg="#ffffff", padx=20, pady=20)
        section_frame.pack(fill="both", expand=True)

        # Create a frame for the title (for the background box)
        title_frame = tk.Frame(section_frame, bg="#0f1074", height=100)  # Light blue background
        title_frame.pack(fill="x", side="top" )
        title_frame.pack_propagate(False)  # Prevent resizing based on child widgets


        # Add an icon
        icon_image = PhotoImage(file="images/chapter.png")  # Replace with the actual path to your icon
        icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
        icon_label.image = icon_image  # Keep a reference to avoid garbage collection
        icon_label.pack(side="left", padx=10)

        # Title Label
        title_label = tk.Label(
            title_frame,
            text="Section Masterlist",
            font=("Arial", 30, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10)

        # Input Frame (Horizontal Layout)
        input_frame = tk.Frame(section_frame, bg="#ffffff")
        input_frame.pack(fill="x", pady=10)

        grade_levels = [f"Grade {i}" for i in range(1, 7)]
        sections = ["Competence", "Conscientiousness", "Compassion", "Commitment", "Love of Country", "Magis"]
        advisers = ["Adviser A", "Adviser B", "Adviser C"]  # Replace with get_teachers()

        # Create ComboBoxes in a single row
        labels = ["Grade Level:", "Section:", "Adviser:"]
        values = [grade_levels, sections, advisers]
        combo_boxes = []

        for i in range(3):
            frame = tk.Frame(input_frame, bg="#ffffff")
            frame.pack(side="left", expand=True, padx=10)

            tk.Label(frame, text=labels[i], font=('Arial', 12, 'bold'), bg="#ffffff").pack(anchor="w")
            combo = ttk.Combobox(frame, values=values[i], state='readonly',font=('Arial', 12))
            combo.pack(fill="x", padx=5, pady=5)
            combo_boxes.append(combo)

        # Submit Button (placed in a new frame to align with combo boxes)
        button_frame = tk.Frame(input_frame, bg="#ffffff")
        button_frame.pack(side="left", expand=True, padx=10, pady=15)  # Added top margin (pady=15)

        submit_button = tk.Button(
            button_frame, text="Submit", font=('Arial', 12, 'bold'), bg="#27ae60", fg="#ffffff",
            width=12, height=2,  # Adjusted width and height
            command=lambda: submit_data(combo_boxes[0], combo_boxes[1], combo_boxes[2], section_tree)
        )
        submit_button.pack(fill="x", padx=5, pady=5)  # Kept padding for consistency

        # Table Frame
        table_frame = tk.Frame(section_frame, bg="#ffffff")
        table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Treeview Table
        columns = ["ID", "Grade_Level", "Section", "Adviser"]
        section_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        for col in columns:
            section_tree.heading(col, text=col)
            section_tree.column(col, width=200, anchor='center')

        section_tree.pack(expand=True, fill='both')

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=section_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=section_tree.xview)
        section_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')

        section_display_data(section_tree)

    def open_teacher_window():
        global teacher_tree

        # Create Teacher Window
        teacher_window = tk.Toplevel()
        teacher_window.title("Add Teacher")
        teacher_window.resizable(False, False)

        # Center Window on Screen
        window_width, window_height = 900, 600
        screen_width, screen_height = teacher_window.winfo_screenwidth(), teacher_window.winfo_screenheight()
        position_x, position_y = (screen_width // 2 - window_width // 2), (screen_height // 2 - window_height // 2)
        teacher_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Main Frame
        teacher_frame = tk.Frame(teacher_window, bg="#ecf0f1", padx=20, pady=20)
        teacher_frame.pack(fill="both", expand=True)

        #Create a frame for the title (for the background box)
        title_frame = tk.Frame(teacher_frame, bg="#0f1074", height=100)  # Light blue background
        title_frame.pack(fill="x", side="top" )
        title_frame.pack_propagate(False)  # Prevent resizing based on child widgets


        # Add an icon
        icon_image = PhotoImage(file="images/teach.png")  # Replace with the actual path to your icon
        icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
        icon_label.image = icon_image  # Keep a reference to avoid garbage collection
        icon_label.pack(side="left", padx=10)

        # Title Label
        title_label = tk.Label(
            title_frame,
            text="Teacher Input Form",
            font=("Arial", 30, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10)

        # Input Frame
        input_frame = tk.Frame(teacher_frame, bg="#ecf0f1")
        input_frame.pack(pady=10, fill='x')

           # === Row 1: ID_NO | Contact | Email ===
        tk.Label(input_frame, text="ID_NO:", font=('Arial', 14), bg="#ecf0f1").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        id_no_entry = tk.Entry(input_frame, font=('Arial', 12), width=10)
        id_no_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Contact:", font=('Arial', 14), bg="#ecf0f1").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(input_frame, font=('Arial', 12), width=20)
        contact_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Email:", font=('Arial', 14), bg="#ecf0f1").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        email_entry = tk.Entry(input_frame, font=('Arial', 12), width=25)
        email_entry.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        # === Row 2: Name | Address ===
        tk.Label(input_frame, text="Name:", font=('Arial', 14), bg="#ecf0f1").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(input_frame, font=('Arial', 12), width=40)
        name_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Address:", font=('Arial', 14), bg="#ecf0f1").grid(row=1, column=3, padx=5, pady=5, sticky="e")
        address_entry = tk.Entry(input_frame, font=('Arial', 12), width=40)
        address_entry.grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky="w")

        # === Picture Frame (Fixed Size) ===
        picture_frame = tk.Frame(input_frame, bg="white", width=150, height=150, relief="solid", bd=2)
        picture_frame.grid(row=0, column=6, rowspan=3, padx=20, pady=5, sticky="n")
        picture_frame.pack_propagate(False)

        picture_label = tk.Label(picture_frame, bg="white")
        picture_label.pack(expand=True, fill="both")

            # === Button Frame (Below "Name") ===
        button_frame = tk.Frame(input_frame, bg="#ecf0f1")
        button_frame.grid(row=2, column=1, columnspan=5, pady=10)

            ## Select Picture Button
        picture_button = tk.Button(
            button_frame, text="Select Picture", font=('Arial', 12), bg="#2980b9", fg="white",
            width=15, command=lambda: select_picture(picture_label)
        )
        picture_button.pack(side="left", padx=10, pady=5)

        # Submit Button
        submit_button = tk.Button(
            button_frame, text="Submit", font=('Arial', 12), bg="#27ae60", fg="white",
            width=15, command=lambda: add_teacher(
                id_no_entry, name_entry, address_entry, contact_entry, email_entry, picture_label, teacher_tree
            )
        )
        submit_button.pack(side="left", padx=10, pady=5)

        # Adjust Grid Columns for Responsive Layout
        for col in range(6):
            input_frame.grid_columnconfigure(col, weight=1, minsize=100)

        # === Treeview Frame ===
        tree_frame = tk.Frame(teacher_frame)
        tree_frame.pack(fill='both', expand=True, pady=20)

        # Teacher Treeview (Added "Address" Column)
        teacher_columns = ["ID", "ID_NO", "Name", "Contact", "Email", "Address"]
        teacher_tree = ttk.Treeview(tree_frame, columns=teacher_columns, show="headings", height=20)

        for col in teacher_columns:
            teacher_tree.heading(col, text=col)
            teacher_tree.column(col, width=120, anchor='center')

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=teacher_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=teacher_tree.xview)
        teacher_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Pack Treeview and Scrollbars
        teacher_tree.pack(expand=True, fill='both', padx=20, pady=10)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')

        # Load Teacher Data
        load_teacher_data(teacher_tree)

        # Double-Click Event to Show Teacher Profile
        teacher_tree.bind("<Double-1>", lambda event: show_teacher_profile(teacher_tree))


        teacher_frame.update_idletasks()
        
    def show_teacher_profile(tree):
        selected_item = tree.selection()[0]
        teacher_id = tree.item(selected_item)['values'][0]

        cursor.execute("SELECT * FROM teacher WHERE ID = %s", (teacher_id,))
        teacher_data = cursor.fetchone()

        if teacher_data:
            profile_window = tk.Toplevel()
            profile_window.title(f"Teacher Profile - {teacher_data[2]}")

            # Disable maximize button
            profile_window.resizable(False, False)  # Prevents resizing
            profile_window.attributes('-toolwindow', True)  # Optional: Hides maximize button on Windows

            # Set fixed window size and center on screen
            window_width, window_height = 900, 500
            screen_width = profile_window.winfo_screenwidth()
            screen_height = profile_window.winfo_screenheight()
            x_position = (screen_width // 2) - (window_width // 2)
            y_position = (screen_height // 2) - (window_height // 2)
            profile_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

            # Background Image
            bg_image = Image.open("images/back.png")  # Replace with actual file path
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(profile_window, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(relwidth=1, relheight=1)

             # Header Section (Full Width)
            header_frame = tk.Frame(profile_window, bg="#0f1074")
            header_frame.place(x=0, y=0, width=900, height=60)
            
            # Create a container frame inside header_frame
            logo_text_frame = tk.Frame(header_frame, bg="#0f1074")
            logo_text_frame.pack(side="top", pady=5)  # Centered in the header_frame

            # Load and display logo
            logo_image = Image.open("images/high.png")
            logo_image.thumbnail((80, 80))
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(logo_text_frame, image=logo_photo, bg="#0f1074")
            logo_label.image = logo_photo
            logo_label.pack(side="left", padx=10)  # Adds spacing

            
            # Header Label (right side)
            header_label = ttk.Label(
                logo_text_frame,
                text="High Horizons Learning Center",
                font=("Arial", 20, "bold"),
                foreground="white",
                background="#0f1074"
            )
            header_label.pack(side="left", padx=10)  # Adds spacing between logo and text

            
        
            sub_header_frame = tk.Frame(profile_window, bg="#D32F2F")
            sub_header_frame.place(x=0, y=60, width=900, height=30)
            ttk.Label(sub_header_frame, text="S.Y 2022 - 2023", font=("Arial", 14, "bold"), foreground="white", background="#D32F2F").pack(pady=2)

           # Profile Picture
            picture_frame = tk.Frame(profile_window, bg="#ffffff", highlightbackground="#000", highlightthickness=2)
            picture_frame.place(x=20, y=120, width=210, height=250)
            
            if teacher_data[6]:
                image = Image.open(io.BytesIO(teacher_data[6]))
                image = image.resize((220, 250))
                photo = ImageTk.PhotoImage(image)
                picture_label = tk.Label(picture_frame, image=photo, bg="#ffffff")
                picture_label.image = photo
                picture_label.pack()
            else:
                tk.Label(picture_frame, text="No Image", bg="#ffffff").pack()

            
            # Button Frame (Placed Under Profile Picture)
            # Button Frame (Placed Under Profile Picture)
            button_frame = tk.Frame(profile_window, bg="#F5F5DC", highlightbackground="#000", highlightthickness=2, relief="solid", padx=10, pady=5)
            button_frame.place(x=20, y=370, width=210, height=50)  # Adjust y to place below the picture

            update_button = ttk.Button(button_frame, text="Update", command=lambda: update_teacher(teacher_id, profile_window))
            update_button.pack(side=tk.LEFT, padx=5)

            delete_button = ttk.Button(button_frame, text="Delete", command=lambda: confirm_delete(teacher_id, profile_window))
            delete_button.pack(side=tk.LEFT, padx=5)
                

            # Name Banner (Full Width)
            name_banner = tk.Label(profile_window, text=teacher_data[2].upper(), font=("Arial", 18, "bold"), fg="white", bg="#1565C0", padx=20, pady=5)
            name_banner.place(x=250, y=120, width=600)

            # Information Section
            info_frame = tk.Frame(profile_window, bg="#F5F5DC", highlightbackground="#000", highlightthickness=2)
            info_frame.place(x=250, y=170, width=600, height=200)
            
            details = [
                ("ID Number:", teacher_data[1]),
                ("Email:", teacher_data[5]),
                ("Contact No:", teacher_data[4]),
                ("Home Address:", teacher_data[3])
            ]

            for i, (label, value) in enumerate(details):
                tk.Label(info_frame, text=label, font=("Arial", 12, "bold"), bg="#F5F5DC").grid(row=i, column=0, sticky="w", padx=10, pady=5)
                tk.Label(info_frame, text=value, font=("Arial", 12), bg="#F5F5DC", wraplength=450).grid(row=i, column=1, sticky="w", padx=10, pady=5)

                

            # Footer (Full Width)
            footer_frame = tk.Frame(profile_window, bg="#FFC107")
            footer_frame.place(x=0, y=450, width=900, height=50)
            tk.Label(footer_frame, text="Teacher Profile", font=("Arial", 16, "bold"), fg="black", bg="#FFC107").pack(pady=10)

            profile_window.mainloop()


    def confirm_delete(teacher_id, profile_window):
        if messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this teacher's profile?"):
            # Call the delete_teacher function if confirmed
            delete_teacher(teacher_id, profile_window)

    def update_teacher(teacher_id, profile_window):
        # Fetch current teacher data
        cursor.execute("SELECT * FROM teacher WHERE ID = %s", (teacher_id,))
        teacher_data = cursor.fetchone()

        # Create update window
        update_window = tk.Toplevel()
        title_text = f"Update Teacher - {teacher_data[2]}"
        update_window.title(title_text)

        # Calculate window width based on title text
        default_font = font.nametofont("TkDefaultFont")  # Get default font
        text_width = default_font.measure(title_text) + 50  # Measure title width + padding

        window_height = 300  # Set a reasonable height

        # Center the window
        screen_width = update_window.winfo_screenwidth()
        screen_height = update_window.winfo_screenheight()
        x_position = (screen_width // 2) - (text_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        # Apply geometry
        update_window.geometry(f"{text_width}x{window_height}+{x_position}+{y_position}")

        # Disable maximize button
        update_window.resizable(False, False)  # Prevents resizing
        update_window.attributes('-toolwindow', True)  # Optional: Hides maximize button on Windows

        # Create input fields
        tk.Label(update_window, text="ID_NO:").grid(row=0, column=0, padx=10, pady=5)
        id_no_entry = tk.Entry(update_window)
        id_no_entry.insert(0, teacher_data[1])
        id_no_entry.grid(row=0, column=1)

        tk.Label(update_window, text="Name:").grid(row=1, column=0, padx=10, pady=5)
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, teacher_data[2])
        name_entry.grid(row=1, column=1)

        tk.Label(update_window, text="Address:").grid(row=2, column=0, padx=10, pady=5)
        address_entry = tk.Entry(update_window)
        address_entry.insert(0, teacher_data[3])
        address_entry.grid(row=2, column=1)

        tk.Label(update_window, text="Contact:").grid(row=3, column=0, padx=10, pady=5)
        contact_entry = tk.Entry(update_window)
        contact_entry.insert(0, teacher_data[4])
        contact_entry.grid(row=3, column=1)

        tk.Label(update_window, text="Email:").grid(row=4, column=0, padx=10, pady=5)
        email_entry = tk.Entry(update_window)
        email_entry.insert(0, teacher_data[5])
        email_entry.grid(row=4, column=1)

        # Picture
        tk.Label(update_window, text="Picture:").grid(row=5, column=0, padx=10, pady=5)
        picture_label = tk.Label(update_window)
        picture_label.grid(row=5, column=1)
        
        if teacher_data[6]:  # If a picture exists
            image = Image.open(io.BytesIO(teacher_data[6]))
            image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            picture_label.config(image=photo)
            picture_label.image = photo
            picture_label.image_data = teacher_data[6]
        else:
            picture_label.config(text="No picture available")

        # Frame to hold buttons
        button_frame = tk.Frame(update_window)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")  # Span all columns

        # Change Picture Button
        picture_button = tk.Button(button_frame, text="Change Picture", font=("Arial", 10, "bold"), 
                                bg="#0f1074", fg="white", relief="raised", bd=3, cursor="hand2",
                                command=lambda: select_picture(picture_label))
        picture_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)  # Expands to fill available space

        # Update Button
        update_button = tk.Button(button_frame, text="Update", font=("Arial", 12, "bold"), 
                                bg="#27ae60", fg="white", relief="raised", bd=3, cursor="hand2",
                                command=lambda: perform_update(
                                    teacher_id, id_no_entry, name_entry, address_entry, contact_entry, email_entry, 
                                    picture_label, update_window, profile_window))
        update_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)  # Expands to fill available space

        # Ensure window resizes properly
        update_window.grid_columnconfigure(0, weight=1)
        update_window.grid_columnconfigure(1, weight=1)
        update_window.grid_columnconfigure(2, weight=1)

    def perform_update(teacher_id, id_no_entry, name_entry, address_entry, contact_entry, email_entry, picture_label, update_window, profile_window):
        id_no = id_no_entry.get()
        name = name_entry.get()
        address = address_entry.get()
        contact = contact_entry.get()
        email = email_entry.get()

        # Handle image data conversion to binary
        img_binary = picture_label.image_data if hasattr(picture_label, 'image_data') else None

        if id_no and name and address and contact and email:
            try:
                cursor.execute(
                    "UPDATE teacher SET ID_NO = %s, Name = %s, Address = %s, Contact = %s, Email = %s, Picture = %s WHERE ID = %s",
                    (id_no, name, address, contact, email, img_binary, teacher_id)
                )
                connection.commit()
                messagebox.showinfo("Success", "Teacher updated successfully")
                update_window.destroy()
                profile_window.destroy()
                load_teacher_data(teacher_tree)  # Refresh the Treeview
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error updating teacher: {err}")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def delete_teacher(teacher_id, profile_window):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this teacher?"):
            try:
                cursor.execute("DELETE FROM teacher WHERE ID = %s", (teacher_id,))
                connection.commit()
                messagebox.showinfo("Success", "Teacher deleted successfully")
                profile_window.destroy()
                load_teacher_data(teacher_tree)  # Refresh the Treeview after deletion
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error deleting teacher: {err}")

    
    def open_subject_window():
        subject_window = tk.Toplevel(main_root)
        subject_window.title("Add Subject")
        subject_window.resizable(False, False)

        window_width = 900
        window_height = 600
        screen_width = subject_window.winfo_screenwidth()
        screen_height = subject_window.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        subject_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        subject_frame = tk.Frame(subject_window, bg="#ecf0f1", padx=20, pady=20)
        subject_frame.pack(fill="both", expand=True)

         # Create a frame for the title (for the background box)
        title_frame = tk.Frame(subject_frame, bg="#0f1074", height=100)  # Light blue background
        title_frame.pack(fill="x", side="top" )
        title_frame.pack_propagate(False)  # Prevent resizing based on child widgets


        # Add an icon
        icon_image = PhotoImage(file="images/subs.png")  # Replace with the actual path to your icon
        icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
        icon_label.image = icon_image  # Keep a reference to avoid garbage collection
        icon_label.pack(side="left", padx=10)

        # Title Label
        title_label = tk.Label(
            title_frame,
            text="Subject Input Form",
            font=("Arial", 30, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10)

        input_frame = tk.Frame(subject_frame, bg="#ecf0f1")
        input_frame.pack(fill="x")


        # Use grid layout for horizontal alignment
        tk.Label(input_frame, text="Descriptive Title:", font=('Arial', 14), bg="#ecf0f1").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        global subject_title_entry
        subject_title_entry = tk.Entry(input_frame, font=('Arial', 12))
        subject_title_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        tk.Label(input_frame, text="Type:", font=('Arial', 14), bg="#ecf0f1").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        global subject_type_combo
        subject_type_combo = ttk.Combobox(input_frame, values=["Core Subject", "Co-Curricular"], state='readonly', font=('Arial', 12))
        subject_type_combo.grid(row=1, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        tk.Label(input_frame, text="Grade Level:", font=('Arial', 14), bg="#ecf0f1").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        global subject_grade_combo
        subject_grade_combo = ttk.Combobox(input_frame, values=["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"], state='readonly', font=('Arial', 12))
        subject_grade_combo.grid(row=2, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        input_frame.columnconfigure(1, weight=1)  # Allow input fields to expand
    
    # Styled Submit Button with adjusted size
        submit_button = tk.Button(
            subject_frame, text="Submit", command=insert_subject, font=('Arial', 14, 'bold'),
            bg="#27ae60", fg="white", padx=20, pady=10, relief="raised", bd=3,
            width=15, height=2  # Adjusted to a comfortable size for horizontal layout
        )
        submit_button.pack(pady=(20, 5))  # Added top padding to raise the button

         # Hide the submit button initially
        submit_button.pack_forget()

        # Bind Enter key to trigger the Submit button
        subject_window.bind('<Return>', lambda event: insert_subject())

            # Treeview Table
        subject_columns = ["ID", "Descriptive_Title", "Type", "Grade_Level"]
        global subject_tree
        subject_tree = ttk.Treeview(subject_frame, columns=subject_columns, show="headings", height=15)

        for col in subject_columns:
            subject_tree.heading(col, text=col)
            subject_tree.column(col, width=200, anchor='center')

        subject_tree.pack(expand=True, fill='both', padx=20, pady=10)

            # Scrollbars
        vsb = ttk.Scrollbar(subject_frame, orient="vertical", command=subject_tree.yview)
        hsb = ttk.Scrollbar(subject_frame, orient="horizontal", command=subject_tree.xview)
        subject_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')

        # Initially display data in the Treeview
        load_subject_data()
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
    new_user_icon = load_icon("images/newuser.png")
    admissions_icon = load_icon("images/admission.png")
    finance_icon = load_icon("images/finance.png")
    interviews_icon = load_icon("images/interview.png")
    admitted_icon = load_icon("images/admitted.png")
    updates_icon = load_icon("images/updates.png")
    scheduling_icon = load_icon("images/schedule.png")
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
        ("New User", new_user_icon, show_new_user_panel), 
        ("Admissions", admissions_icon, show_admissions_panel),
        ("Finance", finance_icon, show_cashier_panel),
        ("Interviews", interviews_icon, show_interview_panel),
        ("Admitted", admitted_icon, show_admitted_panel),
        ("Updates", updates_icon, show_updates_panel),
        ("Scheduling", scheduling_icon, show_scheduling_panel),

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

#====================================================== NEW USER PANEL ==============================================
    def create_new_user_frame():
        """Creates a frame for user registration with a horizontal form layout and styled table."""
        global new_user_frame, user_table

        # Main User Frame
        new_user_frame = tk.Frame(content_frame, bg="#ecf0f1")
        new_user_frame.grid(row=0, column=0, sticky="nsew")

        # Title Section
        create_title_section(new_user_frame)

        # Horizontal Input Section
        create_horizontal_input_section(new_user_frame)

        # Search Section
        search_frame = tk.Frame(new_user_frame, bg="#ecf0f1")
        search_frame.pack(pady=10, padx=10, fill="x")

        search_entry = tk.Entry(search_frame, width=30, font=("Arial", 12), bd=2, relief="solid")
        search_entry.pack(side="left", padx=5)

        def search_users():
            query = search_entry.get().lower()
            if not query:
                load_users()
                return

            for row in user_table.get_children():
                user_table.delete(row)
            
            ensure_connection()
            cursor.execute("SELECT userid, username, pass, permission FROM logininfo WHERE permission IN ('admin', 'registrar', 'cashier', 'interviewer', 'teacher')")
            all_users = cursor.fetchall()

            matching_users = []
            for user in all_users:
                if any(query in str(value).lower() for value in user):
                    matching_users.append(user)
            
            for idx, user in enumerate(matching_users):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                user_table.insert("", "end", values=user, tags=(tag,))

        # Styled Search Button
        search_button = tk.Button(
            search_frame,
            text="Search",
            command=search_users,
            font=("Arial", 12, "bold"),
            bg="#3498db",  # Background color
            fg="#ffffff",  # Text color
            activebackground="#2980b9",  # Background color when clicked
            activeforeground="#ffffff",  # Text color when clicked
            bd=0,  # Remove border
            padx=15,  # Horizontal padding
            pady=5,  # Vertical padding
            relief="flat",  # Flat appearance
            cursor="hand2"  # Change cursor to a hand on hover
        )
        search_button.pack(side="left", padx=5)

        # Hover Effects for Search Button
        def on_hover(event):
            search_button.config(bg="#2980b9")  # Darker background on hover

        def on_leave(event):
            search_button.config(bg="#3498db")  # Restore original background

        search_button.bind("<Enter>", on_hover)
        search_button.bind("<Leave>", on_leave)

        # Bind Enter key to search
        search_entry.bind("<Return>", lambda event: search_users())

        # Users Table Section
        create_table_section(new_user_frame)

        # Apply Styling
        style_treeview()

        # Load Existing Users
        load_users()

    def show_new_user_panel():
        new_user_frame.tkraise()
        
        # Clear previous input fields
        clear_input_fields()

        # Create a search bar frame
        search_frame = tk.Frame(new_user_frame)
        search_frame.pack(pady=10, padx=10, fill="x")

        # Add search entry field
        search_entry = tk.Entry(search_frame, width=30, font=("Arial", 12))
        search_entry.pack(side="left", padx=5)

        # Function to perform search
        def search_users():
            query = search_entry.get().lower()
            for row in user_table.get_children():
                user_table.delete(row)
            
            # Ensure database connection is active
            ensure_connection()
            cursor.execute("SELECT userid, username, permission FROM logininfo WHERE permission IN ('admin', 'registrar', 'cashier', 'interviewer', 'teacher')")
            users = cursor.fetchall()

            # Filter users
            for user in users:
                if any(query in str(value).lower() for value in user):
                    user_table.insert("", "end", values=user)

        # Add search button
        search_button = tk.Button(search_frame, text="Search", command=search_users)
        search_button.pack(side="left", padx=5)

        # Reload users list
        load_users()



    def create_title_section(parent):
        """Creates the title section with an icon and title."""
        title_frame = tk.Frame(parent, bg="#0f1074", height=100)
        title_frame.pack(fill="x", side="top")
        title_frame.pack_propagate(False)

        # Persist the image to avoid garbage collection
        parent.icon_image = tk.PhotoImage(file="images/user.png")  # Store in parent
        icon_label = tk.Label(title_frame, image=parent.icon_image, bg="#0f1074")
        icon_label.pack(side="left", padx=15, pady=10)

        # Title Label
        title_label = tk.Label(
            title_frame,
            text="Register New User",
            font=("Arial", 28, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10)

    def create_horizontal_input_section(parent):
        """Creates a horizontal form layout for username, password, role, and register button."""
        input_frame = tk.Frame(parent, bg="#ecf0f1", padx=20, pady=10)
        input_frame.pack(fill="x", padx=20, pady=10)

        # Username
        tk.Label(input_frame, text="Username:", font=('Arial', 14), bg="#ecf0f1").pack(side="left", padx=10)
        username_entry = tk.Entry(input_frame, font=('Arial', 14), width=15)
        username_entry.pack(side="left", padx=10)

        # Password
        tk.Label(input_frame, text="Password:", font=('Arial', 14), bg="#ecf0f1").pack(side="left", padx=10)
        password_entry = tk.Entry(input_frame, show="*", font=('Arial', 14), width=15)
        password_entry.pack(side="left", padx=10)

        # Role Selection
        tk.Label(input_frame, text="Role:", font=('Arial', 14), bg="#ecf0f1").pack(side="left", padx=10)
        role_combo = ttk.Combobox(input_frame, values=["Registrar", "Cashier", "Interviewer", "Teacher"], state="readonly", font=('Arial', 14), width=12)
        role_combo.pack(side="left", padx=10)
        role_combo.set("Registrar")  # Default selection

        # Register Button
        submit_button = tk.Button(
            input_frame, text="Register", 
            command=lambda: register_user(username_entry, password_entry, role_combo),
            font=('Arial', 14), bg="#27ae60", fg="#ffffff", height=1, width=12
        )
        submit_button.pack(side="left", padx=10)


    def create_table_section(parent):
        """Creates the section displaying registered users (without title)."""
        global user_table

        table_frame = tk.Frame(parent, bg="#ecf0f1", padx=15, pady=10)
        table_frame.pack(fill="both", expand=True)

        # User Table
        user_table = ttk.Treeview(table_frame, columns=("ID", "Username", "Password", "Role", "Last Log-in"), show="headings")
        user_table.pack(fill="both", expand=True, padx=5, pady=5)

        # Define Table Headings
        for col in ("ID", "Username", "Password", "Role", "Last Log-in"):
            user_table.heading(col, text=col)
            user_table.column(col, width=120 if col == "Username" else 80, anchor="center")
        user_table.bind("<Double-1>", on_user_double_click)

    def style_treeview():
        """Applies styling to the Treeview widget."""
        style = ttk.Style()
        style.theme_use("clam")

        # General Treeview Styling
        style.configure("Treeview", rowheight=25, font=('Arial', 12))
        style.map("Treeview", background=[("selected", "#436060")], foreground=[("selected", "white")])

        # Apply striped rows
        user_table.tag_configure("evenrow", background="#ffbb00")
        user_table.tag_configure("oddrow", background="#F5F5DC")


    def register_user(username_entry, password_entry, role_combo):
        """Handles user registration by inserting data into the database."""
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role = role_combo.get().strip()

        if not username or not password:
            messagebox.showerror("Input Error", "Username and Password are required.")
            return

        try:
            cursor.execute("INSERT INTO logininfo (username, pass, permission) VALUES (%s, %s, %s)", (username, password, role))
            connection.commit()
            messagebox.showinfo("Success", "User registered successfully.")

            # Clear fields after registration
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            role_combo.set("Admin")  # Reset role to default

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Refresh user table after registering
        load_users()


    def load_users():
        """Loads users into the table from the database with alternating row colors."""
        for row in user_table.get_children():
            user_table.delete(row)

        ensure_connection()
        connection.commit()

        cursor.execute("SELECT userid, username, pass, permission, last_log FROM logininfo WHERE permission IN ('Admin', 'Registrar', 'Cashier', 'Interviewer', 'Teacher')")
        
        for idx, user in enumerate(cursor.fetchall()):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            user_table.insert("", "end", values=user, tags=(tag,))

    def open_change_password_window(username):
        """Opens a well-designed password change window centered on the screen."""
        def update_password():
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                return

            try:
                cursor.execute("UPDATE logininfo SET pass = %s WHERE username = %s", (new_password, username))
                connection.commit()
                messagebox.showinfo("Success", "Password updated successfully.")
                password_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        def delete_user():
            """Deletes the user from the database."""
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user? This action cannot be undone.")
            if confirm:
                try:
                    cursor.execute("DELETE FROM logininfo WHERE username = %s", (username,))
                    connection.commit()
                    messagebox.showinfo("Success", f"User '{username}' deleted successfully.")
                    password_window.destroy()
                    load_users()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")

        # Create the window
        password_window = tk.Toplevel()
        password_window.title("🔒 Change Password")
        
        # Define window size (adjusted height)
        window_width = 350
        window_height = 400  # Increased height

        # Center the window immediately
        screen_width = password_window.winfo_screenwidth()
        screen_height = password_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        password_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        password_window.resizable(False, False)
        password_window.attributes('-toolwindow', True)  # Removes minimize and maximize buttons

        # Custom Font Styling
        title_font = tkFont.Font(family="Arial", size=14, weight="bold")
        label_font = tkFont.Font(family="Arial", size=12)
        entry_font = tkFont.Font(family="Arial", size=11)

        # Frame Styling
        frame = tk.Frame(password_window, bg="#f4f4f4", padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Title Label
        tk.Label(frame, text="🔒 Change Your Password", font=title_font, bg="#f4f4f4", fg="#333").pack(pady=(5, 10))

        # Username Field (Disabled)
        tk.Label(frame, text="Username:", font=label_font, bg="#f4f4f4").pack(anchor="w", pady=(0, 2))
        username_entry = tk.Entry(frame, font=entry_font, bd=2, relief="solid", bg="white")
        username_entry.pack(fill="x", ipady=3, pady=(0, 8))
        username_entry.insert(0, username)
        username_entry.config(state='disabled')

        # New Password Field
        tk.Label(frame, text="New Password:", font=label_font, bg="#f4f4f4").pack(anchor="w", pady=(0, 2))
        new_password_entry = tk.Entry(frame, font=entry_font, bd=2, relief="solid", show="*")
        new_password_entry.pack(fill="x", ipady=3, pady=(0, 8))

        # Confirm Password Field
        tk.Label(frame, text="Confirm Password:", font=label_font, bg="#f4f4f4").pack(anchor="w", pady=(0, 2))
        confirm_password_entry = tk.Entry(frame, font=entry_font, bd=2, relief="solid", show="*")
        confirm_password_entry.pack(fill="x", ipady=3, pady=(0, 8))

        # Change Password Button (Larger & Fully Visible)
        change_password_button = tk.Button(
            frame, text="Change Password", font=label_font, bg="#27ae60", fg="white",
            activebackground="#2ecc71", activeforeground="white",
            relief="raised", bd=3, height=2, width=22,  # Bigger button!
            command=update_password
        )
        change_password_button.pack(pady=(25, 5))  # Increased bottom padding

        # Delete User Button
        delete_user_button = tk.Button(
            frame, text="DELETE", font=label_font, bg="#e74c3c", fg="white",  # Red color for delete button
            activebackground="#c0392b", activeforeground="white",
            relief="raised", bd=3, height=1, width=8,  
            command=delete_user
        )
        delete_user_button.pack(pady=(0, 0))

        # Hover Effect for Change Password Button
        def on_hover(event):
            change_password_button.config(bg="#2ecc71")

        def on_leave(event):
            change_password_button.config(bg="#27ae60")

        change_password_button.bind("<Enter>", on_hover)
        change_password_button.bind("<Leave>", on_leave)

        # Hover Effect for Delete User Button
        def on_hover_delete(event):
            delete_user_button.config(bg="#c0392b")

        def on_leave_delete(event):
            delete_user_button.config(bg="#e74c3c")

        delete_user_button.bind("<Enter>", on_hover_delete)
        delete_user_button.bind("<Leave>", on_leave_delete)


    def on_user_double_click(event):
        """Handles double-clicking a user row in the table."""
        selected_item = user_table.selection()
        if selected_item:
            item = user_table.item(selected_item, 'values')
            username = item[1]  # Assuming username is in the second column
            open_change_password_window(username)

    def show_new_user_panel():
        global new_user_frame
        clear_input_fields()
        new_user_frame.tkraise()
        load_users()


    

#=======================================================ADMISSION PANEL==============================================
    def create_admission_view():
        global admission_frame, tree_admission, details_frame_admission

        admission_frame = tk.Frame(content_frame, bg="white")
        admission_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights - 4:1 ratio for 80%-20% split
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        admission_frame.columnconfigure(0, weight=4)  # 80% for table
        admission_frame.columnconfigure(1, weight=1)  # 20% for details
        admission_frame.rowconfigure(0, weight=0)     # Title (fixed height)
        admission_frame.rowconfigure(1, weight=0)     # Buttons (fixed height)
        admission_frame.rowconfigure(2, weight=1)     # Content (expands)

        # Title frame with fixed 100px height
        title_frame = tk.Frame(admission_frame, bg="#0f1074", height=100)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        title_frame.grid_propagate(False)

        # Add icon
        try:
            icon_image = PhotoImage(file="images/registration.png")
            icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
            icon_label.image = icon_image
            icon_label.pack(side="left", padx=(20, 10))
        except:
            icon_placeholder = tk.Label(title_frame, text="🎓", bg="#0f1074", fg="white", font=("Arial", 24))
            icon_placeholder.pack(side="left", padx=(20, 10))

        # Title label
        title_label = tk.Label(
            title_frame,
            text="Pending Admissions",
            font=("Arial", 28, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10, pady=20)

        # Button Frame with top padding
        button_frame = tk.Frame(admission_frame, bg="white", height=50)  # Increased height for padding
        button_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 5))  # 10px top padding
        button_frame.grid_propagate(False)

        # Container frame for buttons to center them vertically
        button_container = tk.Frame(button_frame, bg="white")
        button_container.pack(pady=5)  # Centers buttons vertically in the frame

        # Styled Refresh Button
        refresh_button = tk.Button(
            button_container,
            text="Refresh",
            command=load_admission_data,
            width=12,
            font=('Arial', 10, 'bold'),
            bg="#3498db",
            fg="white",
            relief=tk.RAISED,
            bd=2
        )
        refresh_button.pack(side="left", padx=5)

        # Styled Calendar Button
        calendar_button = tk.Button(
            button_container,
            text="Calendar",
            command=show_calendar_app,
            width=12,
            font=('Arial', 10, 'bold'),
            bg="#2ecc71",
            fg="white",
            relief=tk.RAISED,
            bd=2
        )
        calendar_button.pack(side="left", padx=5)

        # Treeview Frame (80% width)
        tree_frame = tk.Frame(admission_frame, bg="white")
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Treeview setup with styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Admission.Treeview",
            rowheight=25,
            font=('Arial', 11),
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#000000"
        )
        style.configure("Admission.Treeview.Heading",
            font=('Arial', 11, 'bold'),
            background="#9f0000",
            foreground="white"
        )
        style.map("Admission.Treeview",
            background=[('selected', '#436060')],
            foreground=[('selected', 'white')]
        )

        tree_columns = (
            "Student ID", "Last Name", "First Name", "Nickname", 
            "Birthday", "Age", "Gender", "Address"
        )
        
        tree_admission = ttk.Treeview(
            tree_frame, 
            columns=tree_columns, 
            show="headings", 
            height=20,
            style="Admission.Treeview"
        )

        # Configure column widths
        col_widths = {
            "Student ID": 80,
            "Last Name": 120,
            "First Name": 120,
            "Nickname": 80,
            "Birthday": 100,
            "Age": 50,
            "Gender": 70,
            "Address": 200
        }

        for col in tree_columns:
            tree_admission.heading(col, text=col)
            tree_admission.column(col, width=col_widths[col], stretch=False)

        # Add striped row styling
        tree_admission.tag_configure('oddrow', background='#F5F5DC')  # Light beige
        tree_admission.tag_configure('evenrow', background='#ffbb00')  # Gold

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_admission.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree_admission.xview)
        tree_admission.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout for treeview
        tree_admission.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Details Frame (20% width)
        details_frame_admission = tk.Frame(
            admission_frame, 
            bg="white", 
            relief=tk.RIDGE, 
            bd=2,
            width=350
        )
        details_frame_admission.grid(row=2, column=1, sticky="nsew", padx=(0, 20), pady=(0, 20))
        details_frame_admission.grid_propagate(False)

        # Scrollable details panel
        canvas = tk.Canvas(details_frame_admission, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(details_frame_admission, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Double-click event
        tree_admission.bind("<Double-1>", start_admission_edit)

        # Force layout update
        admission_frame.update_idletasks()

    def start_admission_edit(event):
        # Get the selected item
        selected_item = tree_admission.selection()
        if selected_item:
            item_data = tree_admission.item(selected_item)
            values = item_data['values']

            # Display the student details in the details frame
            display_admission_details(values)

    def display_admission_details(values):
        """Display the student details in the details frame beside the Treeview with a polished design."""
        # Clear previous details
        for widget in details_frame_admission.winfo_children():
            widget.destroy()

        # Create a canvas and scrollbar for scrolling content
        canvas = tk.Canvas(details_frame_admission, bg="#f8f9fa", highlightthickness=0)
        scrollbar = tk.Scrollbar(details_frame_admission, orient=tk.VERTICAL, command=canvas.yview)

        # Add the scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame within the canvas
        scrollable_frame = tk.Frame(canvas, bg="#f8f9fa")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Define labels for the fields
        labels = [
            "Student ID", "Last Name", "First Name", "Nickname", "Birthday", "Age", "Gender", 
            "Address", "Father", "Father's Age", "Father's Email", "Father's Contact No", 
            "Father's Occupation", "Father's Company Name", "Mother's Name", "Mother's Age", 
            "Mother's Email", "Mother's Contact No", "Mother's Occupation", "Mother's Company Name", "Parent Status"
        ]

        # Add a title
        title_label = tk.Label(scrollable_frame, text="Admission Details", bg="#f8f9fa", font=('Arial', 14, 'bold'), fg="#34495e")
        title_label.pack(pady=(10, 15))

        # Create styled "cards" for each field
        for label, value in zip(labels, values):
            # Card-style container
            card_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RIDGE, bd=2)
            card_frame.pack(fill=tk.X, padx=10, pady=5)

            # Label for the field name
            label_widget = tk.Label(card_frame, text=f"{label}:", bg="white", font=('Arial', 10, 'bold'), fg="#2c3e50", width=10, anchor="w")
            label_widget.pack(side=tk.LEFT, padx=10, pady=5)

            # Value for the field
            value_widget = tk.Text(card_frame, height=1, width=19, bg="white", font=('Arial', 10), fg="#7f8c8d", wrap="word", relief=tk.FLAT)
            value_widget.insert("1.0", value)
            value_widget.config(state="disabled")  # Make the text box read-only
            value_widget.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5, expand=True)

        def open_maximized_window():
            # Create a new Toplevel window
            maximize_window = tk.Toplevel()
            maximize_window.title("Detailed Information")
            maximize_window.configure(bg="white")  # Set background color for consistency

            # Calculate the required width dynamically based on the longest label + value
            max_label_length = max(len(label) for label in labels)
            max_value_length = max(len(str(value)) for value in values)
            char_width = 8  # Approximate width of a character in pixels
            padding = 100  # Additional padding for spacing
            calculated_width = (max_label_length + max_value_length) * char_width + padding

            # Ensure the width does not exceed the screen width
            screen_width = maximize_window.winfo_screenwidth()
            screen_height = maximize_window.winfo_screenheight()
            width = min(calculated_width, screen_width - 50)  # Leave a 50px margin from screen edges
            height = 600  # Fixed height for the window

            # Center the window on the screen
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)

            # Set the geometry of the window with the calculated width and fixed height
            maximize_window.geometry(f"{width}x{height}+{x}+{y}")

            # Add a scrollbar and canvas in the maximize window
            max_canvas = tk.Canvas(maximize_window, bg="white", highlightthickness=0)
            max_scrollbar = tk.Scrollbar(maximize_window, orient=tk.VERTICAL, command=max_canvas.yview)

            max_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            max_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            max_scrollable_frame = tk.Frame(max_canvas, bg="white")
            max_scrollable_frame.bind(
                "<Configure>",
                lambda e: max_canvas.configure(scrollregion=max_canvas.bbox("all"))
            )
            max_canvas.create_window((0, 0), window=max_scrollable_frame, anchor="nw")
            max_canvas.configure(yscrollcommand=max_scrollbar.set)

            # Populate the maximize window with the same data
            for label, value in zip(labels, values):
                frame = tk.Frame(max_scrollable_frame, bg="white", relief=tk.GROOVE, bd=1)
                frame.pack(fill=tk.X, pady=5)

                label_widget = tk.Label(frame, text=f"{label}: ", bg="white", font=('Arial', 12, 'bold'),anchor="w",width=16)
                label_widget.pack(side=tk.LEFT, padx=(5, 2))
                
                value_widget = tk.Label(frame, text=value,width=27, bg="white", font=('Arial', 10))
                value_widget.pack(side=tk.LEFT, padx=(0, 5))

            # Add a Close button for the new window
            close_button = tk.Button(max_scrollable_frame, text="Close", command=maximize_window.destroy,
                                    bg="red", fg="white", font=('Arial', 12, 'bold'))
            close_button.pack(pady=10)

        # Create a frame for buttons in a horizontal layout
        button_frame = tk.Frame(scrollable_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=20)

        # Define button dimensions
        button_width = 10  # Adjust the width of the button (characters)
        button_height = 1  # Adjust the height of the button (lines)

        # Maximize button
        maximize_button = tk.Button(
            button_frame, text="Maximize", command=open_maximized_window,
            bg="blue", fg="white", font=('Arial', 9, 'bold'), relief=tk.RAISED,
            width=button_width, height=button_height
        )
        maximize_button.pack(side=tk.LEFT, padx=5)

        # Schedule button
        schedule_button = tk.Button(
            button_frame, text="Schedule", command=lambda: open_schedule_window(values[0]),
            bg="sky blue", fg="white", font=('Arial', 9, 'bold'), relief=tk.RAISED,
            width=button_width, height=button_height
        )
        schedule_button.pack(side=tk.LEFT, padx=5)

        # Clear Details button
        clear_button = tk.Button(
            button_frame, text="Clear Details", command=lambda: clear_admission_details(),
            bg="red", fg="white", font=('Arial', 9, 'bold'), relief=tk.RAISED,
            width=button_width, height=button_height
        )
        clear_button.pack(side=tk.LEFT, padx=5)


    def open_schedule_window(student_id):
        global schedule_window
        schedule_window = tk.Toplevel()
        schedule_window.title("Student Schedule")
        schedule_window.configure(bg="#ecf0f1")

        # Set initial size
        width = 500
        height = 400
        schedule_window.geometry(f"{width}x{height}")

        # Center the window after rendering
        schedule_window.update_idletasks()
        x = (schedule_window.winfo_screenwidth() // 2) - (schedule_window.winfo_width() // 2)
        y = (schedule_window.winfo_screenheight() // 2) - (schedule_window.winfo_height() // 2)
        schedule_window.geometry(f"{width}x{height}+{x}+{y}")

        # 🚀 Title Bar with Styling
        title_frame = tk.Frame(schedule_window, bg="#0f1074", height=80)
        title_frame.pack(fill="x", side="top")
        title_frame.pack_propagate(False)

        # Icon (Replace 'schedule.png' with actual icon path)
        icon_image = tk.PhotoImage(file="images/scheduling.png")  
        icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
        icon_label.image = icon_image  # Keep reference to avoid garbage collection
        icon_label.pack(side="left", padx=10)

        # Title Label
        title_label = tk.Label(
            title_frame,
            text="Schedule for Student",
            font=("Arial", 24, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10)

        # Main Content Frame
        schedule_frame = tk.Frame(schedule_window, bg="#ffffff", bd=2, relief="ridge", padx=20, pady=20)
        schedule_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # 🔹 Schedule Title
        tk.Label(schedule_frame, text="Schedule Title:", font=('Arial', 12), bg="#ffffff").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        title_entry = tk.Entry(schedule_frame, font=('Arial', 12), width=30, relief="flat", bg="#ecf0f1")
        title_entry.grid(row=0, column=1, padx=5, pady=5)

        # 🔹 Schedule Date
        tk.Label(schedule_frame, text="Schedule Date:", font=('Arial', 12), bg="#ffffff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        date_entry = DateEntry(schedule_frame, font=('Arial', 12), background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_entry.grid(row=1, column=1, padx=5, pady=5)

        # 🔹 Start Time
        tk.Label(schedule_frame, text="Start Time:", font=('Arial', 12), bg="#ffffff").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        time_options = [f"{hour}:{minute:02d} {'AM' if hour < 12 else 'PM'}"
                        for hour in range(7, 18)  # From 7 AM to 5 PM
                        for minute in [0, 30]]   # Every 30 minutes
        start_time_combo = ttk.Combobox(schedule_frame, values=time_options, font=('Arial', 12), width=15, state="readonly")
        start_time_combo.grid(row=2, column=1, padx=5, pady=5)

        # 🔹 End Time
        tk.Label(schedule_frame, text="End Time:", font=('Arial', 12), bg="#ffffff").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        end_time_combo = ttk.Combobox(schedule_frame, values=time_options, font=('Arial', 12), width=15, state="readonly")
        end_time_combo.grid(row=3, column=1, padx=5, pady=5)

        # ✅ Buttons
        button_frame = tk.Frame(schedule_window, bg="#ecf0f1")
        button_frame.pack(pady=15)

        tk.Button(
            button_frame, text="Save Schedule", 
            command=lambda: submit_schedule_and_admission(student_id, title_entry.get(), date_entry.get(), start_time_combo.get(), end_time_combo.get()),
            font=('Arial', 12, 'bold'), bg="#3498db", fg="#ffffff", padx=15, pady=5
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame, text="Close", 
            command=schedule_window.destroy,
            font=('Arial', 12, 'bold'), bg="#e74c3c", fg="#ffffff", padx=15, pady=5
        ).grid(row=0, column=1, padx=10)


    def submit_schedule_and_admission(student_id, title, schedule_date, start_time, end_time):
        """Submit the scheduling data and admission data to the respective tables."""

        # Check if required fields are filled
        if not title or not schedule_date or not start_time or not end_time:
            messagebox.showwarning("Input Error", "Title, date, start time, and end time must be filled out.")
            return

        # Combine start and end time into one string (e.g., "9:00 AM - 10:30 AM")
        combined_time = f"{start_time} - {end_time}"

        # Query to get student info
        cursor.execute("""
            SELECT ID, Last_Name, First_Name, Nickname, Birthday, Age, Gender,
                Address, Fathers_Name, Fathers_Age, Fathers_Email,
                Fathers_Contact_No, Fathers_Occupation, Fathers_Company_Name,
                Mothers_Name, Mothers_Age, Mothers_Email, Mothers_Contact_No,
                Mothers_Occupation, Mothers_Company_Name, Parents_Are
            FROM admission
            WHERE ID = %s
        """, (student_id,))
        
        student_info = cursor.fetchone()

        if not student_info:
            messagebox.showwarning("Input Error", "No student found with the provided ID.")
            return

        # Unpack student information
        admission_id, last_name, first_name, nickname, birthday, age, gender, address, \
        fathers_name, fathers_age, fathers_email, fathers_contact_no, \
        fathers_occupation, fathers_company_name, mothers_name, mothers_age, \
        mothers_email, mothers_contact_no, mothers_occupation, \
        mothers_company_name, parents_are = student_info

        # Interview status
        interview_status = 'pending'
        interview_scheduled = schedule_date
        admit_name = f"{first_name} {last_name}"

        try:
            # Insert into the calendar table
            cursor.execute("""
                INSERT INTO calendar (student_id, Name, date, title, time)
                VALUES (%s, %s, %s, %s, %s)
            """, (student_id, admit_name, schedule_date, title, combined_time))

            # Insert into the admitted table
            cursor.execute("""
                INSERT INTO admitted (Admission_ID, Last_Name, First_Name, Nickname, Birthday, Age, Gender,
                                    Address, Fathers_Name, Fathers_Age, Fathers_Email,
                                    Fathers_Contact_No, Fathers_Occupation, Fathers_Company_Name,
                                    Mothers_Name, Mothers_Age, Mothers_Email, Mothers_Contact_No,
                                    Mothers_Occupation, Mothers_Company_Name, Parents_Are, interview_status, interview_scheduled)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                admission_id, last_name, first_name, nickname, birthday, age, gender,
                address, fathers_name, fathers_age, fathers_email,
                fathers_contact_no, fathers_occupation, fathers_company_name,
                mothers_name, mothers_age, mothers_email, mothers_contact_no,
                mothers_occupation, mothers_company_name, parents_are, interview_status, interview_scheduled
            ))

            # Notify success
            messagebox.showinfo("Success", "Schedule created and student record admitted successfully.")

            # Delete student from admission table
            cursor.execute("DELETE FROM admission WHERE ID = %s", (student_id,))
            connection.commit()

            load_admission_data()
            schedule_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting schedule: {err}")



    def clear_admission_details():
        """Clear the details in the details frame."""
        for widget in details_frame_admission.winfo_children():
            widget.destroy()

#======================================================INTERVIEW PANEL=====================================================================
    def create_interview_view():
        global interview_frame, tree_interview, comments_text
        global selected_student_info_frame, selected_id_label, selected_name_label
        global status_label  # Label to indicate current view

        interview_frame = tk.Frame(content_frame, bg="white")
        interview_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid for responsiveness
        interview_frame.grid_columnconfigure(0, weight=1)
        interview_frame.grid_rowconfigure(1, weight=1)

        # Title Frame (Header)
        title_frame = tk.Frame(interview_frame, bg="#0f1074", height=100)
        title_frame.pack(fill="x", side="top")
        title_frame.pack_propagate(False)

        # Icon
        icon_image = PhotoImage(file="images/inter.png")
        icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
        icon_label.image = icon_image  # Prevent garbage collection
        icon_label.pack(side="left", padx=10)

        # Title Label
        title_label = tk.Label(
            title_frame,
            text="Interview Management",
            font=("Arial", 28, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10)

        # Status Label
        status_label = tk.Label(interview_frame, text="Showing: Pending Interviews",
                                font=("Arial", 14, "bold"), bg="white", fg="black")
        status_label.pack(anchor="w", padx=20, pady=(10, 5))

                # Filter Buttons Frame
        button_frame = tk.Frame(interview_frame, bg="white")
        button_frame.pack(fill="x", padx=20, pady=5)

        # Filter Buttons
        pending_button = tk.Button(button_frame, text="Show Pending",
                                command=lambda: load_interview_data("pending"),
                                font=('Arial', 11, 'bold'), bg="#f39c12", fg="white", width=12)
        pending_button.pack(side="left", padx=5)

        accepted_button = tk.Button(button_frame, text="Show Accepted",
                                    command=lambda: load_interview_data("done"),
                                    font=('Arial', 11, 'bold'), bg="#27ae60", fg="white", width=12)
        accepted_button.pack(side="left", padx=5)

        rejected_button = tk.Button(button_frame, text="Show Rejected",
                                    command=lambda: load_interview_data("rejected"),
                                    font=('Arial', 11, 'bold'), bg="#e74c3c", fg="white", width=12)
        rejected_button.pack(side="left", padx=5)

        refresh_button_interviews = tk.Button(button_frame, text="Refresh",
                                            command=lambda: load_interview_data("pending"),
                                            font=('Arial', 11, 'bold'), bg="#3498db", fg="white", width=12)
        refresh_button_interviews.pack(side="left", padx=5)

        # Calendar Button
        calendar_button = tk.Button(button_frame, text="Calendar",
                                    command=show_calendar_app,  
                                    font=('Arial', 11, 'bold'), bg="#8e44ad", fg="white", width=12)
        calendar_button.pack(side="left", padx=5)


            # Treeview Frame (For Responsiveness)
        tree_frame = tk.Frame(interview_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        # Treeview Columns
        tree_columns = ("Admission ID", "Last Name", "First Name", "Nickname",
                        "Gender", "Father's Name", "Mother's Name", "Interview Scheduled")

        tree_interview = ttk.Treeview(
            tree_frame, columns=tree_columns, show="headings", 
            yscrollcommand=vsb.set, xscrollcommand=hsb.set
        )

        for col in tree_columns:
            tree_interview.heading(col, text=col)
            tree_interview.column(col, anchor="center")

        # Configure scrollbars to work with treeview
        vsb.config(command=tree_interview.yview)
        hsb.config(command=tree_interview.xview)

        # Use grid() for proper alignment
        tree_interview.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Ensure grid resizes properly
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Load interview data initially with "pending"
        load_interview_data("pending")

        tree_interview.bind("<Double-1>", on_student_double_click)

        # Bind window resize event to update column width
        interview_frame.bind("<Configure>", lambda event: adjust_treeview_columns(tree_interview))


    def adjust_treeview_columns(tree):
        """ Dynamically adjust Treeview column width based on window size. """
        total_width = tree.winfo_width()
        num_columns = len(tree["columns"])

        for col in tree["columns"]:
            tree.column(col, width=int(total_width / num_columns) - 10)  # Distribute width evenly


    def on_student_double_click(event):
        selected_item = tree_interview.selection()
        if selected_item:
            admission_id = tree_interview.item(selected_item)['values'][0]
            show_interview_profile(admission_id)

    def show_interview_profile(admission_id):
        global interview_profile_window
        interview_profile_window = tk.Toplevel()
        interview_profile_window.title("Interview Profile")
        interview_profile_window.configure(bg="#ecf0f1")
        
        # Set initial size
        width = 580
        height = 510
        interview_profile_window.geometry(f"{width}x{height}")
        
        # Center the window after rendering
        interview_profile_window.update_idletasks()
        x = (interview_profile_window.winfo_screenwidth() // 2) - (interview_profile_window.winfo_width() // 2)
        y = (interview_profile_window.winfo_screenheight() // 2) - (interview_profile_window.winfo_height() // 2)
        interview_profile_window.geometry(f"{width}x{height}+{x}+{y}")
        
          # Create a frame for the title (background box)
        title_frame = tk.Frame(interview_profile_window, bg="#0f1074", height=80)
        title_frame.pack(fill="x", side="top")
        title_frame.pack_propagate(False)  # Prevent resizing
        
        # Add an icon (ensure 'inter.png' exists in your project)
        icon_image = tk.PhotoImage(file="images/inter.png")  
        icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
        icon_label.image = icon_image  # Keep reference to avoid garbage collection
        icon_label.pack(side="left", padx=10)
        
        # Title Label
        title_label = tk.Label(
            title_frame,
            text="Interview Profile",
            font=("Arial", 24, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10)
        
        cursor.execute("SELECT Admission_ID, Last_Name, First_Name, Nickname, comments FROM admitted WHERE Admission_ID = %s", (admission_id,))
        student_info = cursor.fetchone()
        
        if student_info:
            details_frame = tk.Frame(interview_profile_window, bg="#ecf0f1")
            details_frame.pack(pady=10, padx=20, anchor='w')
            
            admission_id_entry = tk.Entry(details_frame, font=('Arial', 14), bg="#ffffff", bd=2, relief="solid", width=len(f"Admission ID: {student_info[0]}") + 2)
            admission_id_entry.insert(0, f"Admission ID: {student_info[0]}")
            admission_id_entry.pack(anchor='w', padx=5, pady=2)
            
            name_entry = tk.Entry(details_frame, font=('Arial', 14), bg="#ffffff", bd=2, relief="solid", width=len(f"Name: {student_info[1]} {student_info[2]}") + 2)
            name_entry.insert(0, f"Name: {student_info[1]} {student_info[2]}")
            name_entry.pack(anchor='w', padx=5, pady=2)
            
            comments_label = tk.Label(interview_profile_window, text="Comments:", font=('Arial', 14, 'bold'), bg="#ecf0f1")
            comments_label.pack(pady=5, anchor='w', padx=20)  # Added left margin
            
            comments_text = tk.Text(interview_profile_window, width=60, height=8, font=('Arial', 12), bd=2, relief="solid")
            comments_text.pack(pady=5, padx=20)
            comments_text.insert(tk.END, student_info[4] if student_info[4] else "No comments available.")
            
            button_frame = tk.Frame(interview_profile_window, bg="#ecf0f1")
            button_frame.pack(pady=15)

            button_frame2 = tk.Frame(interview_profile_window, bg="#ecf0f1")
            button_frame2.pack(pady=15)
            
            tk.Button(
                button_frame, text="Save Comments", command=lambda: save_profile_comments(admission_id, comments_text.get("1.0", tk.END).strip()),
                font=('Arial', 12, 'bold'), bg="#3498db", fg="#ffffff", padx=15, pady=5
            ).grid(row=0, column=0, padx=10)
            
            tk.Button(
                button_frame, text="Accept Student", command=lambda: update_interview_status(admission_id),
                font=('Arial', 12, 'bold'), bg="#27ae60", fg="#ffffff", padx=15, pady=5
            ).grid(row=0, column=1, padx=10)
            
            tk.Button(
                button_frame2, text="Reject Student", command=lambda:reject_student_interview(admission_id),
                font=('Arial', 12, 'bold'), bg="#e74c3c", fg="#ffffff", padx=15, pady=5
            ).grid(row=0, column=0, padx=10)

    
        def save_profile_comments(admission_id, comments):
            try:
                cursor.execute("""
                    UPDATE admitted 
                    SET comments = %s
                    WHERE Admission_ID = %s
                """, (comments, admission_id))
                connection.commit()
                messagebox.showinfo("Success", "Comments saved successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error saving comments: {err}")

        def reject_student_interview(admission_id, reject):
            try:
                cursor.execute("""
                    UPDATE admitted 
                    SET interview_status = 'rejected'
                    WHERE Admission_ID = %s
                """, (reject, admission_id))
                connection.commit()
                messagebox.showinfo("Success", "The student has been rejected")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error saving comments: {err}")

    def update_interview_status(admission_id):
        try:
            cursor.execute("""
                UPDATE admitted 
                SET interview_status = 'done'
                WHERE Admission_ID = %s
            """, (admission_id,))
            connection.commit()

            messagebox.showinfo("Success", "Interview marked as done.")
            load_interview_data("done")

            # Fetch student name from admitted table
            cursor.execute("SELECT first_name, last_name FROM admitted WHERE Admission_ID = %s", (admission_id,))
            student_info = cursor.fetchone()
            if not student_info:
                messagebox.showerror("Database Error", "Student info not found!")
                return
            
                        # Insert into student_balance
            current_date_added_sb = datetime.now().strftime('%Y-%m-%d')  
            cursor.execute("""
                INSERT INTO student_balance (date_added, student_id, name) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE date_added = VALUES(date_added)
            """, (current_date_added_sb, admission_id, student_info[1] + " " + student_info[0]))
            connection.commit()

            # Insert into requirement_checklist
            cursor.execute("""
                INSERT INTO requirement_checklist (id, name) 
                VALUES (%s, %s)
            """, (admission_id, student_info[1] + " " + student_info[0]))
            connection.commit()

            interview_profile_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating status: {err}")


    def load_interview_data(status):
        global cursor
        global status_label  # Update the label based on the filter

        # Update the label text based on the selected status
        status_text = {
            "pending": "Pending Interviews",
            "done": "Accepted Interviews",
            "rejected": "Rejected Interviews"
        }
        status_label.config(text=f"Showing: {status_text[status]}")

        # Clear existing rows
        for row in tree_interview.get_children():
            tree_interview.delete(row)

        ensure_connection()  # Ensure database connection is active
        connection.commit()  # Force MySQL to refresh

        # Close old cursor safely before reassigning
        if cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error:
                pass  # Ignore if cursor is already closed

        cursor = connection.cursor(buffered=True)

        cursor.execute("""
            SELECT Admission_ID, Last_Name, First_Name, Nickname, Gender, Fathers_Name, Mothers_Name, interview_scheduled 
            FROM admitted
            WHERE interview_status = %s
        """, (status,))

        fetched_rows = cursor.fetchall()
        cursor.fetchall()  # Fetch any unread results (if needed)

        # Configure row colors
        tree_interview.tag_configure("evenrow", background="#f2f2f2")
        tree_interview.tag_configure("oddrow", background="#ffffff")

        for idx, row in enumerate(fetched_rows):
            student_id = row[0]
            unique_iid = f"{student_id}_{idx}"

            # Determine row tag based on index
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            tree_interview.insert("", "end", iid=unique_iid, values=row, tags=(tag,))
       

#====================================================== ADMITTED PANEL ======================================================================
    def create_admitted_view():
        global admitted_frame, tree_admitted  
        all_admitted_students = []
        admitted_frame = tk.Frame(content_frame, bg="#ecf0f1")
        admitted_frame.grid(row=0, column=0, sticky="nsew")

        # Title Frame
        title_frame = tk.Frame(admitted_frame, bg="#0f1074", height=100)
        title_frame.pack(fill="x", side="top")
        title_frame.pack_propagate(False)

        # Add an icon
        icon_image = tk.PhotoImage(file="images/mitted.png")  
        icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
        icon_label.image = icon_image  
        icon_label.pack(side="left", padx=10, pady=10)

        # Title Label
        title_label = tk.Label(
            title_frame,
            text="Admitted Student",
            font=("Arial", 30, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10)

        # Search and Refresh Frame
        search_frame = tk.Frame(admitted_frame, bg="#ecf0f1")
        search_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(search_frame, text="Search:", font=('Arial', 12), bg="#ecf0f1").pack(side='left', padx=5)

        search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30)
        search_entry.pack(side='left', padx=5)

        search_button = tk.Button(
            search_frame, text="Search", command=lambda: search_students(search_entry.get()), 
            font=('Arial', 12, 'bold'), bg="#ff5733", fg="#ffffff", width=10
        )
        search_button.pack(side='left', padx=5)

        refresh_button_admitted = tk.Button(
            search_frame, text="Refresh", command=load_admitted_data, 
            font=('Arial', 10, 'bold'), bg="#3498db", fg="#ffffff", width=10
        )
        refresh_button_admitted.pack(side='left', padx=5)

        # Table Frame (contains table + scrollbars)
        table_frame = tk.Frame(admitted_frame, bg="#ecf0f1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Table Setup
        tree_columns = (
            "Admission ID", "Last Name", "First Name", "Nickname", "Birthday", "Age", 
            "Gender", "Address", "Father's Name", "Father's Age", "Father's email", 
            "Father's contact", "Father's occupation", "Father's company", 
            "Mother's Name", "Mother's Age", "Mother's email", "Mother's contact", 
            "Mother's occupation", "Mother's company", "Parents' Status"
        )

        tree_admitted = ttk.Treeview(table_frame, columns=tree_columns, show="headings", height=15)

        for col in tree_columns:
            tree_admitted.heading(col, text=col)
            tree_admitted.column(col, anchor='center', width=120)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree_admitted.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree_admitted.xview)
        tree_admitted.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Using `grid()` for proper layout
        tree_admitted.grid(row=0, column=0, sticky="nsew")  # Treeview fills available space
        vsb.grid(row=0, column=1, sticky="ns")  # Vertical scrollbar on the right
        hsb.grid(row=1, column=0, sticky="ew")  # Horizontal scrollbar at the bottom

        # Configure `table_frame` to expand properly
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Striped Rows
        tree_admitted.tag_configure("evenrow", background="#ffbb00")
        tree_admitted.tag_configure("oddrow", background="#F5F5DC")

        tree_admitted.bind("<Double-1>", on_admitted_row_double_click)

        load_admitted_data()

        def search_students():
            search_query = search_entry.get().lower()

            for row in tree_admitted.get_children():
                tree_admitted.delete(row)

            if not search_query:
                load_admitted_data()
                for row in all_admitted_students:
                    tree_admitted.insert("", "end", values=row)  
                return 

            cursor.execute("""
                SELECT Admission_ID, Last_Name, First_Name, Nickname, 
                    Birthday, Age, Gender, Address, Fathers_Name, 
                    Fathers_Age, Mothers_Name, Mothers_Age, Parents_Are  
                FROM admitted 
                WHERE LOWER(Last_Name) LIKE %s 
                OR LOWER(First_Name) LIKE %s 
                OR LOWER(Nickname) LIKE %s
            """, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))

            results = cursor.fetchall()
            for idx, row in enumerate(results):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree_admitted.insert("", "end", values=row, tags=(tag,))

    def enroll_student(admission_id):
        input_frame.tkraise()
        cursor.execute("""
            SELECT a.Admission_ID, a.Last_Name, a.First_Name, a.Nickname, 
                            a.Birthday, a.Age, a.Gender, a.Address, 
                            a.Fathers_Name, a.Fathers_Age, a.Fathers_Email, a.Fathers_Contact_No, a.Fathers_Occupation, a.Fathers_Company_Name,
                            a.Mothers_Name, a.Mothers_Age, a.Mothers_Email, a.Mothers_Contact_No, a.Mothers_Occupation, a.Mothers_Company_Name,
                            a.Parents_Are
            FROM admitted a
            WHERE a.Admission_ID = %s
        """, (admission_id,))
        selected_data = cursor.fetchone()


        if selected_data:

            try:
                last_name_entry.delete(0, tk.END)
                last_name_entry.insert(0, selected_data[1])

                first_name_entry.delete(0, tk.END)
                first_name_entry.insert(0, selected_data[2])

                nickname_entry.delete(0, tk.END)
                nickname_entry.insert(0, selected_data[3] if selected_data[3] else "") 

                birthday_entry.set_date(selected_data[4])

                age_entry.delete(0, tk.END)
                age_entry.insert(0, selected_data[5])

                gender_entry.delete(0, tk.END)
                gender_entry.insert(0, selected_data[6])

                address_text.delete(1.0, tk.END)
                address_text.insert(tk.END, selected_data[7])

                if selected_data[8] is not None:
                    father_name_entry.insert(0, selected_data[8])
                else:
                    father_name_entry.insert(0, "")  

                if selected_data[9] is not None:
                    father_age_entry.insert(0, selected_data[9])
                else:
                    father_age_entry.insert(0, "") 

                if selected_data[10] is not None:
                    father_email_entry.insert(0, selected_data[10])
                else:
                    father_email_entry.insert(0, "")  

                if selected_data[11] is not None:
                    father_contact_entry.insert(0, selected_data[11])
                else:
                    father_contact_entry.insert(0, "")  

                if selected_data[12] is not None:
                    father_occupation_entry.insert(0, selected_data[12])
                else:
                    father_occupation_entry.insert(0, "")  

                if selected_data[13] is not None:
                    father_company_entry.insert(0, selected_data[13])
                else:
                    father_company_entry.insert(0, "")     

                if selected_data[14] is not None:
                    mother_name_entry.insert(0, selected_data[14])
                else:
                    mother_name_entry.insert(0, "")  

                if selected_data[15] is not None:
                    mother_age_entry.insert(0, selected_data[15])
                else:
                    mother_age_entry.insert(0, "")  

                if selected_data[16] is not None:
                    mother_email_entry.insert(0, selected_data[16])
                else:
                    mother_email_entry.insert(0, "")    

                if selected_data[17] is not None:
                    mother_contact_entry.insert(0, selected_data[17])
                else:
                    mother_contact_entry.insert(0, "")    

                if selected_data[18] is not None:
                    mother_occupation_entry.insert(0, selected_data[18])
                else:
                    mother_occupation_entry.insert(0, "") 

                if selected_data[19] is not None:
                    mother_company_entry.insert(0, selected_data[19])
                else:
                    mother_company_entry.insert(0, "")       


                status_var.set("together" if selected_data[20] == "Still together" else "not_together")

            except IndexError as e:
                print(f"Error inserting data: {e}")
        else:
            messagebox.showerror("Error", f"No student found with Admission ID: {admission_id}")

    def load_admitted_data():
        global cursor
        for row in tree_admitted.get_children():
            tree_admitted.delete(row)

        ensure_connection()  # Ensure database connection is active
        connection.commit()  # Force MySQL to refresh

        # Close old cursor safely before reassigning
        if cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error:
                pass  # Ignore if cursor is already closed

        cursor = connection.cursor(buffered=True)  # Create a new cursor

        cursor.execute("""
            SELECT a.Admission_ID, a.Last_Name, a.First_Name, a.Nickname, 
                a.Birthday, a.Age, a.Gender, a.Address, 
                a.Fathers_Name, a.Fathers_Age, a.Fathers_Email, a.Fathers_Contact_No, 
                a.Fathers_Occupation, a.Fathers_Company_Name,
                a.Mothers_Name, a.Mothers_Age, a.Mothers_Email, a.Mothers_Contact_No, 
                a.Mothers_Occupation, a.Mothers_Company_Name,
                a.Parents_Are
            FROM admitted a
            WHERE a.interview_status = 'done'
        """)

        fetched_rows = cursor.fetchall()  # Fetch all rows from the query result

        for idx, row in enumerate(fetched_rows):
            # Ensure unique temporary `iid` if duplicates could exist
            student_id = row[0]
            unique_iid = f"{student_id}_{idx}"
            
            # Determine even or odd row for coloring
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            
            # Insert data into the treeview using the unique `iid` and apply the row color
            tree_admitted.insert("", "end", iid=unique_iid, values=row, tags=(tag,))


#======================================================UPDATES PANEL======================================================================
    def load_updates_data():
        global cursor
        for row in tree_updates.get_children():
            tree_updates.delete(row)

        ensure_connection()  # Ensure database connection is active
        connection.commit()  # Force MySQL to refresh

        # Close old cursor safely before reassigning
        if cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error:
                pass  # Ignore if cursor is already closed

        cursor = connection.cursor(buffered=True)  # Create a new cursor

        cursor.execute("""
            SELECT *
            FROM updates
        """)

        fetched_rows = cursor.fetchall()

            # If there are any unread results, we can fetch them and ignore
        cursor.fetchall()  # Fetch any unread results (if needed)


            # Process each fetched row
        for idx, row in enumerate(fetched_rows):
                # Ensure unique temporary `iid` if duplicates could exist
                student_id = row[0]
                unique_iid = f"{student_id}_{idx}"
                
                # Insert data into the treeview using the unique `iid`
                tree_updates.insert("", "end", iid=unique_iid, values=row)

                # Optionally also call striped row logic
                current_row_index = len(tree_updates.get_children())
                tag = "evenrow" if current_row_index % 2 == 0 else "oddrow"
                tree_updates.item(unique_iid, tags=(tag,))

    def start_updates_edit(event):
        selected_item = tree_updates.selection()
        if selected_item:
            item_data = tree_updates.item(selected_item)
            values = item_data['values']

            student_id = values[1]

            display_current_details(student_id)
            display_requested_details(values)

    def fetch_profile_picture(student_id):
        try:    
            ensure_connection()  # Ensure the database connection is active
            cursor = connection.cursor()

            # Query to fetch the profile picture from updates table
            query = "SELECT profile_picture FROM updates WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            if result:
                profile_picture = result[0]
            else:
                profile_picture = None

            # Fetch from studentinfo if profile_picture is still None
            if not profile_picture:
                query = "SELECT profile_picture FROM studentinfo WHERE student_id = %s"
                cursor.execute(query, (student_id,))
                result = cursor.fetchone()
                profile_picture = result[0] if result else None

            return profile_picture

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            if cursor:
                cursor.fetchall()  # Ensure any unread results are cleared
                cursor.close()

                
    def approve_update(update_id):
        """Approve the update request in the database."""
        try:
            # Fetch the requested update details using the update_id
            cursor.execute("""
                SELECT student_id, last_name, first_name, nickname, grade_level, age, gender, birthday, address,
                    father, father_age, father_email, father_occupation, father_contact, father_company,
                    mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company,
                    profile_picture
                FROM updates
                WHERE update_id = %s
            """, (update_id,))
            
            requested_update = cursor.fetchone()

            if requested_update:
                # Unpack the known number of columns that you've specified to retrieve
                (student_id, last_name, first_name, nickname, grade_level, age, gender, birthday, address,
                fathers_name, fathers_age, fathers_email, fathers_occupation, fathers_contact_no, fathers_company_name,
                mothers_name, mothers_age, mothers_email, mothers_occupation, mothers_contact_no, mothers_company_name,
                picture) = requested_update
                
                # Perform the update in the studentinfo table
                cursor.execute("""
                    UPDATE studentinfo
                    SET last_name = %s, first_name = %s, nickname = %s,
                        grade_level = %s, age = %s, gender = %s,
                        birthday = %s, address = %s,
                        father = %s, father_age = %s, father_email = %s,
                        father_occupation = %s, father_contact = %s,
                        father_company = %s, mother = %s,
                        mother_age = %s, mother_email = %s,
                        mother_occupation = %s, mother_contact = %s,
                        mother_company = %s, profile_picture = %s
                    WHERE student_id = %s
                """, (last_name, first_name, nickname, grade_level, age, gender, birthday, address,
                    fathers_name, fathers_age, fathers_email, fathers_occupation, fathers_contact_no, fathers_company_name,
                    mothers_name, mothers_age, mothers_email, mothers_occupation, mothers_contact_no, mothers_company_name,
                    picture, student_id))

                approve_text = "Your request has been approved!"

                cursor.execute("""
                    INSERT INTO student_remarks (student_id, update_reject) 
                    VALUES (%s, %s)
                """, (student_id, approve_text))

                 # Delete the update entry from the updates table
                cursor.execute("DELETE FROM updates WHERE update_id = %s", (update_id,))
                connection.commit()
                
                messagebox.showinfo("Update Approved", "The update request has been approved and applied.")
                load_updates_data()
                clear_details()
                load_studentml_data()
            else:
                messagebox.showwarning("No Update Found", "Could not find the requested update details.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def reject_update(update_id):
        """Prompts for a rejection reason and deletes the update request in the database, logging the reason in student_remarks."""
        
        # Prompt for the reason for rejection
        rejection_reason = simpledialog.askstring("Rejection Reason", "Please provide a reason for rejecting this update:")

        if rejection_reason is not None:  # Check if the user did not cancel the prompt
            try:
                # Fetch the student_id related to the update_id for logging purposes
                cursor.execute("""
                    SELECT student_id
                    FROM updates
                    WHERE update_id = %s
                """, (update_id,))
                student_id_data = cursor.fetchone()

                if student_id_data:
                    student_id = student_id_data[0]  # Get the student ID from the fetched data

                    # Delete the update entry from the updates table
                    cursor.execute("DELETE FROM updates WHERE update_id = %s", (update_id,))
                    
                    # Log the rejection reason into the student_remarks table as a new entry
                    cursor.execute("""
                        INSERT INTO student_remarks (student_id, update_reject) 
                        VALUES (%s, %s)
                    """, (student_id, rejection_reason))

                    connection.commit()
                    messagebox.showinfo("Update Rejected", "The update request has been rejected, and the reason has been logged.")

                    # Reload data to reflect changes
                    load_updates_data()
                    clear_details()
                else:
                    messagebox.showwarning("Error", "Could not retrieve student ID for the selected update.")
            
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showinfo("Rejection Cancelled", "Rejection has been cancelled without changes.")

    def clear_details():
        """Clear both current and requested details frames."""
        for widget in details_frame_current.winfo_children():
            widget.destroy()
            
        for widget in details_frame_requested.winfo_children():
            widget.destroy()
            
    def create_updates_view():
        global updates_frame
        global tree_updates
        global details_frame_current
        global details_frame_requested

        updates_frame = tk.Frame(content_frame, bg="#ecf0f1")
        updates_frame.grid(row=0, column=0, sticky="nsew")

        # Title Frame
        title_frame = tk.Frame(updates_frame, bg="#0f1074", height=100)
        title_frame.pack(fill="x", side="top")
        title_frame.pack_propagate(False)

        # Icon and Title
        icon_image = tk.PhotoImage(file="images/up.png")
        icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
        icon_label.image = icon_image
        icon_label.pack(side="left", padx=10, pady=10)

        title_label = tk.Label(
            title_frame,
            text="Student Updates",
            font=("Arial", 30, "bold"),
            bg="#0f1074",
            fg="#E8E4C9"
        )
        title_label.pack(side="left", padx=10)

        # Frame for Refresh Button
        button_frame = tk.Frame(updates_frame, bg="#ecf0f1")
        button_frame.pack(fill="x", pady=5)

        refresh_button_updates = tk.Button(
            button_frame,
            text="Refresh",
            command=load_updates_data,
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            width=12
        )
        refresh_button_updates.pack(side="left", padx=10, pady=5)

        # Main content container
        main_content = tk.Frame(updates_frame)
        main_content.pack(fill="both", expand=True, padx=10, pady=5)

        # Left pane - Treeview (70% width)
        left_pane = tk.Frame(main_content)
        left_pane.pack(side="left", fill="both", expand=True)

        # Treeview Styling
        style = ttk.Style()
        style.theme_use("clam")
        style_name = "Updates.Treeview"
        style.configure(style_name, rowheight=25, font=("Arial", 11))
        style.configure(style_name + ".Heading", font=("Arial", 13, "bold"))
        style.configure("Treeview", rowheight=25, font=("Arial", 12))
        style.map("Treeview", background=[("selected", "#436060")], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#9f0000", foreground="white")

        # Treeview with scrollbars
        tree_columns = ("Update ID", "Student ID", "Last Name", "First Name")
        tree_updates = ttk.Treeview(left_pane, columns=tree_columns, show="headings", height=15, style=style_name)

        tree_updates.tag_configure("evenrow", background="#ffbb00")
        tree_updates.tag_configure("oddrow", background="#F5F5DC")

        for col in tree_columns:
            tree_updates.heading(col, text=col)
            tree_updates.column(col, anchor='center', width=120)

        vsb = ttk.Scrollbar(left_pane, orient="vertical", command=tree_updates.yview)
        hsb = ttk.Scrollbar(left_pane, orient="horizontal", command=tree_updates.xview)
        tree_updates.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree_updates.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        left_pane.grid_rowconfigure(0, weight=1)
        left_pane.grid_columnconfigure(0, weight=1)

        # Right pane - Details frames (30% width)
        right_pane = tk.Frame(main_content, width=300)  # Fixed width for details
        right_pane.pack(side="right", fill="y", padx=(10, 0))

        # Function to Set Default View
        def set_default_view(frame):
            img = tk.PhotoImage(file="images/1.png")
            label = tk.Label(frame, image=img, bg="#dfe6e9")
            label.image = img
            label.pack(expand=True)

        # Current Details Frame (top)
        details_frame_current = tk.Frame(right_pane, bg="#dfe6e9", relief=tk.GROOVE, bd=3)
        details_frame_current.pack(fill="both", expand=True, pady=(0, 5))
        set_default_view(details_frame_current)

        # Requested Details Frame (bottom)
        details_frame_requested = tk.Frame(right_pane, bg="#dfe6e9", relief=tk.GROOVE, bd=3)
        details_frame_requested.pack(fill="both", expand=True, pady=(5, 0))
        set_default_view(details_frame_requested)

        # Configure weights for the right pane
        right_pane.pack_propagate(False)  # Prevent shrinking
        right_pane.grid_propagate(False)

        # Double-click event
        tree_updates.bind("<Double-1>", start_updates_edit)

        load_updates_data()
        
    def display_current_details(student_id):
        for widget in details_frame_current.winfo_children():
            widget.destroy()

        # Add a label for current details
        current_details_label = tk.Label(details_frame_current, 
            text="Current Student Details", font=('Arial', 14, 'bold'), bg="#ecf0f1")
        current_details_label.pack(pady=(10, 5))

        # Create a canvas for scrolling
        details_canvas = tk.Canvas(details_frame_current, bg="#ecf0f1")
        details_frame = tk.Frame(details_canvas, bg="#ecf0f1")

        # Create a vertical scrollbar for the canvas
        scrollbar = ttk.Scrollbar(details_frame_current, orient="vertical", command=details_canvas.yview)
        details_canvas.configure(yscrollcommand=scrollbar.set)

        # Place the scrollbar and the canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        details_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a window in the canvas to hold the details frame
        details_canvas.create_window((0, 0), window=details_frame, anchor='nw')

        # Bind the canvas to resize the inner frame
        def on_configure(event):
            details_canvas.configure(scrollregion=details_canvas.bbox("all"))

        details_frame.bind("<Configure>", on_configure)

        cursor.execute("""
            SELECT *
            FROM studentinfo
            WHERE student_id = %s
        """, (student_id,))
        current_data = cursor.fetchone()

        labels = ["ID", "Student ID","LRN", "Last Name", "First Name", "Nickname", "Grade Level", "Age", "Gender", "Birthday", 
                "Address", "Father", "Father's Age", "Father's Email", "Father's Occupation", "Father's Contact", 
                "Father's Company", "Mother", "Mother's Age", "Mother's Email", "Mother's Occupation", 
                "Mother's Contact", "Mother's Company", "Profile Picture"]

        if current_data:
            # Display image if available
            profile_picture = current_data[-2]  # Assuming the last column is the profile picture

            if profile_picture:
                try:
                    if isinstance(profile_picture, str):  # Check if it's a file path
                        img = Image.open(profile_picture)  # Use Pillow to open the image
                        img = img.resize((100, 100))  # Resize the image to fit the frame
                        img_tk = ImageTk.PhotoImage(img)

                    elif isinstance(profile_picture, bytes):  # Check if it's binary data
                        img = Image.open(io.BytesIO(profile_picture))  # Open from binary data
                        img = img.resize((100, 100))  # Resize the image
                        img_tk = ImageTk.PhotoImage(img)

                    # Display the image
                    image_label = tk.Label(details_frame, image=img_tk, bg="#ecf0f1")
                    image_label.image = img_tk  # Keep a reference to the image
                    image_label.pack(pady=10)

                except Exception as e:
                    print(f"Error loading image: {e}")
                    # No fallback or placeholder image is shown here
                
            # Continue displaying other labels as normal
            for label, value in zip(labels, current_data):
                frame = tk.Frame(details_frame, bg="#ecf0f1", relief=tk.GROOVE, bd=1)
                frame.pack(fill=tk.X, pady=5)

                label_widget = tk.Label(frame, text=f"{label}: ", bg="#ecf0f1", font=('Arial', 12, 'bold'))
                label_widget.pack(side=tk.LEFT, padx=(5, 2))
                value_widget = tk.Label(frame, text=value if value is not None else "N/A", bg="#ecf0f1", font=('Arial', 12))
                value_widget.pack(side=tk.LEFT, padx=(0, 5))
        else:
            messagebox.showwarning("No Data", "No details found for this student.")

    def display_requested_details(values):
        for widget in details_frame_requested.winfo_children():
            widget.destroy()

        requested_updates_label = Label(details_frame_requested, text="Requested Updates", font=('Arial', 14, 'bold'), bg="#ecf0f1")
        requested_updates_label.pack(pady=(10, 5))

        labels = ["Update ID", "Student ID", "Last Name", "First Name", "Nickname", "Grade Level", "Age", "Gender", "Birthday", 
                "Address", "Father", "Father's Age", "Father's Email", "Father's Occupation", "Father's Contact", 
                "Father's Company", "Mother", "Mother's Age", "Mother's Email", "Mother's Occupation", 
                "Mother's Contact", "Mother's Company"]

        details_canvas = Canvas(details_frame_requested, bg="#ecf0f1")
        details_frame = Frame(details_canvas, bg="#ecf0f1")

        scrollbar = ttk.Scrollbar(details_frame_requested, orient="vertical", command=details_canvas.yview)
        details_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        details_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        details_canvas.create_window((0, 0), window=details_frame, anchor='nw')

        def on_configure(event):
            details_canvas.configure(scrollregion=details_canvas.bbox("all"))

        details_frame.bind("<Configure>", on_configure)

        student_id = values[1]
        profile_picture = fetch_profile_picture(student_id)

        if profile_picture:
            try:
                if isinstance(profile_picture, str) and os.path.exists(profile_picture):
                    img = Image.open(profile_picture)
                elif isinstance(profile_picture, bytes):
                    img = Image.open(io.BytesIO(profile_picture))
                else:
                    raise ValueError("Invalid profile picture format.")
                
                img = img.resize((100, 100))
                img_tk = ImageTk.PhotoImage(img)

                image_label = Label(details_frame, image=img_tk, bg="#ecf0f1")
                image_label.image = img_tk
                image_label.pack(pady=10)
            except Exception as e:
                print(f"Error loading image: {e}")

        for label, value in zip(labels, values):
            frame = Frame(details_frame, bg="#ecf0f1", relief=GROOVE, bd=1)
            frame.pack(fill=X, pady=5)

            label_widget = Label(frame, text=f"{label}: ", bg="#ecf0f1", font=('Arial', 12, 'bold'))
            label_widget.pack(side=LEFT, padx=(5, 2))

            value_widget = Label(frame, text=value if value is not None else "N/A", bg="#ecf0f1", font=('Arial', 12))
            value_widget.pack(side=LEFT, padx=(0, 5))

        button_frame = Frame(details_frame, bg="#ecf0f1")
        button_frame.pack(pady=20)

        approve_button = Button(button_frame, text="Approve", command=lambda: approve_update(values[0]), bg="#8bca84", fg="#ffffff")
        approve_button.pack(side=LEFT, padx=(0, 10))

        reject_button = Button(button_frame, text="Reject", command=lambda: reject_update(values[0]), bg="#e74c3c", fg="#ffffff")
        reject_button.pack(side=LEFT)

        details_frame.bind("<Configure>", lambda event: details_canvas.configure(scrollregion=details_canvas.bbox("all")))
                            



#=======================================================INPUT PANEL========================================================================

    input_frame = tk.Frame(content_frame, bg="#ecf0f1")
    input_frame.grid(row=0, column=0, sticky="nsew")

    # Configure grid columns for better spacing and alignment
    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=2)  # Give this column more weight if needed
    input_frame.columnconfigure(2, weight=1)
    input_frame.columnconfigure(3, weight=1)

    tk.Label(input_frame, text="Enrollment", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)

    # Title for the section
    tk.Label(input_frame, text="STUDENT INFORMATION", font=('Arial', 14), bg="gray", padx=30).grid(row=1, column=0, columnspan=4, pady=10, sticky='ew')

    # Row 1: Last Name and Age
    tk.Label(input_frame, text="Last Name:", font=('Arial', 12)).grid(row=2, column=0, padx=20, pady=5, sticky='e')
    last_name_entry = tk.Entry(input_frame, font=('Arial', 12))
    last_name_entry.grid(row=2, column=1, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="First Name:", font=('Arial', 12)).grid(row=3, column=0, padx=20, pady=5, sticky='e')
    first_name_entry = tk.Entry(input_frame, font=('Arial', 12))
    first_name_entry.grid(row=3, column=1, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="Nickname:", font=('Arial', 12)).grid(row=4, column=0, padx=20, pady=5, sticky='e')
    nickname_entry = tk.Entry(input_frame, font=('Arial', 12))
    nickname_entry.grid(row=4, column=1, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="Birthday:", font=('Arial', 12)).grid(row=5, column=0, padx=20, pady=5, sticky='ne')
    birthday_entry = DateEntry(input_frame, font=('Arial', 12), background='darkblue', foreground='white', borderwidth=2, date_pattern='mm/dd/yyyy')
    birthday_entry.grid(row=5, column=1, padx=20, pady=5, sticky='nw')  # Adjust padding for alignment

    tk.Label(input_frame, text="Grade Level:", font=('Arial', 12), bg="#ecf0f1").grid(row=2, column=2, padx=20, pady=5, sticky='e')
    global enrollment_grade_combo
    enrollment_grade_combo = ttk.Combobox(input_frame, values=["Junior Nursery","Senior Nursery", "Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"], state='readonly', font=('Arial', 12))
    enrollment_grade_combo.grid(row=2, column=3, padx=20, pady=5, sticky='w')
    
    tk.Label(input_frame, text="Age:", font=('Arial', 12)).grid(row=3, column=2, padx=20, pady=5, sticky='e')
    age_entry = tk.Entry(input_frame, font=('Arial', 12))
    age_entry.grid(row=3, column=3, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="Gender:", font=('Arial', 12)).grid(row=4, column=2, padx=20, pady=5, sticky='e')
    gender_entry = tk.Entry(input_frame, font=('Arial', 12))
    gender_entry.grid(row=4, column=3, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="Address:", font=('Arial', 12)).grid(row=5, column=2, padx=20, pady=5, sticky='ne')
    address_text = tk.Text(input_frame, font=('Arial', 12), height=4, width=30)
    address_text.grid(row=5, column=3, padx=20, pady=5, sticky='w')

      # Title for the section
    tk.Label(input_frame, text="FAMILY PARTICULARS (UPDATES)", font=('Arial', 14), bg="gray", padx=30).grid(row=6, column=0, columnspan=4, pady=10, sticky='ew')
    tk.Label(input_frame, text="if one or both the parents are missing or not in communication with the child, leave blank", font=('Arial', 9), padx=30).grid(row=7, column=0, columnspan=4, pady=0, sticky='ew')
    
    # Father's Information
    tk.Label(input_frame, text="Father's Name:", font=('Arial', 12)).grid(row=8, column=0, padx=20, pady=5, sticky='e')
    father_name_entry = tk.Entry(input_frame, font=('Arial', 12))
    father_name_entry.grid(row=8, column=1, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="Age:", font=('Arial', 12)).grid(row=8, column=2, padx=20, pady=5, sticky='e')
    father_age_entry = tk.Entry(input_frame, font=('Arial', 12))
    father_age_entry.grid(row=8, column=3, padx=20, pady=5, sticky='w')

        # Father's Email and Occupation
    tk.Label(input_frame, text="Father's Email:", font=('Arial', 12)).grid(row=9, column=0, padx=20, pady=5, sticky='e')
    father_email_entry = tk.Entry(input_frame, font=('Arial', 12))
    father_email_entry.grid(row=9, column=1, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="Occupation:", font=('Arial', 12)).grid(row=9, column=2, padx=20, pady=5, sticky='e')
    father_occupation_entry = tk.Entry(input_frame, font=('Arial', 12))
    father_occupation_entry.grid(row=9, column=3, padx=20, pady=5, sticky='w')

    # Father's Contact No and Company Name
    tk.Label(input_frame, text="Contact No:", font=('Arial', 12)).grid(row=10, column=0, padx=20, pady=5, sticky='e')
    father_contact_entry = tk.Entry(input_frame, font=('Arial', 12))
    father_contact_entry.grid(row=10, column=1, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="Company Name:", font=('Arial', 12)).grid(row=10, column=2, padx=20, pady=5, sticky='e')
    father_company_entry = tk.Entry(input_frame, font=('Arial', 12))
    father_company_entry.grid(row=10, column=3, padx=20, pady=5, sticky='w')

    # Mother's Information
    tk.Label(input_frame, text="Mother's Name:", font=('Arial', 12)).grid(row=11, column=0, padx=20, pady=5, sticky='e')
    mother_name_entry = tk.Entry(input_frame, font=('Arial', 12))
    mother_name_entry.grid(row=11, column=1, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="Mother's Age:", font=('Arial', 12)).grid(row=11, column=2, padx=20, pady=5, sticky='e')
    mother_age_entry = tk.Entry(input_frame, font=('Arial', 12))
    mother_age_entry.grid(row=11, column=3, padx=20, pady=5, sticky='w')

    # Mother's Email and Occupation
    tk.Label(input_frame, text="Mother's Email:", font=('Arial', 12)).grid(row=12, column=0, padx=20, pady=5, sticky='e')
    mother_email_entry = tk.Entry(input_frame, font=('Arial', 12))
    mother_email_entry.grid(row=12, column=1, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="Occupation:", font=('Arial', 12)).grid(row=12, column=2, padx=20, pady=5, sticky='e')
    mother_occupation_entry = tk.Entry(input_frame, font=('Arial', 12))
    mother_occupation_entry.grid(row=12, column=3, padx=20, pady=5, sticky='w')

    # Mother's Contact No and Company Name
    tk.Label(input_frame, text="Contact No:", font=('Arial', 12)).grid(row=13, column=0, padx=20, pady=5, sticky='e')
    mother_contact_entry = tk.Entry(input_frame, font=('Arial', 12))
    mother_contact_entry.grid(row=13, column=1, padx=20, pady=5, sticky='w')

    tk.Label(input_frame, text="Company Name:", font=('Arial', 12)).grid(row=13, column=2, padx=20, pady=5, sticky='e')
    mother_company_entry = tk.Entry(input_frame, font=('Arial', 12))
    mother_company_entry.grid(row=13, column=3, padx=20, pady=5, sticky='w')

    status_var = tk.StringVar(value="together")
    tk.Label(input_frame, text="Parents' Status:", font=('Arial', 12)).grid(row=14, column=0, padx=20, pady=5, sticky='e')
    tk.Radiobutton(input_frame, text="Still together", variable=status_var, value="together", font=('Arial', 12)).grid(row=14, column=1, padx=20, pady=5, sticky='w')
    tk.Radiobutton(input_frame, text="No longer together", variable=status_var, value="not_together", font=('Arial', 12)).grid(row=14, column=2, padx=20, pady=5, sticky='w')

    tk.Button(input_frame, text="Submit", command=insert_data, font=('Arial', 14), bg="#27ae60", fg="#ecf0f1", width=15).grid(row=15, column=2, columnspan=2, pady=20)


#=======================================================CASHIER PANEL=============================================
    def filter_cashier_data(grade, school_year):
        # Validate if a proper school year is selected
        if not school_year or school_year == "Select School Year" or "-" not in school_year:
            messagebox.showerror("Input Error", "Please select a valid school year.")
            return
        
        try:
            # Extract start and end years from the selected school year (e.g., "2023-2024")
            start_year, end_year = map(int, school_year.split('-'))
            
            # Define the school year range (May 1st to April 30th)
            start_date = f"{start_year}-05-01"  # May 1st of the start year
            end_date = f"{end_year}-04-30"  # April 30th of the end year
        except ValueError:
            messagebox.showerror("Format Error", "Invalid school year format. Please select a proper school year.")
            return

        # Query to filter data based on grade level and date_added within the school year range
        query = """
            SELECT * FROM student_balance 
            WHERE grade_level = %s 
            AND date_added BETWEEN %s AND %s
        """
        cursor.execute(query, (grade, start_date, end_date))
        results = cursor.fetchall()

        # Clear previous entries in the UI and update with new data
        update_cashier_tree(results)

    def filter_all_cashier_data(school_year):
        """Function to load all data without filtering by grade."""
        if not school_year or school_year == "Select School Year" or "-" not in school_year:
            messagebox.showerror("Input Error", "Please select a valid school year.")
            return

        try:
            # Extract start and end years
            start_year, end_year = map(int, school_year.split('-'))
            start_date = f"{start_year}-05-01"
            end_date = f"{end_year}-04-30"
        except ValueError:
            messagebox.showerror("Format Error", "Invalid school year format. Please select a proper school year.")
            return


        query = """
            SELECT date_added, student_id, name, grade_level, cash, cheque, check_transfer, payment_status,
            status, due_date, paid_status, days_past_due, total_amount_due, overdue_amount, total_to_be_paid, date_paid, amount_paid,
            OR_no, balance, date_enrolled
              FROM student_balance 
            WHERE date_added BETWEEN %s AND %s
        """
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

        update_cashier_tree(results)


    def update_cashier_tree(results):
        for item in tree_cashier.get_children():
            tree_cashier.delete(item)
        for index, row in enumerate(results):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            tree_cashier.insert("", "end", values=row, tags=(tag,))
        # Apply striped rows
        tree_cashier.tag_configure("evenrow", background="#ffbb00")
        tree_cashier.tag_configure("oddrow", background="#F5F5DC")


    def sort_cashier_data():
        grade_order = {"Junior Nursery": 0, "Senior Nursery": 1, "Kindergarten": 2}
        grade_order.update({f"Grade {i}": i + 2 for i in range(1, 7)})
        
        data = [(tree_cashier.item(item, "values")) for item in tree_cashier.get_children()]
        sorted_data = sorted(data, key=lambda x: grade_order.get(x[3], 999))
        
        for row in tree_cashier.get_children():
            tree_cashier.delete(row)
        
        for row in sorted_data:
            table_insert_cashier_data(row)

    def search_cashier_data():
        search_term = search_entry.get().strip()
        for row in tree_cashier.get_children():
            tree_cashier.delete(row)
        
        ensure_connection()
        query = """
        SELECT 
            date_added, student_id, name, grade_level, cash, cheque, check_transfer, payment_status,
            status, due_date, paid_status, days_past_due, total_amount_due, overdue_amount, total_to_be_paid, date_paid, amount_paid,
            OR_no, balance, date_enrolled
        FROM 
            student_balance
        WHERE (name LIKE %s OR student_id LIKE %s) AND (YEAR(date_added) = %s AND MONTH(date_added) BETWEEN 5 AND 12
        OR YEAR(date_added) = %s AND MONTH(date_added) BETWEEN 1 AND 4)
        """
        
        previous_year = int(selected_school_year.get().split('-')[0])
        next_year = previous_year + 1
        
        cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", previous_year, next_year))
        fetched_data = cursor.fetchall()
        
        for row in fetched_data:
            table_insert_cashier_data(row)
    

    def edit_cell(event):
        """Enable editing of a specific cell on double-click."""
        # Get the row and column clicked
        selected_item = tree_cashier.focus()
        if not selected_item:
            return  # No row selected

        column = tree_cashier.identify_column(event.x)  # Get column ID
        row = tree_cashier.identify_row(event.y)  # Get row ID (iid)
        if not column or not row:
            return  # No valid cell clicked

        col_index = int(column.replace('#', '')) - 1  # Convert column ID to index
        item_values = tree_cashier.item(selected_item, "values")  # Get all values in the row

        # Get current cell value
        current_value = item_values[col_index]

        # Create an Entry widget to edit the value
        edit_window = tk.Entry(tree_cashier, font=('Arial', 12))
        edit_window.insert(0, current_value)
        edit_window.select_range(0, tk.END)

        # Position the Entry widget over the cell
        bbox = tree_cashier.bbox(selected_item, column)
        if bbox:
            edit_window.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])

        # Commit the value when pressing Enter
        def save_edit(event=None):
            new_value = edit_window.get()
            tree_cashier.item(selected_item, values=[
                new_value if i == col_index else val
                for i, val in enumerate(item_values)
            ])
            
            # Update the database with the student_id (2nd column) and new value
            student_id = item_values[1]  # Assuming student_id is in the second column
            update_database(student_id, col_index, new_value)
            edit_window.destroy()  # Destroy the Entry widget

        # Destroy the Entry widget if focus is lost
        def cancel_edit(event=None):
            edit_window.destroy()

        # Bind events to the Entry widget
        edit_window.bind("<Return>", save_edit)  # Save on Enter
        edit_window.bind("<FocusOut>", cancel_edit)  # Cancel on losing focus
        edit_window.focus()  # Set focus to the Entry widget


    def update_database(item_id, col_index, new_value):
        """Update the database with the edited cell value."""
        try:
            column_mapping = {
                0: "date_added",
                1: "student_id",
                2: "name",
                3: "grade_level",
                4: "cash",
                5: "cheque",
                6: "check_transfer",
                7: "payment_status",
                8: "status",
                9: "due_date",
                10: "paid_status",
                11: "days_past_due",
                12: "total_amount_due",
                13: "overdue_amount",
                14: "total_to_be_paid",
                15: "date_paid",
                16: "amount_paid",
                17: "OR_no",
                18: "balance"
            }

            # Get the corresponding column name
            column_name = column_mapping.get(col_index)
            if not column_name:
                print("Invalid column index")
                return

            # Update the database
            query = f"UPDATE student_balance SET {column_name} = %s WHERE student_id = %s"
            cursor.execute(query, (new_value, item_id))
            connection.commit()

        except Exception as e:
            print(f"Failed to update the database: {e}")

    def load_cashier_data():
        global cursor
        for row in tree_cashier.get_children():
            tree_cashier.delete(row)

        ensure_connection()  # Ensure database connection is active
        connection.commit()  # Force MySQL to refresh

        # Close old cursor safely before reassigning
        if cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error:
                pass  # Ignore if cursor is already closed

        cursor = connection.cursor(buffered=True)
        query = """
        SELECT 
            date_added, student_id, name, grade_level, cash, cheque, check_transfer, payment_status,
            status, due_date, paid_status, days_past_due, total_amount_due, overdue_amount, 
            total_to_be_paid, date_paid, amount_paid, OR_no, balance
        FROM 
            student_balance
        """

        cursor.execute(query)
        fetched_data = cursor.fetchall()

        # Configure row colors
        tree_cashier.tag_configure("oddrow", background="#ffbb00")  # Light Gray
        tree_cashier.tag_configure("evenrow", background="#F5F5DC")  # White

        for idx, row in enumerate(fetched_data):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            tree_cashier.insert("", "end", values=row, tags=(tag,))


    def table_insert_cashier_data(row):
        """Insert row data into the Treeview for cashier records."""
        try:
            current_row_index = len(tree_cashier.get_children())
            tag = "evenrow" if current_row_index % 2 == 0 else "oddrow"
            
            # Insert row without enforcing a unique ID
            tree_cashier.insert("", "end", values=row, tags=(tag,))
            
        except Exception as e:
            print(f"An error occurred: {e}")


    # Main Frame
    cashier_frame = tk.Frame(content_frame, bg="#ecf0f1")
    cashier_frame.grid(row=0, column=0, sticky="nsew")

    # Ensure content_frame resizes properly
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)

    # Title Frame
    title_frame = tk.Frame(cashier_frame, bg="#0f1074", height=100)
    title_frame.pack(fill="x")
    title_frame.pack_propagate(False)

    # Icon and Title
    icon_image = tk.PhotoImage(file="images/report.png")
    icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
    icon_label.image = icon_image
    icon_label.pack(side="left", padx=10)

    title_label = tk.Label(title_frame, text="Cashier Records", font=("Arial", 25, "bold"), bg="#0f1074", fg="#E8E4C9")
    title_label.pack(side="left", padx=10)

    # Search & Filters Frame
    search_frame = tk.Frame(cashier_frame, bg="#ecf0f1")
    search_frame.pack(fill="x", pady=5)

    tk.Label(search_frame, text="Search:", font=('Arial', 10, 'bold'), bg="#ecf0f1").pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, font=('Arial', 10), width=20)
    search_entry.pack(side="left", padx=5)

    tk.Button(search_frame, text="Search", font=('Arial', 9, 'bold'), bg="#2ecc71", fg="white",
            command=search_cashier_data).pack(side="left", padx=5)

    selected_school_year = tk.StringVar()
    school_year_selector = ttk.Combobox(search_frame, textvariable=selected_school_year, font=('Arial', 10), state='readonly', width=12)
    school_year_selector['values'] = [f"{y}-{y+1}" for y in range(2020, 2031)]
    school_year_selector.set("Select Year")
    school_year_selector.pack(side="left", padx=5)

    tk.Button(search_frame, text="Refresh", font=('Arial', 9, 'bold'), bg="#3498db", fg="white",
            command=load_cashier_data).pack(side="left", padx=5)

    # Filter Buttons
    button_frame = tk.Frame(cashier_frame, bg="#ecf0f1")
    button_frame.pack(fill="x", pady=5)

    tk.Label(button_frame, text="Grades:", font=('Arial', 10, 'bold'), bg="#ecf0f1").pack(side="left", padx=5)

    for grade in ["JN", "SN", "K", "G1", "G2", "G3", "G4", "G5", "G6"]:
        tk.Button(button_frame, text=grade, font=('Arial', 8, 'bold'), bg="#3498db", fg="white",
                width=6, command=lambda g=grade: filter_cashier_data(g, selected_school_year.get())).pack(side="left", padx=3)

    tk.Button(button_frame, text="All", font=('Arial', 8, 'bold'), bg="#27ae60", fg="white", width=6,
            command=lambda: filter_all_cashier_data(selected_school_year.get())).pack(side="left", padx=3)
    tk.Button(button_frame, text="Sort", font=('Arial', 8, 'bold'), bg="#34495e", fg="white", width=6,
            command=sort_cashier_data).pack(side="left", padx=3)

    # Table Frame (Expands Fully)
    table_frame = tk.Frame(cashier_frame, bg="#ecf0f1")
    table_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Define Treeview Table
    cashier_columns = (
        "Date", "Student ID", "Name", "Grade", "Cash", "Check", "Bank", "Status", "Due Date", "Notif", "Days Past Due",
        "Total Due", "Overdue", "Total Amt", "Date Paid", "Amt Paid", "OR No.", "Balance"
    )

    tree_cashier = ttk.Treeview(
        table_frame, columns=cashier_columns, show="headings", height=15  # Increased height for better view
    )

    # Scrollbars (Correctly Positioned)
    vsb_cashier = ttk.Scrollbar(table_frame, orient="vertical", command=tree_cashier.yview)
    hsb_cashier = ttk.Scrollbar(table_frame, orient="horizontal", command=tree_cashier.xview)
    tree_cashier.configure(yscrollcommand=vsb_cashier.set, xscrollcommand=hsb_cashier.set)

    # Pack Table Properly (Expands to fill space)
    tree_cashier.grid(row=0, column=0, sticky="nsew")
    vsb_cashier.grid(row=0, column=1, sticky="ns")
    hsb_cashier.grid(row=1, column=0, sticky="ew")

    # Ensure Frame Expands with Window
    table_frame.grid_columnconfigure(0, weight=1)
    table_frame.grid_rowconfigure(0, weight=1)

    # Set Column Headings
    for col in cashier_columns:
        tree_cashier.heading(col, text=col)
        tree_cashier.column(col, width=120, anchor='center')  # Adjust width as needed

    # Bind Double-Click for Editing
    tree_cashier.bind("<Double-1>", edit_cell)


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

                cursor.execute("""
                                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs
                                FROM student_history 
                                WHERE student_status = 'Active'
                               """)
                full_data.clear()
                for row in cursor.fetchall():
                    full_data.append(row)
    
    def table_select_inactive():
                for row in tree_table.get_children():
                    tree_table.delete(row)

                cursor.execute("""
                                SELECT student_id, LRN, last_name, first_name, nickname, grade_level, age, gender, birthday, address, father, 
                                        father_age, father_email, father_occupation, father_contact, father_company, 
                                        mother, mother_age, mother_email, mother_occupation, mother_contact, mother_company, 
                                        parents_status, date_enrolled, year, special_needs
                                FROM student_history 
                                WHERE student_status = 'Inactive'
                               """)
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


        
#=====================================================SCHEDULING FRAME=============================================
    scheduling_frame = tk.Frame(content_frame, bg="#ecf0f1")
    scheduling_frame.grid(row=0, column=0, sticky="nsew")

     # Create a frame for the title (for the background box)
    title_frame = tk.Frame(scheduling_frame, bg="#0f1074", height=100)  # Dark blue background
    title_frame.pack(fill="x", side="top")
    title_frame.pack_propagate(False)  # Prevent resizing based on child widgets

    # Add an icon
    icon_image = tk.PhotoImage(file="images/dule.png")  # Replace with actual icon path
    icon_label = tk.Label(title_frame, image=icon_image, bg="#0f1074")
    icon_label.image = icon_image  # Keep a reference to avoid garbage collection
    icon_label.pack(side="left", padx=10, pady=10)

    # Title Label
    title_label = tk.Label(
        title_frame,
        text="Scheduling",
        font=("Arial", 30, "bold"),
        bg="#0f1074",
        fg="#E8E4C9"  # Light text for contrast
    )
    title_label.pack(side="left", padx=10)

   # Form Frame for Inputs
    form_frame = tk.Frame(scheduling_frame, bg="#ecf0f1")
    form_frame.pack(fill="x", padx=20, pady=10)

    # Grade Level & Section
    tk.Label(form_frame, text="Grade Level", font=('Arial', 14), bg="#ecf0f1").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    grade_combo = ttk.Combobox(form_frame, values=[], width=25, state="readonly")
    grade_combo.grid(row=0, column=1, padx=5, pady=5)
    grade_combo.bind("<<ComboboxSelected>>", refresh_data)

    tk.Label(form_frame, text="Section", font=('Arial', 14), bg="#ecf0f1").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    section_combo = ttk.Combobox(form_frame, values=[], width=25, state="readonly")
    section_combo.grid(row=0, column=3, padx=5, pady=5)
    section_combo.bind("<<ComboboxSelected>>", update_section)

    tk.Button(form_frame, text="Add Section", command=open_section_window, font=('Arial', 10), bg="#2c3e50", fg="white").grid(row=0, column=4, padx=5, pady=5)


    # Adviser, Subject, Teacher
    tk.Label(form_frame, text="Adviser", font=('Arial', 14), bg="#ecf0f1").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    adviser_entry = tk.Entry(form_frame, state=tk.DISABLED, font=('Arial', 14))
    adviser_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Subject", font=('Arial', 14), bg="#ecf0f1").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    subject_combo = ttk.Combobox(form_frame, values=[], width=25, state="readonly")
    subject_combo.grid(row=1, column=3, padx=5, pady=5)
    tk.Button(form_frame, text="Add Subject", command=open_subject_window, font=('Arial', 10), bg="#2c3e50", fg="white").grid(row=1, column=4, padx=5, pady=5)

    # Teacher - Align with Grade Level & Section
    tk.Label(form_frame, text="Teacher", font=('Arial', 14), bg="#ecf0f1").grid(row=0, column=5, sticky="w", padx=5, pady=5)
    teacher_combo = ttk.Combobox(form_frame, values=[], width=25, state="readonly")
    teacher_combo.grid(row=0, column=6, padx=5, pady=5)
    tk.Button(form_frame, text="Add Teacher", command=open_teacher_window, font=('Arial', 10), bg="#2c3e50", fg="white").grid(row=0, column=7, padx=5, pady=5)




 # Create a new frame to hold Time From, Time To, and Buttons in a single row
    time_button_frame = tk.Frame(form_frame, bg="#ecf0f1")
    time_button_frame.grid(row=2, column=0, columnspan=8, sticky="w", pady=10)  # Positioned below Adviser label

    # Time From Label and Inputs
    tk.Label(time_button_frame, text="Time From", font=('Arial', 12, 'bold'), bg="#ecf0f1").pack(side="left", padx=5)

    time_from_hour = tk.Spinbox(time_button_frame, from_=1, to=12, width=3)
    time_from_minute = tk.Spinbox(time_button_frame, from_=0, to=59, width=3)
    time_from_period = ttk.Combobox(time_button_frame, values=["AM", "PM"], width=3, state="readonly")
    time_from_period.set("AM")

    time_from_hour.pack(side="left", padx=(0, 2))
    time_from_minute.pack(side="left", padx=(2, 2))
    time_from_period.pack(side="left", padx=(2, 15))  # Increased spacing

    # Time To Label and Inputs
    tk.Label(time_button_frame, text="Time To", font=('Arial', 12, 'bold'), bg="#ecf0f1").pack(side="left", padx=5)

    time_to_hour = tk.Spinbox(time_button_frame, from_=1, to=12, width=3)
    time_to_minute = tk.Spinbox(time_button_frame, from_=0, to=59, width=3)
    time_to_period = ttk.Combobox(time_button_frame, values=["AM", "PM"], width=3, state="readonly")
    time_to_period.set("PM")

    time_to_hour.pack(side="left", padx=(0, 4))
    time_to_minute.pack(side="left", padx=(2, 2))
    time_to_period.pack(side="left", padx=(2, 40))  # Increased spacing before buttons

    # Frame for Buttons (to move them to the right)
    button_frame = tk.Frame(time_button_frame, bg="#ecf0f1")
    button_frame.pack(side="left", padx=50)  # Moves buttons further right

    # Submit and Print Buttons (Smaller and adjusted to the right)
    tk.Button(button_frame, text="Submit", command=scheduling_insert_data, font=('Arial', 10), bg="#27ae60", fg="white", width=15).pack(side="left", padx=5)
    tk.Button(button_frame, text="Print Schedule", command=print_schedule, font=('Arial', 10), bg="#3498db", fg="white", width=15).pack(side="left", padx=5)

    # Move the check buttons to the right side, above the teacher selection
    # Move Day Selection Below Teacher
    # Day - Align with Adviser & Subject
    tk.Label(form_frame, text="Day", font=('Arial', 14), bg="#ecf0f1").grid(row=1, column=5, sticky="w", padx=5, pady=5)

    day_frame = tk.Frame(form_frame, bg="#ecf0f1")
    day_frame.grid(row=1, column=6, columnspan=2, sticky="w")

    # Creating day check buttons
    mon_var = tk.BooleanVar()
    tk.Checkbutton(day_frame, text="M", variable=mon_var).pack(side="left", padx=2)
    tue_var = tk.BooleanVar()
    tk.Checkbutton(day_frame, text="T", variable=tue_var).pack(side="left", padx=2)
    wed_var = tk.BooleanVar()
    tk.Checkbutton(day_frame, text="W", variable=wed_var).pack(side="left", padx=2)
    thu_var = tk.BooleanVar()
    tk.Checkbutton(day_frame, text="Th", variable=thu_var).pack(side="left", padx=2)
    fri_var = tk.BooleanVar()
    tk.Checkbutton(day_frame, text="F", variable=fri_var).pack(side="left", padx=2)


    # TreeView Frame
    tree_frame = tk.Frame(scheduling_frame, bg="#ecf0f1")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("ID", "Subject", "Time", "Day", "Grade_level", "Section", "Teacher")
    scheduling_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
    scheduling_tree.pack(side="left", fill="both", expand=True)


    for col in ("ID", "Subject", "Time", "Day", "Grade_level", "Section", "Teacher"):
        scheduling_tree.heading(col, text=col)
        scheduling_tree.column(col, width=100, anchor='center')



        # Scrollbars
    scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=scheduling_tree.yview)
    scroll_y.pack(side="right", fill="y")
    scheduling_tree.configure(yscrollcommand=scroll_y.set)

    sections = get_sections()
    grade_levels = get_grade_levels()
    teachers = get_teachers()
    subject_combo['values'] = get_subjects_by_grade_level(grade_levels[0]) if grade_levels else []
    grade_combo['values'] = grade_levels
    section_combo['values'] = sections
    teacher_combo['values'] = teachers

#=====================================================LOAD DATA ON TABLE===========================================  
    create_new_user_frame()      
    create_updates_view()
    create_studentml_view()
    create_admission_view()
    create_admitted_view()
    create_interview_view()
    ensure_connection()


    add_top_right_label(new_user_frame)
    add_top_right_label(dashboard_frame)
    add_top_right_label(admission_frame)
    add_top_right_label(scheduling_frame)
    add_top_right_label(cashier_frame)
    add_top_right_label(updates_frame)
    add_top_right_label(table_frame)
    add_top_right_label(interview_frame)
    add_top_right_label(admitted_frame)
    add_top_right_label(studentml_frame)

    show_dashboard_panel()
    def auto_refresh():
        ensure_connection()
        if dashboard_frame.winfo_viewable():
            update_student_count()
        elif admission_frame.winfo_viewable():
            load_admission_data()
        elif cashier_frame.winfo_viewable():
            load_cashier_data()
        elif admitted_frame.winfo_viewable():
            load_admitted_data()
        elif updates_frame.winfo_viewable():
            load_updates_data()
        elif table_frame.winfo_viewable():
            load_data()
        elif studentml_frame.winfo_viewable():
            load_studentml_data()
        elif scheduling_frame.winfo_viewable():
            load_scheduling_data()
        elif interview_frame.winfo_viewable():
            load_interview_data("pending")
        main_root.after(5000, auto_refresh)

    auto_refresh()
    main_root.mainloop()
    
    

