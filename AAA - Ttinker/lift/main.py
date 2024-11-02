import tkinter as tk
from tkinter import TclError, messagebox

# Initialize Tkinter root window
root = tk.Tk()
root.title("Peak 2 Peak Gondola Control Panel Simulation")
root.geometry("750x750")

# Global variables to track system state
voltage = tk.IntVar(value=230)
wind_speed = tk.IntVar(value=0)
temperature = tk.IntVar(value=15)
speed = tk.DoubleVar(value=2)  # Use DoubleVar for more precision
lift_status = tk.StringVar(value="Stopped")
passenger_count = tk.IntVar(value=0)
capacity = 28
glass_bottom = tk.BooleanVar(value=False)
energy_consumption = tk.IntVar(value=0)

zone1_status = tk.StringVar(value="Active")
zone2_status = tk.StringVar(value="Active")
zone3_status = tk.StringVar(value="Active")

zone1_severity = tk.StringVar(value="Low")
zone2_severity = tk.StringVar(value="Low")
zone3_severity = tk.StringVar(value="Low")
load_passengers_button = None
next_gondola_button = None
gondola_passenger_list=[]
total_passengers=tk.IntVar(value=0)
gondola_count = 28

def create_zone_control(root, zone_name, zone_status, zone_severity, row):
    tk.Label(root, text=zone_name).grid(row=row, column=0, padx=10, pady=5)
    
    # Create status dropdown
    status_menu = tk.OptionMenu(root, zone_status, "Active", "Inactive", "Requiring Maintenance", 
                                 command=lambda x: update_severity(zone_status, zone_severity, severity_menu))
    status_menu.grid(row=row, column=1, padx=10, pady=5)
    
    # Create severity dropdown
    severity_menu = tk.OptionMenu(root, zone_severity, "Low", "Medium", "High")
    severity_menu.grid(row=row + 1, column=1, padx=10, pady=5)
    
    # Hide severity dropdown initially if status is not 'Requiring Maintenance'
    if zone_status.get() != "Requiring Maintenance":
        severity_menu.grid_remove()

def update_severity(zone_status, zone_severity, severity_menu):
    if zone_status.get() == "Requiring Maintenance":
        severity_menu.grid()  # Show severity menu
        zone_severity.set("Low")  # Default to 'Low' severity
    else:
        severity_menu.grid_remove()  # Hide severity menu

def update_energy_consumption():
    global energy_consumption, speed, total_passengers, capacity
    
    if capacity > 0:  # Avoid division by zero
            current_total_passengers = total_passengers.get()
            consumption = round(speed.get() * (current_total_passengers / capacity)*3)
            energy_consumption.set(consumption)  # Store as a double
    else:
        energy_consumption.set(0)  # Set to 0 if capacity is invalid

    # Update the Entry widget for total energy consumption dynamically



def start_lift():
    global lift_status, wind_speed, temperature, load_passengers_button, next_gondola_button  # Add buttons to global scope
    if wind_speed.get() > 80:
        messagebox.showwarning("High Wind", "Cannot start lift, wind speed too high!")
    elif temperature.get() < -20 or temperature.get() > 35:
        messagebox.showwarning("Temperature Warning", "Temperature outside operational range!")
    elif not check_zones_active():
        messagebox.showwarning("Zone Control", "One or more zones are inactive or in maintenance!")
    else:
        lift_status.set("Running")
        load_passengers_button.config(state="normal")  # Enable load passengers button
        next_gondola_button.config(state="normal")  # Enable next gondola button
        update_energy_consumption()

def stop_lift():
    global lift_status, load_passengers_button, next_gondola_button
    load_passengers_button.config(state="disabled")  # Enable load passengers button
    next_gondola_button.config(state="disabled")
    lift_status.set("Stopped")
    update_energy_consumption()

def emergency_stop():
    global lift_status, load_passengers_button, next_gondola_button
    load_passengers_button.config(state="disabled")  # Disable load passengers button
    next_gondola_button.config(state="disabled")  # Disable next gondola button
    lift_status.set("EMERGENCY STOP")
    messagebox.showerror("Emergency", "The gondola has been stopped due to an emergency!")
    messagebox.showerror("Rest System", "In order to continue operating, the system must be reset.")
    reset_system()  # Call reset_system() to reset the application state

def reset_system():
    global lift_status, passenger_count, energy_consumption, total_passengers, gondola_passenger_list
    lift_status.set("Stopped")
    passenger_count.set(0)
    energy_consumption.set(0)
    zone1_status.set("Active")
    zone2_status.set("Active")
    zone3_status.set("Active")
    wind_speed.set(0)  # Reset wind speed
    temperature.set(15)  # Reset temperature
    total_passengers.set(0)  # Reset total passengers
    gondola_passenger_list = []  # Clear gondola passenger list
    
    # Update Entry widgets for total passengers and total energy consumption dynamically

    messagebox.showinfo("System Reset", "The system has been reset.")

def load_passengers():
    global passenger_count, capacity, total_passengers, gondola_passenger_list, gondola_count

    # Check if the current gondola has reached capacity
    if passenger_count.get() >= capacity:
        messagebox.showwarning("Capacity Reached", "The gondola is at full capacity!")
    else:
        loading_passengers = min(5, capacity - passenger_count.get())  # Load 5 passengers or as many as possible
        passenger_count.set(passenger_count.get() + loading_passengers)  # Update the current gondola passenger count
        
        # Update total passengers correctly
        current_total = total_passengers.get()  # Get current total passengers
        total_passengers.set(current_total + loading_passengers)  # Update total passengers
        

        update_energy_consumption()  # Update energy consumption based on the new total


def next_gondola():
    """Handle the dispatch of the next gondola with the passenger load."""
    global total_passengers  # Ensure you access the global variable

    # Check if the gondola list has reached its max capacity (gondola_count)
    if len(gondola_passenger_list) >= gondola_count:
        # Subtract the passengers from the oldest gondola (first item in the list)
        oldest_gondola_passengers = gondola_passenger_list.pop(0)  # Remove the first item
        total_passengers.set(total_passengers.get() - oldest_gondola_passengers)  # Subtract its passengers from total

    # Add the current passenger count to the gondola list
    gondola_passenger_list.append(passenger_count.get())  # Add new passengers to the end 
    # Reset passenger count for the next gondola
    passenger_count.set(0)

    # Update Entry widget for total passengers dynamically

    update_energy_consumption()  # Update energy based on new total passenger count

def check_zone(zone_status, zone_severity):
    if zone_status.get() == "Active":
        return True
    elif zone_status.get() == "Requiring Maintenance":
        if zone_severity.get() == "Low":
            return True
        else:
            messagebox.showwarning("Maintenance Alert", 
                                    f"Zone is in maintenance. Severity: {zone_severity.get()}")
            return False
    elif zone_status.get() == "Inactive":
        return False
    return False

def check_zones_active():
    zone1_active = check_zone(zone1_status, zone1_severity)
    zone2_active = check_zone(zone2_status, zone2_severity)
    zone3_active = check_zone(zone3_status, zone3_severity)

    print(f"Zone 1 Active: {zone1_active}, Status: {zone1_status.get()}, Severity: {zone1_severity.get()}")
    print(f"Zone 2 Active: {zone2_active}, Status: {zone2_status.get()}, Severity: {zone2_severity.get()}")
    print(f"Zone 3 Active: {zone3_active}, Status: {zone3_status.get()}, Severity: {zone3_severity.get()}")

    return zone1_active and zone2_active and zone3_active

def run():
    global load_passengers_button, next_gondola_button, total_passengers
    # Voltage Display
    tk.Label(root, text="Voltage:").grid(row=0, column=0, padx=10, pady=10)
    voltage_label = tk.Label(root, textvariable=voltage, bg="white", width=10)
    voltage_label.grid(row=0, column=1, padx=10, pady=10)

    # Wind Speed Monitor
    tk.Label(root, text="Wind Speed (km/h):").grid(row=1, column=0, padx=10, pady=10)
    wind_speed_label = tk.Label(root, textvariable=wind_speed, bg="white", width=10)
    wind_speed_label.grid(row=1, column=1, padx=10, pady=10)

    # Manual Wind Speed Input
    tk.Label(root, text="Set Wind Speed:").grid(row=2, column=0, padx=10, pady=10)
    wind_speed_input = tk.Entry(root, textvariable=wind_speed, width=10)
    wind_speed_input.grid(row=2, column=1, padx=10, pady=10)

    # Temperature Monitor
    tk.Label(root, text="Temperature (°C):").grid(row=3, column=0, padx=10, pady=10)
    temperature_label = tk.Label(root, textvariable=temperature, bg="white", width=10)
    temperature_label.grid(row=3, column=1, padx=10, pady=10)

    # Manual Temperature Input
    tk.Label(root, text="Set Temperature:").grid(row=4, column=0, padx=10, pady=10)
    temperature_input = tk.Entry(root, textvariable=temperature, width=10)
    temperature_input.grid(row=4, column=1, padx=10, pady=10)

    # Speed Control
    tk.Label(root, text="Lift Speed (m/s):").grid(row=5, column=0, padx=10, pady=10)
    tk.Scale(root, from_=0, to=8, orient=tk.HORIZONTAL, variable=speed).grid(row=5, column=1, padx=10, pady=10)

    # Lift Status
    tk.Label(root, text="Lift Status:").grid(row=6, column=0, padx=10, pady=10)
    status_label = tk.Label(root, textvariable=lift_status, bg="white", width=15)
    status_label.grid(row=6, column=1, padx=10, pady=10)

    # Zone-Specific Controls
    tk.Label(root, text="Zone Control:").grid(row=7, column=0, padx=10, pady=10)
    create_zone_control(root, "Whistler Mountain Station (Zone 1)", zone1_status, zone1_severity, 7)
    create_zone_control(root, "Mid-Tower (Zone 2)", zone2_status, zone2_severity, 9)
    create_zone_control(root, "Blackcomb Mountain Station (Zone 3)", zone3_status, zone3_severity, 11)

    # Passenger Load
    load_passengers_button = tk.Button(root, text="Load Passengers", command=load_passengers, state="disabled")
    load_passengers_button.grid(row=13, column=2, padx=10, pady=10)
    tk.Label(root, text="Passengers Onboard:").grid(row=13, column=0, padx=10, pady=10)
    passenger_label = tk.Label(root, textvariable=passenger_count, bg="white", width=10)
    passenger_label.grid(row=13, column=1, padx=10, pady=10)
    tk.Label(root, text="Total Passengers:").grid(row=13, column=3, padx=10, pady=10)
    total_passengers_label = tk.Label(root, textvariable=total_passengers, bg="white", width=10)
    total_passengers_label.grid(row=13, column=4, padx=10, pady=10)
    # Next Gondola Button

    # Glass-Bottom Cabins
    tk.Checkbutton(root, text="Glass-Bottom Cabin", variable=glass_bottom).grid(row=14, column=0, columnspan=2, padx=10, pady=10)

    # Energy Consumption
    tk.Label(root, text="Energy Consumption (kWh):").grid(row=15, column=0, padx=10, pady=10)
    energy_label = tk.Label(root, textvariable=energy_consumption, bg="white", width=10)
    energy_label.grid(row=15, column=1, padx=10, pady=10)

    # Control Buttons
    tk.Button(root, text="Start", command=start_lift, bg="green").grid(row=16, column=0, padx=10, pady=10)
    tk.Button(root, text="Stop", command=stop_lift, bg="orange").grid(row=16, column=1, padx=10, pady=10)
    tk.Button(root, text="Emergency", command=emergency_stop, bg="red").grid(row=17, column=0, padx=10, pady=10)
    tk.Button(root, text="Reset", command=reset_system).grid(row=17, column=1, padx=10, pady=10)
    
    
    next_gondola_button = tk.Button(root, text="Next Gondola", command=next_gondola, state="disabled")
    next_gondola_button.grid(row=14, column=1, padx=10, pady=10)


     # Add Total Passengers Entry
    root.mainloop()

# Run the application
run()
