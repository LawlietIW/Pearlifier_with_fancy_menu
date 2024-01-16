import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk






class PixelColorChanger:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Color Changer")

        self.image_path = None
        self.image = None
        self.tk_image = None

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_hold)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.selected_pixel_label = tk.Label(self.root, text="Selected Pixel: None")
        self.selected_pixel_label.pack()

        self.color_map = {
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

        self.inverted_color_map = {
            (236, 237, 237): "White",
            (240, 232, 185): "Cream",
            (240, 185, 1): "Yellow",
            (230, 79, 39): "Orange",
            (182, 49, 54): "Red",
            (225, 136, 159): "Pink",
            (105, 74, 130): "Purple",
            (44, 70, 144): "Dark Blue (Blue)",
            (48, 92, 176): "Light Blue",
            (37, 104, 71): "Green",
            (73, 174, 137): "Light green",
            (83, 65, 55): "Brown",
            (192, 36, 53): "Transparent Red",
            (55, 184, 118): "Transparent Green",
            (131, 136, 138): "Grey",
            (46, 47, 49): "Black",
            (216, 210, 206): "Clear",
            (127, 51, 42): "Reddish Brown",
            (165, 105, 63): "Light Brown",
            (165, 45, 54): "Dark Red",
            (104, 62, 154): "Translucent Purple",
            (135, 89, 61): "Translucent Brown",
            (222, 155, 144): "Flesh",
            (222, 180, 139): "Beige",
            (54, 63, 56): "Army (Dark Green)",
            (185, 57, 94): "Claret",
            (89, 47, 56): "Burgundy",
            (103, 151, 174): "Turquoise",
            (255, 32, 141): "Neon Pink (Fucsia)",
            (255, 57, 86): "Cerise",
            (229, 239, 19): "Neon Yellow",
            (255, 40, 51): "Neon Red",
            (35, 83, 176): "Neon Blue",
            (6, 183, 60): "Neon Green",
            (253, 134, 0): "Neon Orange",
            (241, 242, 28): "Fluorescent Yellow",
            (254, 99, 11): "Fluorescent Orange",
            (38, 89, 178): "Fluorescent Blue",
            (12, 189, 81): "Fluorescent Green",
            (240, 234, 55): "Pastel Yellow",
            (238, 105, 114): "Pastel Red",
            (136, 109, 185): "Pastel Purple",
            (98, 158, 215): "Pastel Blue",
            (131, 203, 112): "Pastel Green",
            (207, 112, 183): "Pastel Pink",
            (73, 152, 188): "Azure",
        }
        self.color_menu_frame = tk.Frame(self.root)
        self.color_menu_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.color_menu = tk.Listbox(self.color_menu_frame, selectmode=tk.SINGLE, height=len(self.color_map))
        for color in self.color_map:
            self.color_menu.insert(tk.END, color)
        self.color_menu.pack()

        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.open_image)
        file_menu.add_command(label="Save Image", command=self.save_image)

        self.mouse_pressed = False  # Flag to track if the mouse button is pressed
        self.undo_stack = []  # Stack to store pixel changes for undo
        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo)
        self.undo_button.pack()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image_path = file_path
            self.load_image()

    def load_image(self):
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((self.image.width * 3, self.image.height * 3), Image.NEAREST)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.config(width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def on_click(self, event):
        x, y = event.x, event.y
        pixel_color = self.image.getpixel((x, y))
        self.selected_pixel_label.config(text=f"Selected Pixel: ({x}, {y}) - {pixel_color}")

        selected_color_index = self.color_menu.curselection()
        if selected_color_index:
            selected_color = list(self.color_map.keys())[selected_color_index[0]]

            pixels = self.image.load()

            # Save the current pixel information for undo
            self.undo_stack.append((x, y, pixel_color))

            # Replace all pixels of the same color around the clicked position until a black pixel is encountered
            self.replace_color_around_position(pixels, x, y, selected_color)

            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)


    def replace_color_around_position(self, pixels, x, y, selected_color):
        # print("sel", selected_color)
        target_color = pixels[x, y]  #Color already there
        if target_color == (0,0,1): 
            return # Don't replace the line color
        if target_color == self.color_map[selected_color]:
            return # Don't replace the same color
        stack = [(x, y)]
        print("target_color", target_color)
        print("selected_color", selected_color)

        while stack:
            current_x, current_y = stack.pop()

            # Check if the pixel is within the image boundaries
            if 0 <= current_x < self.image.width and 0 <= current_y < self.image.height:
                # Check if the pixel has the target color
                if pixels[current_x, current_y] == target_color:
                    # Replace the color
                    pixels[current_x, current_y] = self.color_map[selected_color]

                    # Add neighboring pixels to the stack
                    stack.append((current_x - 1, current_y))
                    stack.append((current_x + 1, current_y))
                    stack.append((current_x, current_y - 1))
                    stack.append((current_x, current_y + 1))





    def undo(self):
        if self.undo_stack:
            x, y, prev_color = self.undo_stack.pop()
            pixels = self.image.load()

            # Restore the previous color
            selected_color = self.inverted_color_map[prev_color]
            self.replace_color_around_position(pixels, x, y, selected_color)

            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)





    def on_button_press(self, event):
        self.mouse_pressed = True
        self.on_click(event)

    def on_button_hold(self, event):
        if self.mouse_pressed:
            self.on_click(event)
            # Call the on_click method repeatedly while the mouse button is held
            self.root.after(10, self.on_button_hold, event)

    def on_button_release(self, event):
        self.mouse_pressed = False

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelColorChanger(root)
    root.mainloop()