import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random
import time

# Functions to control various features

# Machine Monitoring Functions
def start_machine():
    machine_status_var.set('Running')
    temp_var.set(random.uniform(20.0, 100.0))  # Random temperature for simulation
    history.append(f"{time.strftime('%H:%M:%S')} - Machine Started")

def stop_machine():
    machine_status_var.set('Idle')
    temp_var.set(random.uniform(20.0, 100.0))  # Update temperature when stopped
    history.append(f"{time.strftime('%H:%M:%S')} - Machine Stopped")

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Machine History")
    tk.Label(history_window, text="\n".join(history)).pack(padx=10, pady=10)

# Robotics Control Functions
def move_robot(direction):
    robot_status_var.set(f'Moving {direction}')
    history.append(f"{time.strftime('%H:%M:%S')} - Robot moved {direction}")

def stop_robot():
    robot_status_var.set('Idle')
    history.append(f"{time.strftime('%H:%M:%S')} - Robot Stopped")

def obstacle_detected():
    messagebox.showwarning("Obstacle Alert", "Obstacle detected! Robot will stop.")
    stop_robot()

# Transportation Fleet Management Functions
def update_vehicle_status():
    status = random.choice(["Active", "Inactive", "In Maintenance"])
    vehicle_status_var.set(f'Vehicle {random.randint(1, 10)}: {status}')
    history.append(f"{time.strftime('%H:%M:%S')} - Vehicle status updated: {status}")

def add_vehicle():
    vehicle_id = simpledialog.askinteger("Add Vehicle", "Enter Vehicle ID:")
    if vehicle_id:
        vehicle_status_var.set(f'Vehicle {vehicle_id} added.')
        history.append(f"{time.strftime('%H:%M:%S')} - Vehicle {vehicle_id} added.")

# Audio/Visual Control Functions
def load_media():
    media_file = simpledialog.askstring("Load Media", "Enter the path of the media file:")
    if media_file:
        current_media_var.set(media_file)
        messagebox.showinfo("Media Loaded", f"Media {media_file} loaded successfully.")

def adjust_volume(source, value):
    if source == 'Audio':
        audio_volume_var.set(value)
    else:
        video_volume_var.set(value)

def toggle_light():
    light_status_var.set('Off' if light_status_var.get() == 'On' else 'On')

def play_audio():
    print(f"Playing audio: {current_media_var.get()}")

def stop_audio():
    print("Stopping audio...")

def play_video():
    print(f"Playing video: {current_media_var.get()}")

def stop_video():
    print("Stopping video...")

# Home Automation Functions
def set_thermostat(value):
    thermostat_temp_var.set(value)

def toggle_security_system():
    if security_status_var.get() == 'Disarmed':
        security_status_var.set('Armed')
    else:
        # Ask for passcode to disarm
        passcode = simpledialog.askstring("Passcode Required", "Enter Passcode to Disarm Security System:")
        if passcode == "1234":  # Predefined passcode
            security_status_var.set('Disarmed')
            messagebox.showinfo("Security System", "Security System Disarmed")
        else:
            messagebox.showerror("Security System", "Incorrect Passcode! Security System remains Armed.")

# Create main window
root = tk.Tk()
root.title("Smart Industrial Control and Monitoring Dashboard")
root.geometry("800x600")
thermostat_temp_var = tk.DoubleVar(20)
security_status_var = tk.StringVar("Disarmed")
# Create Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# History for Machine Monitoring
history = []

# Machine Monitoring Tab
machine_tab = ttk.Frame(notebook)
notebook.add(machine_tab, text='Machine Monitoring')

machine_status_var = tk.StringVar(value='Idle')
temp_var = tk.DoubleVar(value=20.0)

tk.Label(machine_tab, text="Machine Status:").grid(row=0, column=0, padx=10, pady=10)
tk.Label(machine_tab, textvariable=machine_status_var).grid(row=0, column=1, padx=10, pady=10)

tk.Button(machine_tab, text="Start Machine", command=start_machine).grid(row=1, column=0, padx=10, pady=10)
tk.Button(machine_tab, text="Stop Machine", command=stop_machine).grid(row=1, column=1, padx=10, pady=10)
tk.Button(machine_tab, text="Show History", command=show_history).grid(row=1, column=2, padx=10, pady=10)

tk.Label(machine_tab, text="Temperature:").grid(row=2, column=0, padx=10, pady=10)
tk.Label(machine_tab, textvariable=temp_var).grid(row=2, column=1, padx=10, pady=10)

# Robotics Control Tab
robotics_tab = ttk.Frame(notebook)
notebook.add(robotics_tab, text='Robotics Control')

robot_status_var = tk.StringVar(value='Idle')

tk.Label(robotics_tab, text="Robot Status:").grid(row=0, column=0, padx=10, pady=10)
tk.Label(robotics_tab, textvariable=robot_status_var).grid(row=0, column=1, padx=10, pady=10)

tk.Button(robotics_tab, text="Move Up", command=lambda: move_robot("Up")).grid(row=1, column=0, padx=10, pady=10)
tk.Button(robotics_tab, text="Move Down", command=lambda: move_robot("Down")).grid(row=1, column=1, padx=10, pady=10)
tk.Button(robotics_tab, text="Stop Robot", command=stop_robot).grid(row=1, column=2, padx=10, pady=10)
tk.Button(robotics_tab, text="Simulate Obstacle", command=obstacle_detected).grid(row=1, column=3, padx=10, pady=10)

# Transportation Fleet Management Tab
fleet_tab = ttk.Frame(notebook)
notebook.add(fleet_tab, text='Transportation Fleet')

vehicle_status_var = tk.StringVar(value='Inactive')

tk.Label(fleet_tab, text="Vehicle Status:").grid(row=0, column=0, padx=10, pady=10)
tk.Label(fleet_tab, textvariable=vehicle_status_var).grid(row=0, column=1, padx=10, pady=10)

tk.Button(fleet_tab, text="Update Vehicle Status", command=update_vehicle_status).grid(row=1, column=0, padx=10, pady=10)
tk.Button(fleet_tab, text="Add Vehicle", command=add_vehicle).grid(row=1, column=1, padx=10, pady=10)

# Audio/Visual Control Tab
audio_visual_tab = ttk.Frame(notebook)
notebook.add(audio_visual_tab, text='Audio/Visual Control')

audio_volume_var = tk.DoubleVar(value=50)
video_volume_var = tk.DoubleVar(value=50)
light_status_var = tk.StringVar(value='Off')
current_media_var = tk.StringVar(value='No media loaded')

tk.Label(audio_visual_tab, text="Audio Volume:").grid(row=0, column=0, padx=10, pady=10)
tk.Scale(audio_visual_tab, from_=0, to=100, variable=audio_volume_var, orient='horizontal', command=lambda value: adjust_volume('Audio', value)).grid(row=0, column=1, padx=10, pady=10)

tk.Label(audio_visual_tab, text="Video Volume:").grid(row=1, column=0, padx=10, pady=10)
tk.Scale(audio_visual_tab, from_=0, to=100, variable=video_volume_var, orient='horizontal', command=lambda value: adjust_volume('Video', value)).grid(row=1, column=1, padx=10, pady=10)

tk.Label(audio_visual_tab, text="Lights:").grid(row=2, column=0, padx=10, pady=10)
tk.Label(audio_visual_tab, textvariable=light_status_var).grid(row=2, column=1, padx=10, pady=10)
tk.Button(audio_visual_tab, text="Toggle Lights", command=toggle_light).grid(row=2, column=2, padx=10, pady=10)

tk.Button(audio_visual_tab, text="Load Media", command=load_media).grid(row=3, column=0, padx=10, pady=10)
tk.Button(audio_visual_tab, text="Play Audio", command=play_audio).grid(row=3, column=1, padx=10, pady=10)
tk.Button(audio_visual_tab, text="Stop Audio", command=stop_audio).grid(row=3, column=2, padx=10, pady=10)
tk.Button(audio_visual_tab, text="Play Video", command=play_video).grid(row=3, column=3, padx=10, pady=10)
tk.Button(audio_visual_tab, text="Stop Video", command=stop_video).grid(row=3, column=4, padx=10, pady=10)

# Start the application
root.mainloop()
