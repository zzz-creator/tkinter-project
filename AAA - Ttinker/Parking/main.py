import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel
from datetime import datetime

# Initialize main application
root = tk.Tk()
root.title("Parking Lot Management System")

# Configuration
num_rows = 11
num_columns = 9
total_spots = num_rows * num_columns
spot_status = {i: {"occupied": False, "entry_time": None, "fee_rate": 0.05} for i in range(total_spots)}

# Admin password
admin_password = "admin123"  # Change this to your desired password

# GUI Elements
info_label = tk.Label(root, text="Available Spots: " + str(total_spots), font=("Helvetica", 12))
info_label.grid(row=0, column=0, columnspan=num_columns, pady=10)

# Function to calculate and show parking fees based on time spent
def calculate_fees(spot_id):
    spot = spot_status[spot_id]
    if spot["occupied"]:  # Only calculate fees if the spot is occupied
        duration = (datetime.now() - spot["entry_time"]).total_seconds() // 60  # time in minutes
        fee = duration * spot["fee_rate"]
        return round(fee, 2)
    return 0  # Return 0 fee if the spot is not occupied

# Function to handle entry actions
def toggle_spot(spot_id):
    spot = spot_status[spot_id]
    if not spot["occupied"]:
        # Vehicle entering
        spot["occupied"] = True
        spot["entry_time"] = datetime.now()
        parking_buttons[spot_id].config(bg="red", text=f"Spot {spot_id + 1}\nOccupied")
        parking_buttons[spot_id].config(state=tk.DISABLED)  # Disable button after occupancy
        update_info()

# Function to handle exit actions
def prompt_exit():
    spot_id = simpledialog.askinteger("Exit Spot", "Which spot do you want to exit from? (1-20)", minvalue=1, maxvalue=total_spots)
    if spot_id is not None:
        handle_exit(spot_id - 1)  # Convert to zero-based index

def handle_exit(spot_id):
    spot = spot_status[spot_id]
    if spot["occupied"]:
        duration = calculate_fees(spot_id)  # Pass the spot ID to calculate fees
        # Display fee and ask for credit card number
        if messagebox.askyesno("Exit Confirmation", f"Fee: ${duration}. Do you want to proceed to pay?"):
            cc_number = simpledialog.askstring("Credit Card", "Enter Credit Card Number:")
            if cc_number and verify_credit_card(cc_number):
                # Complete exit process
                spot["occupied"] = False
                spot["entry_time"] = None
                parking_buttons[spot_id].config(bg="green", text=f"Spot {spot_id + 1}\nFee: ${duration:.2f}")
                parking_buttons[spot_id].config(state=tk.NORMAL)  # Enable button again for future entries
                update_info()
                messagebox.showinfo("Exit Successful", f"Exited from Spot {spot_id + 1}. Fee: ${duration:.2f}")
            else:
                messagebox.showwarning("Error", "Invalid credit card number.")
    else:
        messagebox.showwarning("Error", f"Spot {spot_id + 1} is already vacant.")

def verify_credit_card(number):
    """Luhn's algorithm to validate a credit card number"""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    
    return checksum % 10 == 0

# Function to update available spots count
def update_info():
    occupied_spots = sum(spot["occupied"] for spot in spot_status.values())
    available_spots = total_spots - occupied_spots
    info_label.config(text=f"Available Spots: {available_spots}")
def open_admin_panel():
    admin_window = Toplevel(root)
    admin_window.title("Admin Panel Login")

    tk.Label(admin_window, text="Enter Admin Password:").grid(row=0, column=0, pady=5, padx=5)

    # Entry widget for password
    password_entry = tk.Entry(admin_window, show="*", width=20)
    password_entry.grid(row=0, column=1, pady=5, padx=5)

    # Variable to track the "show password" checkbox
    show_password_var = tk.BooleanVar()

    # Function to toggle password visibility
    def toggle_password():
        if show_password_var.get():
            password_entry.config(show="")  # Show password
        else:
            password_entry.config(show="*")  # Mask password

    # Checkbox to show/hide password
    show_password_checkbox = tk.Checkbutton(admin_window, text="Show Password", variable=show_password_var, command=toggle_password)
    show_password_checkbox.grid(row=1, column=1, pady=5, sticky='w')

    # Function to validate the password and open the admin panel if correct
    def validate_password():
        if password_entry.get() == admin_password:
            admin_window.destroy()  # Close login window if password is correct
            open_admin_panel_controls()  # Open the main admin panel
        else:
            messagebox.showerror("Access Denied", "Invalid Password.")

    # Login button
    login_button = tk.Button(admin_window, text="Login", command=validate_password)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Center elements in the login window
    admin_window.grid_rowconfigure(0, weight=1)
    admin_window.grid_columnconfigure(1, weight=1)
# Admin Panel Functionality
def open_admin_panel_controls():
    admin_window = Toplevel(root)
    admin_window.title("Admin Panel")

    # Center elements in the admin panel
    for i in range(5):
        admin_window.grid_rowconfigure(i, weight=1)
    for j in range(2):
        admin_window.grid_columnconfigure(j, weight=1)

    # Spot Selection for Fee Update
    tk.Label(admin_window, text="Select Spot:").grid(row=0, column=0, pady=5)
    spot_var = tk.StringVar(admin_window)
    spot_var.set("1")  # Set default value
    spot_menu = tk.OptionMenu(admin_window, spot_var, *[str(i + 1) for i in range(total_spots)])
    spot_menu.grid(row=0, column=1, pady=5)

    def update_fee():
        spot_id = int(spot_var.get()) - 1  # Convert to zero-based index
        if spot_status[spot_id]["occupied"]:
            new_fee = simpledialog.askfloat("Update Fee", f"Enter new fee for Spot {spot_id + 1}:")
            if new_fee is not None and new_fee >= 0:
                spot_status[spot_id]["fee_rate"] = new_fee
                messagebox.showinfo("Success", f"Fee for Spot {spot_id + 1} updated to ${new_fee:.2f}.")
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid fee rate.")
        else:
            messagebox.showwarning("Invalid Operation", f"Cannot update fee for Spot {spot_id + 1} because it is vacant.")

    tk.Button(admin_window, text="Update Fee", command=update_fee).grid(row=1, columnspan=2, pady=5)

    # Update Status Button
    tk.Label(admin_window, text="Set Spot Status:").grid(row=2, column=0, pady=5)
    status_var = tk.StringVar(admin_window)
    status_var.set("Occupied")  # Set default value
    status_menu = tk.OptionMenu(admin_window, status_var, "Occupied", "Vacant")
    status_menu.grid(row=2, column=1, pady=5)

    def update_status():
        spot_id = int(spot_var.get()) - 1  # Convert to zero-based index
        new_status = status_var.get()
        if new_status == "Occupied" and not spot_status[spot_id]["occupied"]:
            # Mark as occupied
            spot_status[spot_id]["occupied"] = True
            spot_status[spot_id]["entry_time"] = datetime.now()
            parking_buttons[spot_id].config(bg="red", text=f"Spot {spot_id + 1}\nOccupied")
            parking_buttons[spot_id].config(state=tk.DISABLED)  # Disable button after occupancy
            messagebox.showinfo("Success", f"Spot {spot_id + 1} is now marked as Occupied.")
        elif new_status == "Vacant" and spot_status[spot_id]["occupied"]:
            # Mark as vacant
            spot_status[spot_id]["occupied"] = False
            spot_status[spot_id]["entry_time"] = None
            parking_buttons[spot_id].config(bg="green", text=f"Spot {spot_id + 1}\nFee: ${calculate_fees(spot_id):.2f}")
            parking_buttons[spot_id].config(state=tk.NORMAL)  # Enable button again for future entries
            messagebox.showinfo("Success", f"Spot {spot_id + 1} is now marked as Vacant.")
        else:
            messagebox.showwarning("Invalid Operation", f"Cannot mark Spot {spot_id + 1} as {new_status}.")

    tk.Button(admin_window, text="Update Status", command=update_status).grid(row=3, columnspan=2, pady=5)

    # Refresh Status Button
    def refresh_status():
        status_text.delete(1.0, tk.END)  # Clear existing text
        for i in range(total_spots):
            status = "Occupied" if spot_status[i]["occupied"] else "Vacant"
            fee = calculate_fees(i)  # Calculate fee based on the status
            status_text.insert(tk.END, f"Spot {i + 1}: {status} (Fee: ${fee:.2f})\n")

    tk.Button(admin_window, text="Refresh Status", command=refresh_status).grid(row=4, columnspan=2, pady=5)

    # Spot Status Overview
    tk.Label(admin_window, text="Spot Status:").grid(row=5, column=0, pady=5)
    status_text = tk.Text(admin_window, height=10, width=50)
    status_text.grid(row=6, columnspan=2, pady=5, sticky='nsew')  # Fill whole space

    # Make the status text box expand
    admin_window.grid_rowconfigure(6, weight=1)  # Make row 6 expandable
    admin_window.grid_columnconfigure(0, weight=1)  # Make column 0 expandable
    admin_window.grid_columnconfigure(1, weight=1)  # Make column 1 expandable

    # Initialize status display
    refresh_status()

# Create parking spots as buttons
parking_buttons = []
for i in range(total_spots):
    button = tk.Button(root, text=f"Spot {i + 1}", width=12, height=4, bg="green",
                       command=lambda i=i: toggle_spot(i))
    button.grid(row=(i // num_columns) + 1, column=i % num_columns, padx=5, pady=5)
    parking_buttons.append(button)

# Exit button
exit_button = tk.Button(root, text="Exit", command=prompt_exit)
exit_button.grid(row=num_rows + 1, column=0, columnspan=num_columns, pady=10)

# Admin panel button
admin_button = tk.Button(root, text="Admin Panel", command=open_admin_panel)
admin_button.grid(row=num_rows + 2, column=0, columnspan=num_columns, pady=10)

update_info()
root.mainloop()
