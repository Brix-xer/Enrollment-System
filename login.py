import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import Admin
import Registrar
import Interviewer
import TeacherAccount
import Cashier
import subprocess
from datetime import datetime

try:
    connection = mysql.connector.connect(
        host="145.223.108.159",
        user="u507702827_hiholc",
        password="Hiholearningcenter123",
        database="u507702827_hihodatabase"
    )
    cursor = connection.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to database: {err}")
    exit()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def check_login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    
    if username == "Enter username" or password == "Enter password" or username == "" or password == "":
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return
    
    try:
        cursor.execute("SELECT permission FROM logininfo WHERE username=%s AND pass=%s", (username, password))
        user = cursor.fetchone()
        
        if user:
            account_type = user[0].strip().lower()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("UPDATE logininfo SET last_log = %s WHERE username = %s", (current_time, username))
            connection.commit()

            root.withdraw()
            
            if account_type == "admin":
                Admin.open_main_gui()
                Admin.ensure_connection()
            elif account_type == "registrar":
                Registrar.open_main_gui()
                Registrar.ensure_connection()
            elif account_type == "cashier":
                Cashier.open_main_gui()
                Cashier.ensure_connection()
            elif account_type == "interviewer":
                Interviewer.open_main_gui()
                Interviewer.ensure_connection()
            elif account_type == "teacher":
                TeacherAccount.open_main_gui()
                TeacherAccount.ensure_connection()
            else:
                messagebox.showerror("Login Failed", f"Unknown account type: {account_type}. Please contact support.")
                root.deiconify()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            root.deiconify()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error during login: {err}")
        root.deiconify()


# Function to handle placeholder text
def on_entry_click(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.config(fg='black')

def on_focusout(event, entry, default_text):
    if entry.get().strip() == '':
        entry.insert(0, default_text)
        entry.config(fg='grey')

# Main Window
root = tk.Tk()
root.title("Login")
root.overrideredirect(True)  # Removes window decorations (title bar, minimize, maximize, close)
width, height = 900, 500
center_window(root, width, height)
root.configure(bg="#f0f0f0")

# Custom Close Button
def close_app():
    root.destroy()

btn_close = tk.Button(root, text="X", command=close_app, font=("Arial", 12, "bold"), bg="red", fg="white", relief="flat", width=3)
btn_close.place(relx=0.95, rely=0.02)

# Load and set background image
try:
    bg_image = Image.open("images/ribbon.png")
    bg_image = bg_image.resize((900, 500), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    print(f"Error loading background image: {e}")

# Username Label
username_label = tk.Label(root, text="Username", font=("Arial", 12, "bold"), bg="#f0f0f0")
username_label.place(relx=0.62, rely=0.46)

# Username Frame
username_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
username_frame.place(relx=0.62, rely=0.51)

username_icon = tk.Label(username_frame, text="👤", font=("Arial", 16), bg="white")
username_icon.pack(side="left", padx=5)

entry_username = tk.Entry(username_frame, font=("Arial", 13), bd=0, width=20, fg='black')
entry_username.pack(side="right", padx=5)

# Password Label
password_label = tk.Label(root, text="Password", font=("Arial", 12, "bold"), bg="#f0f0f0")
password_label.place(relx=0.62, rely=0.60)

# Password Frame
password_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
password_frame.place(relx=0.62, rely=0.65)

password_icon = tk.Label(password_frame, text="🔒", font=("Arial", 16), bg="white")
password_icon.pack(side="left", padx=5)

entry_password = tk.Entry(password_frame, font=("Arial", 13), bd=0, width=20, fg='black', show="*")
entry_password.pack(side="right", padx=5)

# Login Button
btn_login = tk.Button(root, text="Login", command=check_login, font=("Arial", 12, "bold"), bg="#000a2e", fg="white", relief="flat", width=18)
btn_login.place(relx=0.64, rely=0.75)

def close_app():
    root.destroy()

def on_enter(event):
    btn_close.config(bg="#ff0000")  # Change background color to a brighter red on hover

def on_leave(event):
    btn_close.config(bg="#c60f05")  # Change background color back to the original color

btn_close = tk.Button(root, text="X", command=close_app, font=("Arial", 8, "bold"), bg="#c60f05", fg="white", relief="flat", width=3)
btn_close.place(relx=0.95, rely=0.02)

# Bind the hover events
btn_close.bind("<Enter>", on_enter)
btn_close.bind("<Leave>", on_leave)

# Function to enable Enter key to trigger login
def on_enter(event):
    check_login()

root.bind('<Return>', on_enter)
root.mainloop()

