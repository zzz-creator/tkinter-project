import tkinter as tk
import random
from tkinter import messagebox

# Global variables
num_floors = 110  # Number of floors
num_elevators = 6 # Number of elevators
current_floors = [1] * num_elevators  # Current positions of the elevators
requested_floors = [[] for _ in range(num_elevators)]  # List to store requested floors for each elevator
statuses = [None] * num_elevators  # Statuses of each elevator's state
floors_per_column = 10  # Number of floors per column for floor buttons
is_waiting = [False] * num_elevators
requested_floor_buttons = []
max_floors=110

# Function to create the main user interface
def create_ui(master):
    global floors_per_column,requested_floor_buttons, max_floors
    # Create floor buttons in multiple columns
    for i in range(1, num_floors + 1):
        column = (i - 1) // floors_per_column
        row = (i - 1) % floors_per_column + 1
        button = tk.Button(master, text=f"Floor {i}", command=lambda floor=i: request_floor(floor))
        button.grid(row=row, column=column, padx=5, pady=2)
        requested_floor_buttons.append(button)

    # Create canvases and labels for each elevator
    global canvases, floor_labels, status_labels
    canvases = []
    floor_labels = []
    status_labels = []

    for elevator in range(num_elevators):
        # Dynamically calculate canvas height to fit the window height for the given number of floors
        canvas_height = min(600, num_floors * (600 // max_floors))  # You can adjust this height if needed
        canvas = tk.Canvas(master, width=60, height=canvas_height, bg='white')
        canvas.grid(row=1, column=floors_per_column + elevator + 1, rowspan=num_floors, padx=10)
        canvases.append(canvas)

        # Draw each elevator initially
        draw_elevator(elevator, canvas_height)

        # Display current floor and status for each elevator
        floor_label = tk.Label(master, text=f"Elevator {elevator + 1} - Current Floor: {current_floors[elevator]}")
        floor_label.grid(row=0, column=floors_per_column + elevator + 1, padx=10, pady=5)
        floor_labels.append(floor_label)

        status_label = tk.Label(master, text="Status: Idle")
        status_label.grid(row=num_floors + 1, column=floors_per_column + elevator + 1, padx=10, pady=5)
        status_labels.append(status_label)

    # Reset button
    reset_button = tk.Button(master, text="Reset", command=reset)
    reset_button.grid(row=num_floors + 2, column=0, columnspan=floors_per_column + num_elevators + 1, pady=10)
    emergency_stop_button = tk.Button(master, text="Emergency Stop", command=emergency_stop)
    emergency_stop_button.grid(row=num_floors + 3, column=0, columnspan=floors_per_column + num_elevators + 1, pady=10)
def emergency_stop():
    for i in range(num_elevators):
        statuses[i] = "Stopped"  # Set all elevators to stopped
        is_waiting[i] = False  # Clear any waiting states
        requested_floors[i].clear()  # Clear all requests for the elevator
        update_display(i)  # Update the display for each elevator
    messagebox.showwarning("Emergency Stop", "All elevators have been stopped for emergency.")
    for button in requested_floor_buttons:
        button.config(state=tk.DISABLED)
# Function to draw the elevator on the canvas
def draw_elevator(elevator_index, canvas_height):
    elevator_width = 40
    elevator_height = 40
    floor_height = canvas_height / num_floors
    x1 = 10
    y1 = canvas_height - (current_floors[elevator_index] * floor_height) + 5
    x2 = x1 + elevator_width
    y2 = y1 + elevator_height

    # Clear any previous drawing of the elevator
    canvases[elevator_index].delete("elevator")
    
    # Draw the elevator with color based on status
    if statuses[elevator_index] == "Stopped":
        color = "red"
    else:
        color = "blue"
    
    canvases[elevator_index].create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags="elevator")

# Function to request a floor
def request_floor(floor):
    elevator_index = min(range(num_elevators), key=lambda i: len(requested_floors[i]))
    
    if floor not in requested_floors[elevator_index]:
        requested_floors[elevator_index].append(floor)
        requested_floors[elevator_index].sort()  # Sort requests to process them in order
        
        # Provide feedback if the floor is already requested
        if is_waiting[elevator_index]:
            print(f"Floor {floor} has been added to Elevator {elevator_index + 1}'s queue.")
            disable_floor_button(floor)
        
        if not is_waiting[elevator_index]:  # Only initiate movement if not waiting
            move_elevator(elevator_index)
            disable_floor_button(floor)
def disable_floor_button(floor):
    button_index = floor - 1  # Button index is floor number - 1
    requested_floor_buttons[button_index].config(state=tk.DISABLED)  # Disable the button

# Function to enable the button for a floor when the elevator arrives
def enable_floor_button(floor):
    button_index = floor - 1  # Button index is floor number - 1
    requested_floor_buttons[button_index].config(state=tk.NORMAL)  # Enable the button
# Function to move the elevator based on requests
def move_elevator(elevator_index):
    global statuses
    
    # Get the current elevator status and requested floors
    status = statuses[elevator_index]
    requests = requested_floors[elevator_index]

    # If no requests, keep the elevator idle
    if not requests:
        statuses[elevator_index] = "Idle"
        return

    # Determine next action based on current floor and requests
    next_floor = requests[0]  # Get the next requested floor
    current_floor = current_floors[elevator_index]

    if current_floor < next_floor:
        statuses[elevator_index] = "Moving Up"
        current_floors[elevator_index] += 1  # Simulate moving up
    elif current_floor > next_floor:
        statuses[elevator_index] = "Moving Down"
        current_floors[elevator_index] -= 1  # Simulate moving down
    else:
        statuses[elevator_index] = "Stopped"
        requested_floors[elevator_index].pop(0)  # Remove the served request
        # If there are no more requests, set to Idle
        if not requested_floors[elevator_index]:
            statuses[elevator_index] = "Idle"

    update_display(elevator_index)  # Update the UI to reflect the current state
    simulate_movement(elevator_index,next_floor)

# Function to simulate the movement of the elevator with acceleration and deceleration
# Function to simulate the movement of the elevator with acceleration and deceleration
def simulate_movement(elevator_index, target_floor, delay=100):
    global current_floors

    # Determine distance from target to adjust speed
    distance = abs(current_floors[elevator_index] - target_floor)

    # Adjust delay to simulate acceleration and deceleration
    if distance > 10:
        delay = max(50, delay - 10)  # Accelerate by decreasing delay
    elif distance <= 3:
        delay = min(200, delay + 30)  # Decelerate by increasing delay

    # Move elevator up or down by 1 floor at a time
    if current_floors[elevator_index] < target_floor:
        current_floors[elevator_index] += 1
    elif current_floors[elevator_index] > target_floor:
        current_floors[elevator_index] -= 1

    # Get current canvas height to draw elevator at new position
    canvas_height = canvases[elevator_index].winfo_height()
    draw_elevator(elevator_index, canvas_height)
    update_display(elevator_index)

    # If the elevator reaches the target floor
    if current_floors[elevator_index] == target_floor:
        # Remove the completed request
        if target_floor in requested_floors[elevator_index]:
            requested_floors[elevator_index].remove(target_floor)
        
        total_wait_time = random.randint(5, 10)  # Total wait time in seconds
        wait_countdown(elevator_index, total_wait_time)  # Start countdown
        enable_floor_button(target_floor)
    else:
        master.after(delay, lambda: simulate_movement(elevator_index, target_floor, delay))


def wait_countdown(elevator_index, remaining_time):
    is_waiting[elevator_index] = True  # Set waiting flag at the start of countdown
    if remaining_time > 0:
        statuses[elevator_index] = f"Waiting for {remaining_time} seconds"
        update_display(elevator_index)
        master.after(1000, lambda: wait_countdown(elevator_index, remaining_time - 1))  # Countdown by 1 second
    else:
        finish_waiting(elevator_index)  # Only clear waiting after finishing

# Function to resume movement after waiting
def finish_waiting(elevator_index):
    statuses[elevator_index] = "Idle"
    is_waiting[elevator_index] = False
    update_display(elevator_index)
    if current_floors[elevator_index] in requested_floors[elevator_index]:
        enable_floor_button(current_floors[elevator_index])
    if requested_floors[elevator_index]:  # Continue to the next request if there are any
        move_elevator(elevator_index)

# Function to reset the elevator system
def update_countdown(dialog, seconds):
    if seconds > 0:
        label.config(text=f"Relaunching in {seconds} seconds")
        dialog.after(1000, lambda: update_countdown(dialog, seconds - 1))  # Update countdown every second
    else:
        dialog.destroy()  # Close the countdown dialog
        relaunch_application()  # Relaunch the application

# Function to show the countdown dialog
def show_countdown_dialog():
    dialog = tk.Toplevel(master)  # Create a new top-level window
    dialog.title("Relaunching Application")
    global label
    label = tk.Label(dialog, font=("Helvetica", 16))
    label.pack(padx=20, pady=20)

    # Disable the main window to prevent interaction
    #master.withdraw()
    dialog.grab_set() 

    update_countdown(dialog, 10)  # Start the countdown from 10 seconds
    dialog.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing the dialog

# Function to reset the elevator system
def reset():
    if messagebox.askyesno("Reset Application", "Do you want to reset the application?"):
        show_countdown_dialog()  # Show the countdown dialog
        for button in requested_floor_buttons:
            button.config(state=tk.NORMAL)

# Function to update the display labels
def update_display(elevator_index):
    if statuses[elevator_index] == "Stopped":
        floor_labels[elevator_index].config(text=f"Elevator {elevator_index + 1} - Status: Stopped")
        status_labels[elevator_index].config(text=f"Status: Emergency Stop Activated")
    else:
        floor_labels[elevator_index].config(text=f"Elevator {elevator_index + 1} - Current Floor: {current_floors[elevator_index]}")
        status_labels[elevator_index].config(text=f"Status: {statuses[elevator_index]}")

def relaunch_application():
    global master
    reinitialize_variables()
    master.destroy()  # Close the current Tkinter window
    master = tk.Tk()  # Create a new instance of the Tk class
    master.title("Elevator Control System")
    create_ui(master)  # Call the UI creation function to set everything up
    master.mainloop()  # Start the main event loop again
def reinitialize_variables():
    global current_floors, requested_floors, statuses, is_waiting
    current_floors = [1] * num_elevators  # Reset to starting floor
    requested_floors = [[] for _ in range(num_elevators)]  # Clear requests
    statuses = ["Idle"] * num_elevators  # Reset statuses
    is_waiting = [False] * num_elevators  # Reset waiting states
#Condtion Checks
if num_floors <= 1 or num_floors>max_floors:
    messagebox.showerror("Error 403: Forbidden", f"The number of floors must be greater than 1 AND less or equal to than {max_floors}.")
    exit()

if num_elevators <= 0:
    messagebox.showerror("Error 403: Forbidden", "The number of elevators must be greater than 0.")
    exit()
# Main application setup
master = tk.Tk()
master.title("Elevator Control System")
create_ui(master)
master.mainloop()
