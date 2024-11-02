import tkinter as tk
from tkinter import ttk, colorchooser
import random
import math
from tkinter import filedialog
import pygame

pygame.mixer.init()

# Music state
music_state = {
    "is_playing": False,
    "current_track": None
}

# State dictionaries for each light and sound channel
lights_state = {
    "Front Lighting": {"color": "#ffffff", "intensity": 100, "on": True, "position": (150, 100, 200, 150), "canvas_id": None},
    "Backlighting": {"color": "#ffffff", "intensity": 100, "on": True, "position": (300, 100, 350, 150), "canvas_id": None},
    "Downlighting": {"color": "#ffffff", "intensity": 100, "on": True, "position": (450, 75, 500, 125), "canvas_id": None},
    "Side Lighting": {"color": "#ffffff", "intensity": 100, "on": True, "position": (75, 150, 125, 200), "canvas_id": None},
    "High Side Lighting": {"color": "#ffffff", "intensity": 100, "on": True, "position": (525, 150, 575, 200), "canvas_id": None}
}

# Sound state
sound_state = {
    "Master Volume": 80,
    "Vocals": 75,
    "Instruments": 70,
    "Drums": 65,
    "Effects": 65
}

# Sound file paths for instruments and drums
sound_files = {
    "Vocals": "vocals.mp3",
    "Instruments": "instruments.mp3",
    "Drums": "drums.mp3",
    "Effects": "effects.mp3"
}

# Presets for lighting
presets = {
    "Full Stage": {"Front Lighting": 100, "Backlighting": 80, "Downlighting": 70, "Side Lighting": 60, "High Side Lighting": 50},
    "Spotlight Center": {"Front Lighting": 80, "Backlighting": 60, "Downlighting": 100, "Side Lighting": 0, "High Side Lighting": 0},
    "Fade to Black": {"Front Lighting": 0, "Backlighting": 0, "Downlighting": 0, "Side Lighting": 0, "High Side Lighting": 0}
}

# Movement presets
movement_presets = {
    "Random Movement": {"type": "random", "duration": 10000},
    "Left to Right": {"type": "linear", "steps": 10, "move_distance": 20},
    "Up and Down": {"type": "vertical", "steps": 10, "move_distance": 20},
    "Circular Movement": {"type": "circular", "radius": 50},
    "Back and Forth": {"type": "back_forth", "move_distance": 20},
}

# Apply lighting preset
def apply_preset(preset_name, stage_canvas):
    if preset_name in presets:
        for light_type, intensity in presets[preset_name].items():
            lights_state[light_type]["intensity"] = intensity
            lights_state[light_type]["on"] = intensity > 0
        update_stage_preview(stage_canvas)

# Update the stage based on light and sound settings
def update_stage_preview(stage_canvas):
    stage_canvas.delete("all")
    stage_canvas.create_rectangle(50, 50, 650, 300, fill="darkgrey", outline="black")  # Stage rectangle
    
    for light_type, state in lights_state.items():
        if state["on"]:
            x1, y1, x2, y2 = state["position"]
            color = adjust_intensity(state["color"], state["intensity"])
            # Create the oval and store the canvas ID in the state
            lights_state[light_type]["canvas_id"] = stage_canvas.create_oval(x1, y1, x2, y2, fill=color, outline="")

# Adjust color brightness based on intensity
def adjust_intensity(color, intensity):
    r, g, b = root.winfo_rgb(color)
    r = int((r / 256) * (intensity / 100))
    g = int((g / 256) * (intensity / 100))
    b = int((b / 256) * (intensity / 100))
    return f"#{r:02x}{g:02x}{b:02x}"

# Select color for light
def choose_color(light_type, stage_canvas):
    color = colorchooser.askcolor()[1]
    if color:
        lights_state[light_type]["color"] = color
        update_stage_preview(stage_canvas)

# Toggle light on/off
def toggle_light(light_type, stage_canvas):
    lights_state[light_type]["on"] = not lights_state[light_type]["on"]
    update_stage_preview(stage_canvas)

# Update intensity of light
def update_intensity(light_type, intensity_var, stage_canvas):
    lights_state[light_type]["intensity"] = intensity_var.get()
    update_stage_preview(stage_canvas)

# Glide movement for lights
def glide_light(light_type, target_position, duration, stage_canvas):
    original_position = lights_state[light_type]["position"]

    def animate(start, end, duration, steps=100):
        for step in range(steps + 1):
            # Calculate the intermediate position
            new_x1 = start[0] + (end[0] - start[0]) * step / steps
            new_y1 = start[1] + (end[1] - start[1]) * step / steps
            new_x2 = start[2] + (end[2] - start[2]) * step / steps
            new_y2 = start[3] + (end[3] - start[3]) * step / steps
            
            # Update the light's position on the canvas
            stage_canvas.coords(lights_state[light_type]["canvas_id"], new_x1, new_y1, new_x2, new_y2)
            stage_canvas.update()
            stage_canvas.after(duration // steps)

    animate(original_position, target_position, duration)

    # Update the lights_state with the new position after moving
    lights_state[light_type]["position"] = target_position  # Update position in state

# Move lights in a specific direction
def move_light(light_type, direction, stage_canvas):
    x1, y1, x2, y2 = lights_state[light_type]["position"]
    move_amount = 10  # Pixels to move

    if direction == "left":
        target_position = (x1 - move_amount, y1, x2 - move_amount, y2)
    elif direction == "right":
        target_position = (x1 + move_amount, y1, x2 + move_amount, y2)
    elif direction == "up":
        target_position = (x1, y1 - move_amount, x2, y2 - move_amount)
    elif direction == "down":
        target_position = (x1, y1 + move_amount, x2, y2 + move_amount)

    # Glide to the new position over 1 second (1000 ms)
    glide_light(light_type, target_position, 1000, stage_canvas)

# Execute movement preset
def execute_movement_preset(preset_name, stage_canvas):
    if preset_name in movement_presets:
        duration = 10000  # Total movement time is always 10 seconds
        if movement_presets[preset_name]["type"] == "random":
            random_movement(stage_canvas, duration)
        elif movement_presets[preset_name]["type"] == "linear":
            left_to_right_movement(stage_canvas, movement_presets[preset_name]["move_distance"], duration)
        elif movement_presets[preset_name]["type"] == "vertical":
            up_and_down_movement(stage_canvas, movement_presets[preset_name]["steps"], movement_presets[preset_name]["move_distance"], duration)
        elif movement_presets[preset_name]["type"] == "circular":
            circular_movement(stage_canvas, movement_presets[preset_name]["radius"], duration)
        elif movement_presets[preset_name]["type"] == "back_forth":
            back_and_forth_movement(stage_canvas, movement_presets[preset_name]["move_distance"], duration)

def random_movement(stage_canvas, duration):
    for light_type in lights_state.keys():
        if lights_state[light_type]["on"]:
            # Randomly choose a new position
            x1, y1, x2, y2 = lights_state[light_type]["position"]
            new_x1 = random.randint(75, 575)
            new_y1 = random.randint(75, 225)
            target_position = (new_x1, new_y1, new_x1 + (x2 - x1), new_y1 + (y2 - y1))
            glide_light(light_type, target_position, duration, stage_canvas)
    update_stage_preview(stage_canvas)

def left_to_right_movement(stage_canvas, move_distance, duration):
    steps = 10  # Number of steps to move across the stage
    for step in range(steps):
        for light_type in lights_state.keys():
            if lights_state[light_type]["on"]:
                x1, y1, x2, y2 = lights_state[light_type]["position"]
                target_position = (x1 + move_distance, y1, x2 + move_distance, y2)
                glide_light(light_type, target_position, duration // steps, stage_canvas)

def up_and_down_movement(stage_canvas, steps, move_distance, duration):
    for step in range(steps):
        for light_type in lights_state.keys():
            if lights_state[light_type]["on"]:
                x1, y1, x2, y2 = lights_state[light_type]["position"]
                target_position = (x1, y1 + move_distance, x2, y2 + move_distance)
                glide_light(light_type, target_position, duration // steps, stage_canvas)

def circular_movement(stage_canvas, radius, duration):
    for light_type in lights_state.keys():
        if lights_state[light_type]["on"]:
            x1, y1, x2, y2 = lights_state[light_type]["position"]
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            for angle in range(0, 360, 10):  # Move in 10 degree increments
                rad = math.radians(angle)
                new_x = center_x + radius * math.cos(rad)
                new_y = center_y + radius * math.sin(rad)
                target_position = (new_x, new_y, new_x + (x2 - x1), new_y + (y2 - y1))
                glide_light(light_type, target_position, duration // 36, stage_canvas)  # 36 steps to complete a circle

def back_and_forth_movement(stage_canvas, move_distance, duration):
    for light_type in lights_state.keys():
        if lights_state[light_type]["on"]:
            x1, y1, x2, y2 = lights_state[light_type]["position"]
            glide_light(light_type, (x1 + move_distance, y1, x2 + move_distance, y2), duration // 2, stage_canvas)
            glide_light(light_type, (x1, y1, x2, y2), duration // 2, stage_canvas)

# Function to toggle music on/off
def toggle_music():
    if music_state["is_playing"]:
        pygame.mixer.music.stop()
        music_state["is_playing"] = False
    else:
        music_file = filedialog.askopenfilename(title="Select Music File", filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")])
        if music_file:
            pygame.mixer.music.load(music_file)  # Load the user-selected music file
            pygame.mixer.music.play(-1)  # Play on loop
            music_state["is_playing"] = True

# Create the main application window
root = tk.Tk()
root.title("Audiovisual Stage Management System")
root.geometry("800x600")

# Create stage canvas
stage_canvas = tk.Canvas(root, width=700, height=300, bg="white")
stage_canvas.pack(pady=10)

# Create light controls
for light in lights_state.keys():
    frame = ttk.Frame(root)
    frame.pack(fill='x')

    light_label = ttk.Label(frame, text=light)
    light_label.pack(side='left')

    intensity_var = tk.IntVar(value=lights_state[light]["intensity"])
    intensity_slider = ttk.Scale(frame, from_=0, to=100, variable=intensity_var, command=lambda val, lt=light: update_intensity(lt, intensity_var, stage_canvas))
    intensity_slider.pack(side='left', fill='x', expand=True)

    color_button = ttk.Button(frame, text="Choose Color", command=lambda lt=light: choose_color(lt, stage_canvas))
    color_button.pack(side='left')

    toggle_button = ttk.Button(frame, text="Toggle", command=lambda lt=light: toggle_light(lt, stage_canvas))
    toggle_button.pack(side='left')

# Create sound controls
sound_frame = ttk.Frame(root)
sound_frame.pack(fill='x')

sound_label = ttk.Label(sound_frame, text="Master Volume")
sound_label.pack(side='left')

master_volume_var = tk.IntVar(value=sound_state["Master Volume"])
master_volume_slider = ttk.Scale(sound_frame, from_=0, to=100, variable=master_volume_var)
master_volume_slider.pack(side='left', fill='x', expand=True)

# Create instrument and drums volume sliders
for sound in ["Vocals", "Instruments", "Drums", "Effects"]:
    frame = ttk.Frame(root)
    frame.pack(fill='x')

    sound_label = ttk.Label(frame, text=sound)
    sound_label.pack(side='left')

    sound_var = tk.IntVar(value=sound_state[sound])
    sound_slider = ttk.Scale(frame, from_=0, to=100, variable=sound_var, command=lambda val, snd=sound: update_sound_volume(snd, sound_var))
    sound_slider.pack(side='left', fill='x', expand=True)

# Function to update sound volume based on slider value
def update_sound_volume(sound_type, sound_var):
    sound_state[sound_type] = sound_var.get()
    # Update the volume in pygame mixer
    if sound_type in sound_files:
        pygame.mixer.Sound(sound_files[sound_type]).set_volume(sound_state[sound_type] / 100.0)

# Create preset buttons
preset_frame = ttk.Frame(root)
preset_frame.pack(fill='x')

for preset in presets.keys():
    preset_button = ttk.Button(preset_frame, text=preset, command=lambda p=preset: apply_preset(p, stage_canvas))
    preset_button.pack(side='left')

# Create movement preset buttons
movement_frame = ttk.Frame(root)
movement_frame.pack(fill='x')

for movement in movement_presets.keys():
    movement_button = ttk.Button(movement_frame, text=movement, command=lambda m=movement: execute_movement_preset(m, stage_canvas))
    movement_button.pack(side='left')

# Create music control button
music_button = ttk.Button(root, text="Toggle Music", command=toggle_music)
music_button.pack(pady=10)

# Run the application
update_stage_preview(stage_canvas)
root.mainloop()
