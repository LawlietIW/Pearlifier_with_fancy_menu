import tkinter as tk
from tkinter import ttk, colorchooser
from tkinter import messagebox

color_map = {
    "White": (236, 237, 237),
    "Cream": (240, 232, 185),
    "Yellow": (240, 185, 1),
    "Orange": (230, 79, 39),
    "Red": (182, 49, 54),
    "Pink": (225, 136, 159),
    "Purple": (105, 74, 130),
    "Dark Blue (Blue)": (44, 70, 144),
    "Light Blue": (48, 92, 176),
    "Green": (37, 104, 71),
    "Light green": (73, 174, 137),
    "Brown": (83, 65, 55),
    "Transparent Red": (192, 36, 53),
    "Transparent Green": (55, 184, 118),
    "Grey": (131, 136, 138),
    "Black": (46, 47, 49),
    "Clear": (216, 210, 206),
    "Reddish Brown": (127, 51, 42),
    "Light Brown": (165, 105, 63),
    "Dark Red": (165, 45, 54),
    "Translucent Purple": (104, 62, 154),
    "Translucent Brown": (135, 89, 61),
    "Flesh": (222, 155, 144),
    "Beige": (222, 180, 139),
    "Army (Dark Green)": (54, 63, 56),
    "Claret": (185, 57, 94),
    "Burgundy": (89, 47, 56),
    "Turquoise": (103, 151, 174),
    "Neon Pink (Fucsia)": (255, 32, 141),
    "Cerise": (255, 57, 86),
    "Neon Yellow": (229, 239, 19),
    "Neon Red": (255, 40, 51),
    "Neon Blue": (35, 83, 176),
    "Neon Green": (6, 183, 60),
    "Neon Orange": (253, 134, 0),
    "Fluorescent Yellow": (241, 242, 28),
    "Fluorescent Orange": (254, 99, 11),
    "Fluorescent Blue": (38, 89, 178),
    "Fluorescent Green": (12, 189, 81),
    "Pastel Yellow": (240, 234, 55),
    "Pastel Red": (238, 105, 114),
    "Pastel Purple": (136, 109, 185),
    "Pastel Blue": (98, 158, 215),
    "Pastel Green": (131, 203, 112),
    "Pastel Pink": (207, 112, 183),
    "Azure": (73, 152, 188),
}

def process_input(value):
    if value.lower() == 'choose colours':
        open_color_palette_window()
    elif value == 'RGB' or value == 'HSL' or value == 'HSV':
        result_label.config(text=f"Result: {process_function(value)}")
    elif value.lower() == 'grid':
        open_grid_window()
    else:
        messagebox.showinfo("Invalid Option", "Please enter a valid option.")

def open_color_palette_window():
    color_palette_window = tk.Toplevel(root)
    color_palette_window.title("Choose Colors")

    for color_name, rgb in color_map.items():
        # Convert RGB values to hexadecimal color code
        color_code = "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

        # Create a solid-colored image with the specified size
        image = tk.PhotoImage(width=20, height=20)
        image.put(color_code, to=(0, 0, 19, 19))  # Fill the entire image with the color

        # Create a style for the button with the image
        style_name = f"{color_name}.TButton"
        style.configure(style_name, background=color_code)

        # Create the button with the specified style and image
        color_button = ttk.Button(color_palette_window, image=image, command=lambda c=color_name: select_color(c, rgb), style=style_name, compound="center")
        color_button.image = image  # Keep a reference to the image to prevent it from being garbage collected
        color_button.pack(padx=10, pady=5)




def open_grid_window():
    grid_window = tk.Toplevel(root)
    grid_window.title("Grid Options")

    # Add grid options here

def process_function(value):
    # Replace this with your actual processing logic
    return f"You selected option {value}"

def select_color(color_name, rgb):
    if color_name in selected_colors:
        selected_colors.remove(color_name)
    else:
        selected_colors.append(color_name)
    update_result_label()

def update_result_label():
    result_label.config(text=f"Result: Selected Colors - {', '.join(selected_colors)}")

# Create the main window
root = tk.Tk()
root.title("Interactive Menu")

# Create a list to store selected colors
selected_colors = []

# Create buttons for different options
buttons_frame = ttk.Frame(root)

options = ['Choose Colours', 'RGB', 'HSL', 'HSV', 'Grid']

for i, option in enumerate(options):
    button = ttk.Button(buttons_frame, text=option, command=lambda option=option: process_input(option))
    button.grid(row=0, column=i, padx=10, pady=10)

# Bindings for Choose Colours and Grid options
buttons_frame.winfo_children()[0].bind("<Button-1>", lambda event: choose_colours_pressed())
grid_button = buttons_frame.winfo_children()[4]
grid_button.bind("<Button-1>", lambda event: grid_pressed())

buttons_frame.pack()

# Create a style to highlight the pressed button
style = ttk.Style(root)
style.configure('Highlighted.TButton', background='lightblue')

# Create the result label
result_label = ttk.Label(root, text="Result: ", font=("Arial", 14))
result_label.pack()

# Run the application
root.mainloop()
