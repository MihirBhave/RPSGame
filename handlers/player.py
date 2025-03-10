import socket
import time
import tkinter as tk
import threading
from tkinter import ttk
import screens.endScreen as EndScreen

PORT = 5555

p_moves = {"r": 0, "p": 1, "s": 2}
points = [0, 0]


class PlayerHandler:
    def __init__(self, master, frame):
        self.master = master
        self.frame = frame
        self.labels = frame.labels
        self.buttons = frame.buttons
        self.notif_label = ttk.Label(
            self.frame, text="Pairing", font=("Helvetica", 20, "bold"), foreground="red"
        )
        self.notif_label.grid(row=1, column=2)
        self.player_move = None
        self.opponent_move = None

        self.toggle_buttons(tk.DISABLED)
        self.connect()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.master.HOST, PORT))
            self.client.send(f"{self.master.username}".encode()) # Send this first message to differentiate from detect server connection. ( Username)
            self.stop_event = threading.Event()
            self.receive_thread = threading.Thread(target=self.receive)
            self.receive_thread.start()

            print("[+] Connected to the server!")

        except Exception as e:
            print(e)
            print(
                "[-] Error while connecting to the server! Attempting again in 3 seconds..."
            )
            time.sleep(3)
            self.connect()
            return None

    def receive(self):
        while not self.stop_event.is_set():
            try:
                data = self.client.recv(1024).decode()
                if not data:
                    # The server has disconnected.
                    break

                msg_type = data.split(";")[0]
                
                if msg_type == "FIRST":
                    self.player_id = data.split(";")[1]
                    self.master.oppName = data.split(";")[2]
                    self.frame.oppLabel.config(text=self.master.oppName)
                    self.master.after(0, self.toggle_buttons, tk.NORMAL)
                    self.master.after(0, self.show_notif, "Start!")

                elif msg_type == "UPDATE":
                    move = data.split(";")[1]
                    #print("Opponent has played!")
                    self.master.after(0, self.update,move, True)

                elif msg_type == "FORFEIT":
                    # The other player has disconnected.
                    self.master.endMessage = "Opponent has disconnected!"
                    self.client.close()
                    self.master.switch_frame(EndScreen.EndScreen)
                    break

            except Exception as e:
                #print(e)
                self.stop_event.set()  # Stop the thread.
                break

    def send(self, message):
        try:
            self.client.send(message.encode())
        except:
            print("[-] Error while sending message to the server!")
            return None

    def handle_click(self, choice):
        self.master.after(0, self.update, choice, False)
        self.send(f"MOVE;{choice}")

    def update(self, move, opp):

        if opp == False:

            # Player has played.
            self.player_move = p_moves[move]
            self.toggle_buttons(tk.DISABLED)
            self.labels[0].config(image=self.frame.imgs[self.player_move])

        else:
            self.opponent_move = p_moves[move]
            self.labels[1].config(image=self.frame.oppImgs[self.opponent_move])
            self.master.after(500, self.determine_winner)

    def toggle_buttons(self, state):
        for btn in self.buttons:
            btn["state"] = state

    def determine_winner(self):
        winner = ""
        if self.player_move == self.opponent_move:
            winner = "Tie"
            self.master.after(0, self.show_notif, "Tie!")

        elif self.player_move == 0 and self.opponent_move == 1:
            winner = "Opponent"
            self.master.after(0, self.show_notif, "Whoops!")

        elif self.player_move == 0 and self.opponent_move == 2:
            winner = "Player"
            self.master.after(0, self.show_notif, "Yay!")

        elif self.player_move == 1 and self.opponent_move == 0:
            winner = "Player"
            self.master.after(0, self.show_notif, "Yay!")

        elif self.player_move == 1 and self.opponent_move == 2:
            winner = "Opponent"
            self.master.after(0, self.show_notif, "Whoops!")

        elif self.player_move == 2 and self.opponent_move == 0:
            winner = "Opponent"
            self.master.after(0, self.show_notif, "Whoops!")

        elif self.player_move == 2 and self.opponent_move == 1:
            winner = "Player"
            self.master.after(0, self.show_notif, "Yay!")

        self.master.after(0, self.update_stats, winner)

    def update_stats(self, result):
        if result == "Player":
            points[0] += 1

        elif result == "Opponent":
            points[1] += 1

        # Update the scores too!
        self.labels[2].config(text=points[0])
        self.labels[3].config(text=points[1])
        self.master.after(500, self.reset)

    def show_notif(self, msg):
        self.notif_label.config(text=msg)
        self.notif_label.grid(row=1, column=2)
        try:
            self.master.after(500, self.hide_notif)

        except tk.TclError as e:
            pass
    
    def hide_notif(self):
        try:
            self.notif_label.grid_remove()

        except tk.TclError as e:
            # Ignore it as it occurs when the frame is switched.
            pass

    def reset(self):
        self.player_move = None
        self.opponent_move = None
        self.labels[0].config(image=self.frame.blankImg)
        self.labels[1].config(image=self.frame.blankImg)
        self.toggle_buttons(tk.NORMAL)
        self.master.after(0, self.show_notif, "Play!")
        self.master.after(200, self.check_end) #Give a slight delay.

    def check_end(self):
        end = False

        if points[0] == 5:
            self.master.endTtle = "You Won!"
            self.master.endMessage = f"You won against your opponent by {points[0]}-{points[1]}! "
            end = True
            self.master.switch_frame(EndScreen.EndScreen)
        elif points[1] == 5:
            self.master.endTitle = "You Lost!"
            self.master.endMessage = f"You lost against your opponent by {points[0]}-{points[1]} ! "
            end = True
            self.master.switch_frame(EndScreen.EndScreen)

        if end == True and self.player_id == "1":
            self.send("END;") # Let the server know that the game is over.


            


