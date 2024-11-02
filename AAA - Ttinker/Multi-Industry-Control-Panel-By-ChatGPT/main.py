import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import pyodbc
from datetime import datetime

# Database connection settings
server = 'localhost'  # e.g. 'localhost' or 'your_server_name'
database = 'MultiIndustryControlPanel'
username = 'admin'
password = 'admin'
STORED_PASSWORD=""

# Function to connect to the database
def connect_db():
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;'
    return pyodbc.connect(conn_str)

# Function to insert or update machine data based on industry
def save_machine_data(industry, machine_name, data):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        # Prepare the appropriate SQL statement based on the industry
        if industry == "Aerospace":
            cursor.execute(f"""
                INSERT INTO AerospaceData (MachineName, Speed, Status, LastUpdated, Altitude, FuelLevel)
                VALUES (?, ?, ?, ?, ?, ?)
            """, machine_name, data['Speed'], data['Status'], data['LastUpdated'], data['Altitude'], data['FuelLevel'])
        elif industry == "Industrial":
            cursor.execute(f"""
                INSERT INTO IndustrialData (MachineName, Speed, Status, LastUpdated, ProductionRate)
                VALUES (?, ?, ?, ?, ?)
            """, machine_name, data['Speed'], data['Status'], data['LastUpdated'], data['ProductionRate'])
        elif industry == "Transportation":
            cursor.execute(f"""
                INSERT INTO TransportationData (MachineName, Speed, Status, LastUpdated, Location, Route)
                VALUES (?, ?, ?, ?, ?, ?)
            """, machine_name, data['Speed'], data['Status'], data['LastUpdated'], data['Location'], data['Route'])
        elif industry == "Research":
            cursor.execute(f"""
                INSERT INTO ResearchData (MachineName, Speed, Status, LastUpdated, ExperimentType, EnergyLevels)
                VALUES (?, ?, ?, ?, ?, ?)
            """, machine_name, data['Speed'], data['Status'], data['LastUpdated'], data['ExperimentType'], data['EnergyLevels'])
        elif industry == "Maritime":
            cursor.execute(f"""
                INSERT INTO MaritimeData (MachineName, Speed, Status, LastUpdated, Depth, CargoLoad)
                VALUES (?, ?, ?, ?, ?, ?)
            """, machine_name, data['Speed'], data['Status'], data['LastUpdated'], data['Depth'], data['CargoLoad'])

        # Commit changes
        connection.commit()
        messagebox.showinfo("Success", "Machine data saved successfully.")
    except pyodbc.Error as e:
        messagebox.showerror("Database Error", f"Error: {str(e)}")
    finally:
        cursor.close()
        connection.close()


# Function to get all machines from a specific industry
def get_machines(industry):
    conn = connect_db()
    cursor = conn.cursor()
    table_name = f"{industry}Data"
    cursor.execute(f"SELECT * FROM {table_name}")
    machines = cursor.fetchall()
    cursor.close()
    conn.close()
    return machines

# Function to open the respective control panel with unique values and functions
def open_panel(industry):
    panel_window = tk.Toplevel(root)
    panel_window.title(f"{industry} Control Panel")

    frame = tk.Frame(panel_window)
    frame.pack(padx=20, pady=20)

    label = tk.Label(frame, text=f"{industry} Control Panel", font=("Arial", 16))
    label.pack()

    tk.Label(frame, text="Select Machine:").pack()
    
    # Dropdown for machine selection
    machine_var = tk.StringVar(value="Select Machine")
    machine_menu = tk.OptionMenu(frame, machine_var, *[m.MachineName for m in get_machines(industry)])
    machine_menu.pack()

    if industry == "Aerospace":
        tk.Label(frame, text="Altitude:").pack()
        altitude_entry = tk.Entry(frame)
        altitude_entry.pack()

        tk.Label(frame, text="Fuel Level:").pack()
        fuel_level_entry = tk.Entry(frame)
        fuel_level_entry.pack()

        tk.Button(frame, text="Launch", command=lambda: save_machine_data(industry, machine_var.get(), {
            'Speed': 100,  # Assume a default speed for launch
            'Status': 'Active',
            'Altitude': altitude_entry.get(),
            'FuelLevel': fuel_level_entry.get()
        })).pack(pady=5)

        tk.Button(frame, text="Land", command=lambda: save_machine_data(industry, machine_var.get(), {
            'Speed': 0,
            'Status': 'Inactive',
            'Altitude': altitude_entry.get(),
            'FuelLevel': fuel_level_entry.get()
        })).pack(pady=5)

    elif industry == "Industrial":
        tk.Label(frame, text="Production Rate:").pack()
        production_rate_entry = tk.Entry(frame)
        production_rate_entry.pack()

        tk.Button(frame, text="Start Production", command=lambda: save_machine_data(industry, machine_var.get(), {
            'Speed': 100,  # Assume a default speed
            'Status': 'Active',
            'ProductionRate': production_rate_entry.get()
        })).pack(pady=5)

        tk.Button(frame, text="Stop Production", command=lambda: save_machine_data(industry, machine_var.get(), {
            'Speed': 0,
            'Status': 'Inactive',
            'ProductionRate': production_rate_entry.get()
        })).pack(pady=5)

    elif industry == "Transportation":
        tk.Label(frame, text="Current Location:").pack()
        location_entry = tk.Entry(frame)
        location_entry.pack()

        tk.Label(frame, text="Route:").pack()
        route_entry = tk.Entry(frame)
        route_entry.pack()

        tk.Button(frame, text="Schedule Vehicle", command=lambda: save_machine_data(industry, machine_var.get(), {
            'Speed': 60,  # Assume a default speed
            'Status': 'Active',
            'Location': location_entry.get(),
            'Route': route_entry.get()
        })).pack(pady=5)

        tk.Button(frame, text="Reroute Vehicle", command=lambda: save_machine_data(industry, machine_var.get(), {
            'Speed': 60,
            'Status': 'Active',
            'Location': location_entry.get(),
            'Route': route_entry.get()
        })).pack(pady=5)

    elif industry == "Research":
        tk.Label(frame, text="Experiment Type:").pack()
        experiment_type_entry = tk.Entry(frame)
        experiment_type_entry.pack()

        tk.Label(frame, text="Energy Levels:").pack()
        energy_levels_entry = tk.Entry(frame)
        energy_levels_entry.pack()

        tk.Button(frame, text="Start Experiment", command=lambda: save_machine_data(industry, machine_var.get(), {
            'Speed': 0,  # Assume no speed for experiments
            'Status': 'Active',
            'ExperimentType': experiment_type_entry.get(),
            'EnergyLevels': energy_levels_entry.get()
        })).pack(pady=5)

        tk.Button(frame, text="Stop Experiment", command=lambda: save_machine_data(industry, machine_var.get(), {
            'Speed': 0,
            'Status': 'Inactive',
            'ExperimentType': experiment_type_entry.get(),
            'EnergyLevels': energy_levels_entry.get()
        })).pack(pady=5)

    elif industry == "Maritime":
        tk.Label(frame, text="Depth:").pack()
        depth_entry = tk.Entry(frame)
        depth_entry.pack()

        tk.Label(frame, text="Cargo Load:").pack()
        cargo_load_entry = tk.Entry(frame)
        cargo_load_entry.pack()

        tk.Button(frame, text="Control Navigation", command=lambda: save_machine_data(industry, machine_var.get(), {
            'Speed': 30,  # Assume a default speed for navigation
            'Status': 'Active',
            'Depth': depth_entry.get(),
            'CargoLoad': cargo_load_entry.get()
        })).pack(pady=5)

        tk.Button(frame, text="Monitor Conditions", command=lambda: save_machine_data(industry, machine_var.get(), {
            'Speed': 0,
            'Status': 'Inactive',
            'Depth': depth_entry.get(),
            'CargoLoad': cargo_load_entry.get()
        })).pack(pady=5)
# Function to open the global dashboard
# Function to open the global dashboard with an overview of all industries
def open_global_dashboard():
    global dashboard_window
    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Global Dashboard Overview")

    frame = tk.Frame(dashboard_window)
    frame.pack(padx=20, pady=20)

    label = tk.Label(frame, text="Global Control Dashboard Overview", font=("Arial", 16))
    label.pack()

    industries = ["Aerospace", "Industrial", "Transportation", "Research", "Maritime"]

    for industry in industries:
        # Create a frame for each industry overview
        industry_frame = tk.Frame(frame)
        industry_frame.pack(padx=10, pady=10, fill="x")

        industry_label = tk.Label(industry_frame, text=f"{industry} Overview", font=("Arial", 14))
        industry_label.pack()

        machines = get_machines(industry)  # Fetch machine data from the database

        # Display the number of machines
        num_machines = len(machines)
        machine_count_label = tk.Label(industry_frame, text=f"Number of Machines: {num_machines}")
        machine_count_label.pack()

        if num_machines > 0:
            # Display machine details
            for machine in machines:
                machine_info = f"Name: {machine.MachineName}, Status: {machine.Status}, Speed: {machine.Speed}"
                machine_label = tk.Label(industry_frame, text=machine_info)
                machine_label.pack()

        # Button to open the specific control panel for the industry
        open_panel_button = tk.Button(industry_frame, text=f"Control {industry}", command=lambda ind=industry: open_panel(ind))
        open_panel_button.pack(pady=5)
    
    # Optionally, add a button to close the dashboard
    refresh_button = tk.Button(frame, text="Relaunch/Refresh", command=relaunch_global_dashboard)
    refresh_button.pack(pady=10)
    close_button = tk.Button(frame, text="Close", command=dashboard_window.destroy)
    close_button.pack(pady=10)
def relaunch_global_dashboard():
        dashboard_window.destroy()
        open_global_dashboard()    
def add_new_machine():
    # Prompt for password
    password = simpledialog.askstring("Password", "Enter password to add new machine:", show='*')
    
    if password != STORED_PASSWORD:
        messagebox.showerror("Error", "Incorrect password!")
        return

    # Prompt for industry selection
    industry_window = tk.Toplevel()
    industry_window.title("Select Industry")

    industries = ["Aerospace", "Industrial", "Transportation", "Research", "Maritime"]
    selected_industry = tk.StringVar(industry_window)

    # Dropdown for selecting industry
    industry_label = tk.Label(industry_window, text="Select Industry:")
    industry_label.pack(pady=5)
    
    industry_dropdown = tk.OptionMenu(industry_window, selected_industry, *industries)
    industry_dropdown.pack(pady=5)
    
    # Button to confirm industry selection
    confirm_button = tk.Button(industry_window, text="Confirm", command=lambda: display_input_fields(selected_industry.get(), industry_window))
    confirm_button.pack(pady=10)

def display_input_fields(industry, parent_window):
    # Close the industry selection window
    parent_window.destroy()

    # Create a new window for machine details
    machine_window = tk.Toplevel()
    machine_window.title(f"Add New Machine - {industry}")

    # Machine name input
    machine_name_label = tk.Label(machine_window, text="Machine Name:")
    machine_name_label.pack(pady=5)
    machine_name_entry = tk.Entry(machine_window)
    machine_name_entry.pack(pady=5)

    # Define additional fields based on the selected industry
    input_fields = {}
    if industry == "Aerospace":
        input_fields = {
            "Speed": tk.Entry(machine_window),
            "Status": tk.Entry(machine_window),
            "Altitude": tk.Entry(machine_window),
            "FuelLevel": tk.Entry(machine_window),
        }
    elif industry == "Industrial":
        input_fields = {
            "Speed": tk.Entry(machine_window),
            "Status": tk.Entry(machine_window),
            "ProductionRate": tk.Entry(machine_window),
        }
    elif industry == "Transportation":
        input_fields = {
            "Speed": tk.Entry(machine_window),
            "Status": tk.Entry(machine_window),
            "Location": tk.Entry(machine_window),
            "Route": tk.Entry(machine_window),
        }
    elif industry == "Research":
        input_fields = {
            "Speed": tk.Entry(machine_window),
            "Status": tk.Entry(machine_window),
            "ExperimentType": tk.Entry(machine_window),
            "EnergyLevels": tk.Entry(machine_window),
        }
    elif industry == "Maritime":
        input_fields = {
            "Speed": tk.Entry(machine_window),
            "Status": tk.Entry(machine_window),
            "Depth": tk.Entry(machine_window),
            "CargoLoad": tk.Entry(machine_window),
        }

    # Display input fields
    for field_name, entry in input_fields.items():
        label = tk.Label(machine_window, text=f"{field_name}:")
        label.pack(pady=5)
        entry.pack(pady=5)

    # Submit button with validation for empty fields
    def on_submit():
        # Check if any field is empty
        if not machine_name_entry.get():
            messagebox.showerror("Error", "Machine Name cannot be empty.")
            return
        for field_name, entry in input_fields.items():
            if not entry.get():
                messagebox.showerror("Error", f"{field_name} cannot be empty.")
                return

        # Prepare data to save
        data_to_save = {
            'MachineName': machine_name_entry.get(),
            'Status': 'Active',
            'LastUpdated': datetime.now(),
        }
        data_to_save.update({field_name: entry.get() for field_name, entry in input_fields.items()})

        # Save machine data
        save_machine_data(industry, data_to_save['MachineName'], data_to_save)
        machine_window.destroy()
    submit_button = tk.Button(machine_window, text="Submit", command=on_submit)
    submit_button.pack(pady=10)
    


# Main application window
root = tk.Tk()
root.title("Global Hybrid Control Panels")

# Create the global dashboard button
global_dashboard_button = tk.Button(root, text="Open Global Dashboard", command=open_global_dashboard)
global_dashboard_button.pack(padx=10, pady=5)

# List of industries
industries = ["Aerospace", "Industrial", "Transportation", "Research", "Maritime"]

# Create buttons for each industry
for industry in industries:
    button = tk.Button(root, text=industry, command=lambda ind=industry: open_panel(ind))
    button.pack(padx=10, pady=5)
add_machine_button = tk.Button(root, text="Add New Machine", command=add_new_machine)
add_machine_button.pack(padx=10, pady=5)
# Start the Tkinter main loop
root.mainloop()
