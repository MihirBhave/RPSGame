import tkinter as tk
from tkinter import messagebox
import pickle
from screens.mainScreen import MainScreen

class AuthScreen(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.configure(bg="#3498db") 
        self.pack(fill=tk.BOTH, expand=True)

        self.credentials = {}

        # Check if credentials file exists and load
        try:
            with open("credentials.pkl", "rb") as file:
                self.credentials = pickle.load(file)
        except FileNotFoundError:
            pass  # File doesn't exist, create an empty dictionary

        self.show_login()

    def show_login(self):
        username_label = tk.Label(self, text="Username:", font=("Helvetica", 12), bg="#3498db", fg="#ecf0f1")
        username_label.pack(pady=5)

        username_entry = tk.Entry(self, font=("Helvetica", 12))
        username_entry.pack(pady=5)

        password_label = tk.Label(self, text="Password:", font=("Helvetica", 12), bg="#3498db", fg="#ecf0f1")
        password_label.pack(pady=5)

        password_entry = tk.Entry(self, show='*', font=("Helvetica", 12))
        password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Login", command=lambda: self.authenticate(username_entry.get(), password_entry.get()), bg="#2ecc71", fg="#ecf0f1")
        login_button.pack(pady=10)

        signup_button = tk.Button(self, text="Sign Up", command=lambda: self.create_account(username_entry.get(), password_entry.get()), bg="#f39c12", fg="#ecf0f1")
        signup_button.pack()

    def show_welcome(self, username):
        # Display welcome message
        self.master.username = username
        self.master.switch_frame(MainScreen)

    def authenticate(self, username, password):
        # Authenticate user
        if username in self.credentials and self.credentials[username] == password:
            self.show_welcome(username)
        else:
            self.master.switch_frame(AuthScreen)

    def create_account(self, username, password):
        # Create a new account
        if username not in self.credentials:
            self.credentials[username] = password

            # Save updated credentials to a file
            with open("credentials.pkl", "wb") as file:
                pickle.dump(self.credentials, file)

            self.show_welcome(username)
        else:
            messagebox.showerror("Sign Up Failed", "Username already exists")



