import socket
import requests
import uuid
from datetime import datetime
import tkinter as tk
import settings

# Replace this with the IPs of the gamer PCs/Check setting.py to change
gamer_pc1_ip = settings.pc_1
gamer_pc2_ip = settings.pc_2

# Function to get a unique identifier (UUID) for the host PC
def get_unique_id():
    return str(uuid.getnode())  # This gets the MAC address as the unique ID

def send_command_to_gamer_pc(ip, command):
    # Create a socket (AF_INET for IPv4, SOCK_STREAM for TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the gamer PC
        s.connect((ip, settings.port))  # Replace settings.port with the desired port number

        # Send the command to the gamer PC
        s.sendall(command.encode())

def send_start_game_command():
    try:
        send_command_to_gamer_pc(gamer_pc1_ip, "START_GAME")
        send_command_to_gamer_pc(gamer_pc2_ip, "START_GAME")
        # You can add more gamer PCs here if needed
        print("Command sent: START_GAME")
    except Exception as e:
        print("Error:", e)

# Function to get server time and display time difference
def send_post_request():
    url = "https://vip.vr360action.com/machines/getServerTime"
    unique_id = get_unique_id()
    data = {"uuid": unique_id}

    # Send the POST request and handle the response
    response = requests.post(url, json=data)
    if response.status_code == 200:
        server_time = response.json()["serverTime"]
        server_time = server_time[11:19]
        local_time = datetime.now() # Get the local time using the time module
        local_time = local_time.strftime("%H:%M:%S")
        time_difference = calc_time_diff(server_time, local_time)
        return(f"Time difference with server: {time_difference} seconds")
    else:
        return("Error: Failed to get server time")

def update_time_difference_label(time_difference_label):
    time_difference = send_post_request()
    time_difference_label.config(text=f"{time_difference}")

def calc_time_diff(time1, time2):
        time_format = "%H:%M:%S"
        time1 = datetime.strptime(time1, time_format)
        time2 = datetime.strptime(time2, time_format)
        time_difference = time1 - time2
        return time_difference

def main():
    # GUI setup
    root = tk.Tk()
    root.title("Host PC")

    start_game_button = tk.Button(root, text="Start Game", command=send_start_game_command)
    start_game_button.pack(pady=10)

    time_difference_label = tk.Label(root, text="", fg="black")
    time_difference_label.pack(pady=20)
    update_time_difference_label(time_difference_label)  # Initially update the label text
    root.mainloop()



if __name__ == "__main__":
    main()
