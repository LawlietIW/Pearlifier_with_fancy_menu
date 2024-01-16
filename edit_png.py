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
            "Azure": (73, 152, 188),
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
        target_color = pixels[x, y]
        stack = [(x, y)]

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
            pixels[x, y] = prev_color

            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)





    def on_button_press(self, event):
        self.mouse_pressed = True
        self.on_click(event)

    def on_button_hold(self, event):
        if self.mouse_pressed:
            self.on_click(event)

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