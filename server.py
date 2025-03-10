import socket
from _thread import *

HOST = "0.0.0.0"
PORT = 5555

connected = set()
games = {}
connected_ids = 0

def client_thread(connection, p_id, game_id):
    end_reason = None # Reason for ending the game
    opp_id = 0 if p_id == 1 else 1

    '''
    Message Sending Format:
    FIRST;player_id;player_username
    FORFEIT;
    UPDATE;move
    '''

    '''
    Message Receiving Format:
    PING
    CONNECTED
    MOVE;move
    END;
    '''

    # Send the player id to the client only after the opponent has connected.
    try:
        while not games[game_id][p_id]["paired"]:
            continue

    except Exception:
        pass

    connection.send(f"FIRST;{p_id+1};{games[game_id][opp_id]['username']}".encode())

    while True:
        try:
            data = connection.recv(2048).decode()
            if not data:
                # The client has disconnected.
                break

            if game_id in games:
                game = games[game_id]
                msg_type = data.split(";")[0]

                if msg_type == "MOVE":
                    move = data.split(";")[1]
                    game[p_id]["move"] = move
                    if game[opp_id]["move"] is not None:
                        # Both the players have made their moves.
                        # Send the moves to both the players.
                        game[opp_id]["conn"].send(f"UPDATE;{game[p_id]['move']}".encode())
                        game[p_id]["conn"].send(f"UPDATE;{game[opp_id]['move']}".encode())
    
                        # Reset the moves
                        game[p_id]["move"] = None
                        game[opp_id]["move"] = None
                        

                elif msg_type == "END":
                    end_reason = "OVER"
                    connection.close()
                    game[opp_id]["conn"].close()

                if game[p_id]["move"] is not None and game[opp_id]["move"] is not None:
                    # Reset the moves for both players
                    game[p_id]["move"] = None
                    game[opp_id]["move"] = None

            else:
                break           

        except Exception as e:
            print(e)
            break

    print(f"[-] Player {p_id+1} has disconnected!")
    try:
        if end_reason == None:
            # The player has disconnected.
            games[game_id][opp_id]["conn"].send("FORFEIT;".encode())
        else:
            print("[+] Game Over!")
        del games[game_id]
    except:
        pass



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: # Get the server up and running
    s.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

s.listen(2) # Accept 2 connections at a time and queue the others

print("[+] Server has started!")

while True:
    connection, address= s.accept()

    first_msg = connection.recv(2048).decode()
    if(first_msg == "PING"):
        # This was by the server detector, so ignore it.
        connection.close()
        continue

    print(f'[+] Connected to {address} !')

    connected_ids += 1
    game_id = (connected_ids - 1) // 2
    p = 0 # Player Display ID

    if connected_ids % 2 == 1:
        games[game_id] = {
            0 : {
                "move": None,
                "paired": False,
                "conn": connection,
                "username": first_msg
            }
        }
        print("[+] Creating a new game...")

    else:
        games[game_id][1] = {
            "move": None,
            "paired": True,
            "conn": connection,
            "username": first_msg
        }

        games[game_id][0]["paired"] = True # Set the paired status of player1 to True
        p  = 1 # Player Display ID

    start_new_thread(client_thread, (connection, p, game_id)) # Start the thread!
     


