import socket
import tkinter as tk
import configparser
import threading

# Initialize the configparser
config = configparser.ConfigParser()

# Read the config file
config.read('settings.ini')

# Accessing variables from the config file
db_host = config.get('Host', 'host_ip')
db_port = config.getint('Host', 'port')

def handle_connection(connection):
    while True:
        # Receive commands from the host
        command = connection.recv(1024).decode('utf-8')

        if not command:
            # If the connection is closed, exit the loop
            break

        # Process the command and update the GUI (dummy logic)
        if command == 'START_GAME':
            # Your code to update the GUI here
            print("Starting the game on gamer PC")
            update_gui("Game started!")  # Call the update_gui function with the new information

    print("Disconnected from host")
    connection.close()

def update_gui(new_info):
    # Your code to update the GUI here
    # For example, if you have a label to display the information
    info_label.config(text=new_info)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gamer PC")

    # Your GUI code here
    info_label = tk.Label(root, text="Waiting for game start...")
    info_label.pack(pady=20)

    root.mainloop()
