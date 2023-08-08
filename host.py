import socket
import requests
import uuid
from datetime import datetime
import tkinter as tk
import configparser
import threading

# Initialize the configparser
config = configparser.ConfigParser()

# Read the config file
config.read('settings.ini')

db_host = config.get('Host', 'host_ip')
db_port = config.getint('Host', 'port')

gamer_ips = []
for section in config.sections():
    if section.startswith("Computer_"):
        gamer_ip = config.get(section, 'ip')
        gamer_ips.append(gamer_ip)


def get_unique_id():
    return str(uuid.getnode())  # This gets the MAC address as the unique ID


def send_command_to_gamer_pc(ip, command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, db_port))
            s.sendall(command.encode())
        print("Command sent:", command)
    except Exception as e:
        print("Error:", e)


def send_command_to_all_gamer_pcs(command):
    for ip in gamer_ips:
        send_command_to_gamer_pc(ip, command)


def send_post_request():
    url = "https://vip.vr360action.com/machines/getServerTime"
    unique_id = get_unique_id()
    data = {"uuid": unique_id}

    response = requests.post(url, json=data)
    if response.status_code == 200:
        server_time = response.json()["serverTime"]
        server_time = server_time[11:19]
        local_time = datetime.now().strftime("%H:%M:%S")
        time_difference = calc_time_diff(server_time, local_time)
        return f"Time difference with server: {time_difference} seconds"
    else:
        return "Error: Failed to get server time"


def update_time_difference_label(time_difference_label):
    time_difference = send_post_request()
    time_difference_label.config(text=f"{time_difference}")


def calc_time_diff(time1, time2):
    time_format = "%H:%M:%S"
    time1 = datetime.strptime(time1, time_format)
    time2 = datetime.strptime(time2, time_format)
    time_difference = time1 - time2
    return time_difference


def handle_gamer_connection(connection, address):
    print("Connected to gamer PC at {}:{}".format(*address))

    while True:
        # Receive commands from the host
        command = connection.recv(1024).decode('utf-8')

        if not command:
            # If the connection is closed, exit the loop
            break

        # Process the command and update the GUI (dummy logic)
        if command == 'START_GAME':
            # Your code to update the GUI in gamer.py when the game starts
            print("Starting the game on gamer PC at {}:{}".format(*address))
            # Add code to update the GUI in gamer.py here

    connection.close()


def accept_gamer_connections():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((db_host, db_port))
    server_socket.listen()

    while True:
        connection, address = server_socket.accept()
        gamer_thread = threading.Thread(target=handle_gamer_connection, args=(connection, address))
        gamer_thread.start()


def main():
    root = tk.Tk()
    root.title("Host PC")

    start_game_button = tk.Button(root, text="Start Game", command=lambda: send_command_to_all_gamer_pcs("START_GAME"))
    start_game_button.pack(pady=10)

    time_difference_label = tk.Label(root, text="", fg="black")
    time_difference_label.pack(pady=20)
    update_time_difference_label(time_difference_label)

    accept_thread = threading.Thread(target=accept_gamer_connections)
    accept_thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
