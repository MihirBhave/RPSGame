import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os
from handlers.player import PlayerHandler

class PlayVsPlayer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#05e8d5")
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.handler = PlayerHandler(self.master, self)

    def create_widgets(self):

        self.imgs = [
            ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "images\\rock.jpeg")).resize((200,200))),
            ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "images\\paper.jpeg")).resize((200,200))),
            ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "images\\scissor.jpeg")).resize((200,200))),
        ]

        self.oppImgs = [
            ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "images\\rock.jpeg")).resize((200,200)).transpose(Image.FLIP_LEFT_RIGHT)),
            ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "images\\paper.jpeg")).resize((200,200)).transpose(Image.FLIP_LEFT_RIGHT)),
            ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "images\\scissor.jpeg")).resize((200,200)).transpose(Image.FLIP_LEFT_RIGHT)),
        ]

        # Blank Image to display at the start and when no one has played.
        self.blankImg = ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "images\\blank.jpg")).resize((200,200)))
        # Pack all the labels

        player_label = ttk.Label(self, image=self.blankImg)
        computer_label = ttk.Label(self, image=self.blankImg)

        player_label.grid(row=1,column=0)
        computer_label.grid(row=1,column=4)
        
        ttk.Label(self,text=f"{self.master.username}",font=("Comic Sans MS", 15,"bold"), background="#05e8d5").grid(row=0,column=1)
        opp_name = ttk.Label(self,text="Opponent",font=("Comic Sans MS", 15,"bold"), background="#05e8d5")
        opp_name.grid(row=0,column=3)
        ttk.Label(self,text="SCORE",font=("Comic Sans MS", 15,"bold"), background="#05e8d5").grid(row=0,column=2)

        player_score = ttk.Label(self, text="0", font=("Helvetica", 15,"bold"))
        computer_score = ttk.Label(self, text="0", font=("Helvetica", 15,"bold"))
        
        player_score.grid(row=1,column=1)
        computer_score.grid(row=1,column=3)
    
        self.labels = [player_label, computer_label, player_score, computer_score]
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 15,"bold"), padding=(10, 5),background="#FFB6C1",foreground="#5A5A5A",width=15,height=8)

        rockbtn = ttk.Button(self,text="ROCK",command=lambda: self.handler.handle_click("r"),style="TButton")
        paperbtn = ttk.Button(self,text="PAPER",command=lambda: self.handler.handle_click("p"),style="TButton")
        scissorbtn = ttk.Button(self,text="SCISSOR",command=lambda: self.handler.handle_click("s"),style="TButton")
        # Add the buttons to the frame.
        rockbtn.grid(row=2,column=1)
        paperbtn.grid(row=2,column=2)
        scissorbtn.grid(row=2,column=3)

        self.oppLabel = opp_name
        self.buttons = [rockbtn, paperbtn, scissorbtn]

   