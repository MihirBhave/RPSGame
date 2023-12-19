import tkinter as tk
import screens.mainScreen as mainScreen
class EndScreen(tk.Frame):
    def __init__(self,master):
        super().__init__(bg="#05e8d5")
        self.master = master
        self.title = self.master.endTitle
        self.message = self.master.endMessage
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text=self.title, font=("Comic Sans MS", 20, "bold"), bg="#05e8d5")
        title_label.pack(pady=(20, 10))

        message_label = tk.Label(self, text=self.message, font=("Comic Sans MS", 15, "bold"), bg="#05e8d5")
        message_label.pack(pady=10)

        play_again_button = tk.Button(self, text="Play Again", command=self.play_again, bg="#4CAF50", fg="white", padx=20, pady=10)
        play_again_button.pack(pady=10)

        quit_button = tk.Button(self, text="Quit", command=self.quit, bg="#f44336", fg="white", padx=20, pady=10)
        quit_button.pack(pady=10)

        # Configure pack to expand and fill both X and Y directions
        self.pack(expand=True, fill="both")

    def play_again(self):
        self.master.endTitle = None
        self.master.endMessage = None
        self.master.switch_frame(mainScreen.MainScreen)