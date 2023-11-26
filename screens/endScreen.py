import tkinter as tk
import screens.mainScreen as mainScreen
class EndScreen(tk.Frame):
    def __init__(self,master):
        super().__init__(bg="#ECF4D6")
        self.master = master
        self.message = self.master.endMessage
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self,text=self.message,font=("Helvetica", 15,"bold"),bg="#ECF4D6").pack()
        tk.Button(self,text="Play Again",command=self.play_again).pack()
        tk.Button(self,text="Quit",command=self.quit).pack()

    def play_again(self):
        self.master.endMessage = None
        self.master.switch_frame(mainScreen.MainScreen)