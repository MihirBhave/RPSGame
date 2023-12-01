import tkinter as tk
import random
import screens.endScreen as EndScreen
from tkinter import ttk

class BotGameHandler:
    def __init__(self,frame,master):
        self.master = master
        self.frame = frame
        self.points = [0,0]
        self.buttons = frame.buttons
        self.labels = frame.labels
        self.Player_played = False
        self.Bot_played = False
        self.player_choice = None
        self.bot_choice = None
        self.choices = ["rock","paper","scissor"]
        self.notif_label = ttk.Label(self.frame,text="",font=("Helvetica", 20,"bold"), foreground="red")
        self.show_notif("Start!")

    def handle_click(self,choice):
        self.Player_played = True
        for btn in self.buttons:
            btn["state"] = tk.DISABLED


        self.player_choice = self.choices.index(choice)
        self.labels[0].config(image=self.frame.imgs[self.player_choice])
        self.master.after(1000, self.bot_play)

    def bot_play(self):
        if not self.Bot_played:
            self.bot_choice = random.randint(0,2)
            self.labels[1].config(image=self.frame.oppImgs[self.bot_choice])
            self.Bot_played = True
            self.master.after(1000, self.determine_winner)

    def determine_winner(self):
        if self.player_choice == self.bot_choice:
            winner = "Tie"
            self.show_notif("Tie!")

        elif self.player_choice == 0 and self.bot_choice == 1:
            winner = "Bot"
            self.show_notif("Whoops!")

        elif self.player_choice == 0 and self.bot_choice == 2:
            winner = "Player"
            self.show_notif("Yay!")
    
        elif self.player_choice == 1 and self.bot_choice == 0:
            winner = "Player"
            self.show_notif("Yay!")
        
        elif self.player_choice == 1 and self.bot_choice == 2:
            winner = "Bot"
            self.show_notif("Whoops!")
        
        elif self.player_choice == 2 and self.bot_choice == 0:
            winner = "Bot"
            self.show_notif("Whoops!")
        
        elif self.player_choice == 2 and self.bot_choice == 1:
            winner = "Player"
            self.show_notif("Yay!")

        self.update_stats(winner)

    def update_stats(self,result):
        if result == "Tie":
            pass # Nobody gets a point.

        elif result == "Player":
            self.points[0] += 1

        elif result == "Bot":
            self.points[1] += 1

        self.labels[2].config(text=str(self.points[0]))
        self.labels[3].config(text=str(self.points[1])) # Update the scores.

        self.master.after(1000, self.reset)

    def reset(self):

        self.Player_played = False
        self.Bot_played = False
        self.player_choice = None
        self.bot_choice = None

        for btn in self.buttons:
            btn["state"] = tk.NORMAL

        self.labels[0].config(image=self.frame.blankImg)
        self.labels[1].config(image=self.frame.blankImg)

        self.master.after(700, self.check_end)
    def check_end(self):
        if self.points[0] == 5:
            self.master.endTitle = "You Won!"
            self.master.endMessage = f"You won against the computer by {self.points[0]}-{self.points[1]} !"
            self.master.switch_frame(EndScreen.EndScreen)
        elif self.points[1] == 5:
            self.master.endTitle = "You Lost!"
            self.master.endMessage = f"You lost against the computer by {self.points[0]}-{self.points[1]} !"
            self.master.switch_frame(EndScreen.EndScreen)    

    def show_notif(self, message):
        self.notif_label.config(text=message)
        self.notif_label.grid(row=1,column=2)
        self.master.after(500, self.notif_label.grid_remove)  # Remove the label after 0.5 seconds.


    