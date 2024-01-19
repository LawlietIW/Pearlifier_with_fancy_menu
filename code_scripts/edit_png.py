import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


# color_map = {
#     "Black": (46, 47, 49),
#     "Dark Blue (Blue)": (44, 70, 144),
#     "Dark Red": (165, 45, 54),
#     "Brown": (83, 65, 55),
#     "Reddish Brown": (127, 51, 42),
#     "Grey": (131, 136, 138),
#     "Clear": (216, 210, 206),
#     "White": (236, 237, 237),
#     "Cream": (240, 232, 185),
#     "Light Brown": (165, 105, 63),
#     "Yellow": (240, 185, 1),
#     "Orange": (230, 79, 39),
#     "Transparent Red": (192, 36, 53),
#     "Transparent Green": (55, 184, 118),
#     "Green": (37, 104, 71),
#     "Light green": (73, 174, 137),
#     "Army (Dark Green)": (54, 63, 56),
#     "Turquoise": (103, 151, 174),
#     "Pastel Green": (131, 203, 112),
#     "Pastel Yellow": (240, 234, 55),
#     "Fluorescent Green": (12, 189, 81),
#     "Neon Green": (6, 183, 60),
#     "Light Blue": (48, 92, 176),
#     "Azure": (73, 152, 188),
#     "Pastel Blue": (98, 158, 215),
#     "Neon Blue": (35, 83, 176),
#     "Pastel Purple": (136, 109, 185),
#     "Translucent Purple": (104, 62, 154),
#     "Purple": (105, 74, 130),
#     "Pink": (225, 136, 159),
#     "Pastel Pink": (207, 112, 183),
#     "Neon Pink (Fucsia)": (255, 32, 141),
#     "Cerise": (255, 57, 86),
#     "Burgundy": (89, 47, 56),
#     "Claret": (185, 57, 94),
#     "Red": (182, 49, 54),
#     "Fluorescent Yellow": (241, 242, 28),
#     "Neon Yellow": (229, 239, 19),
#     "Pastel Red": (238, 105, 114),
#     "Neon Red": (255, 40, 51),
#     "Flesh": (222, 155, 144),
#     "Beige": (222, 180, 139),
#     "Translucent Brown": (135, 89, 61),
# }


color_map = {
    "Black": (0, 0, 0),
    "Blue" : (44, 70, 144),
    "Aqua" : (0, 255, 255),
    "Turquoise" : (51, 204, 204),
    "Pastel Pink": (207, 112, 183),
    "Purple": (153, 51, 153),
    "Light Brown": (255, 153, 102),
    "Brown": (204, 102, 0),
    "Dark Brown": (153, 51, 0),
    "Pig Pink" :  (255, 204, 204),
    "Pink" : (255, 153, 153),
    "Rindigo" : (204, 0, 102),
    "Gold" : (255, 187, 51),
    "Lemon" : (255, 255, 77),
    "Yellow" : (255, 255, 0),
    "Teal" : (102, 255, 179),
    "Neon" : (26, 255, 26),
    "Dark Green" : (0, 153, 51),
    "Orange" : (255, 117, 26),
    "Red" : (255, 0, 0),
    "Maroon" : (128, 0, 0),
    "White" : (255, 255, 255),
    "Grey" : (128, 128, 128),
    "Glass" : (217, 217, 217),   
}



inverted_color_map = {}
for key, value in color_map.items():
    inverted_color_map[value] = key




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

        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        # Bind arrow keys to scroll
        self.root.bind("<Up>", lambda event: self.canvas.yview_scroll(-1, "units"))
        self.root.bind("<Down>", lambda event: self.canvas.yview_scroll(1, "units"))
        self.root.bind("<Left>", lambda event: self.canvas.xview_scroll(-1, "units"))
        self.root.bind("<Right>", lambda event: self.canvas.xview_scroll(1, "units"))

        self.color_menu_frame = tk.Frame(self.root)
        self.color_menu_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.color_menu = tk.Listbox(self.color_menu_frame, selectmode=tk.SINGLE, height=len(color_map))
        for color in color_map:
            self.color_menu.insert(tk.END, color)
        self.color_menu.pack()

        for i, color in enumerate(color_map):
            self.color_menu.itemconfig(i, {'bg': f'#{self.rgb_to_hex(color_map[color])}'})

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
            self.load_image(file_path)

    def load_image(self, file_path):
        # file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image_path = file_path
            self.load_image_from_path()

    def load_image_from_path(self):
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((self.image.width * 3, self.image.height * 3), Image.NEAREST)
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Update canvas size
        self.canvas.config(scrollregion=(0, 0, self.image.width, self.image.height),
                           width=min(800, self.image.width),
                           height=min(600, self.image.height))

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        # Update color bar placement
        self.color_menu_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.color_menu.pack()

        for i, color in enumerate(color_map):
            self.color_menu.itemconfig(i, {'bg': f'#{self.rgb_to_hex(color_map[color])}'})

    def on_click(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        pixel_color = self.image.getpixel((x, y))
        self.selected_pixel_label.config(text=f"Selected Pixel: ({x}, {y}) - {pixel_color}")

        selected_color_index = self.color_menu.curselection()
        if selected_color_index:
            selected_color = list(color_map.keys())[selected_color_index[0]]

            pixels = self.image.load()

            # Save the current pixel information for undo
            self.undo_stack.append((x, y, pixel_color))

            # Replace all pixels of the same color around the clicked position until a black pixel is encountered
            self.replace_color_around_position(pixels, x, y, selected_color)

            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def scroll_canvas(self, event, dx, dy):
        self.canvas.xview_scroll(dx, "units")
        self.canvas.yview_scroll(dy, "units")
        self.on_click(event)  # Reapply color change after scrolling


    def replace_color_around_position(self, pixels, x, y, selected_color):
        # print("sel", selected_color)
        target_color = pixels[x, y]  #Color already there
        if target_color == (0,0,1): 
            return # Don't replace the line color
        if target_color == color_map[selected_color]:
            return # Don't replace the same color
        stack = [(x, y)]
        # print("target_color", target_color)
        # print("selected_color", selected_color)

        while stack:
            current_x, current_y = stack.pop()

            # Check if the pixel is within the image boundaries
            if 0 <= current_x < self.image.width and 0 <= current_y < self.image.height:
                # Check if the pixel has the target color
                if pixels[current_x, current_y] == target_color:
                    # Replace the color
                    pixels[current_x, current_y] = color_map[selected_color]

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
            selected_color = inverted_color_map[prev_color]
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

    def rgb_to_hex(self, rgb):
        return f'{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelColorChanger(root)
    root.mainloop()