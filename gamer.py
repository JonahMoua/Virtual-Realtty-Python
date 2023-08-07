import socket
import tkinter as tk
import threading
import configparser

# Initialize the configparser
config = configparser.ConfigParser()

# Read the config file
config.read('settings.ini')

# Accessing variables from the config file
db_host = config.get('Host', 'host_ip')
db_port = config.getint('Host', 'port')

host_ip_address = db_host  # Replace with the IP of the host PC

def listen_for_commands():
    # Create a socket (AF_INET for IPv4, SOCK_STREAM for TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the gamer PC's IP and desired port number
        s.bind((db_host, db_port))  # Replace settings.port with the same port number used in host.py
        s.listen()

        print("Waiting for commands...")
        while True:
            conn, addr = s.accept()
            with conn:
                print("Received command from host:", conn.recv(1024).decode())
                # Process the received command here (e.g., change UI element, start/stop game, etc.)

def update_gui():
    # Function to update the GUI icon based on the communication status
    if communication_status.get():
        status_label.config(text="Communication: Successful", fg="green")
    else:
        status_label.config(text="Communication: Failed", fg="red")
    root.after(5000, update_gui)  # Update the GUI every 5 seconds

def start_listening():
    listen_thread = threading.Thread(target=listen_for_commands)
    listen_thread.daemon = True
    listen_thread.start()
    update_gui()  # Start updating the GUI

# GUI setup
root = tk.Tk()
root.title("Gamer PC Communication Status")

communication_status = tk.BooleanVar()
communication_status.set(False)

status_label = tk.Label(root, text="Communication: Initializing...", fg="gray")
status_label.pack(pady=20)

start_listening()

root.mainloop()
