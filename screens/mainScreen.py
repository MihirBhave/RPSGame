import tkinter as tk
from tkinter import ttk
from screens.oppComp import PlayVsBot
from screens.oppPlayer import PlayVsPlayer

class MainScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, background="#05e8d5")
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.add_widgets()


    def add_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10)

        welcome_label = tk.Label(self, text=f"Welcome, {self.master.username}!", font=("Comic Sans MS", 26), bg="#05e8d5", fg="#000000")

        #self.title_label = tk.Label(self, text="Welcome to Rock, Paper, Scissors!", font=("Helvetica", 16), bg="#74c7b8")
        welcome_label.pack(side="top", pady=50)

        self.bot_button = ttk.Button(self, text="Play vs Bot", command=self.play_vs_bot, style="TButton")
        self.bot_button.pack(side="top", pady=50)
        
        self.player_button = ttk.Button(self, text="Play vs Player", command=self.play_vs_player, style="TButton")
        self.player_button.pack(side="top")


    def play_vs_bot(self):
        self.master.switch_frame(PlayVsBot)

    def play_vs_player(self):
        self.master.switch_frame(PlayVsPlayer)