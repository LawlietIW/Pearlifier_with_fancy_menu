from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
import os
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from threading import Thread
# from edit_png import PixelColorChanger
import subprocess

from code_scripts.see_color import create_color_image, see_colors_used
from code_scripts.hsv_pearl import resize_image as hsv_reformer
from code_scripts.rgb_pearl import resize_image as rgb_reformer
from code_scripts.hsl_pearl import resize_image as hsl_reformer
from code_scripts.add_grid import upscale_and_add_grid



color_map = {
    "Black": (46, 47, 49),
    "Dark Blue (Blue)": (44, 70, 144),
    "Dark Red": (165, 45, 54),
    "Brown": (83, 65, 55),
    "Reddish Brown": (127, 51, 42),
    "Grey": (131, 136, 138),
    "Clear": (216, 210, 206),
    "White": (236, 237, 237),
    "Cream": (240, 232, 185),
    "Light Brown": (165, 105, 63),
    "Yellow": (240, 185, 1),
    "Orange": (230, 79, 39),
    "Transparent Red": (192, 36, 53),
    "Transparent Green": (55, 184, 118),
    "Green": (37, 104, 71),
    "Light green": (73, 174, 137),
    "Army (Dark Green)": (54, 63, 56),
    "Turquoise": (103, 151, 174),
    "Pastel Green": (131, 203, 112),
    "Pastel Yellow": (240, 234, 55),
    "Fluorescent Green": (12, 189, 81),
    "Neon Green": (6, 183, 60),
    "Light Blue": (48, 92, 176),
    "Azure": (73, 152, 188),
    "Pastel Blue": (98, 158, 215),
    "Neon Blue": (35, 83, 176),
    "Pastel Purple": (136, 109, 185),
    "Translucent Purple": (104, 62, 154),
    "Purple": (105, 74, 130),
    "Pink": (225, 136, 159),
    "Pastel Pink": (207, 112, 183),
    "Neon Pink (Fucsia)": (255, 32, 141),
    "Cerise": (255, 57, 86),
    "Burgundy": (89, 47, 56),
    "Claret": (185, 57, 94),
    "Red": (182, 49, 54),
    "Fluorescent Yellow": (241, 242, 28),
    "Neon Yellow": (229, 239, 19),
    "Pastel Red": (238, 105, 114),
    "Neon Red": (255, 40, 51),
    "Flesh": (222, 155, 144),
    "Beige": (222, 180, 139),
    "Translucent Brown": (135, 89, 61),
}



inverted_color_map = {
    (46, 47, 49): "Black",
    (44, 70, 144): "Dark Blue (Blue)",
    (165, 45, 54): "Dark Red",
    (83, 65, 55): "Brown",
    (127, 51, 42): "Reddish Brown",
    (131, 136, 138): "Grey",
    (216, 210, 206): "Clear",
    (236, 237, 237): "White",
    (240, 232, 185): "Cream",
    (165, 105, 63): "Light Brown",
    (240, 185, 1): "Yellow",
    (230, 79, 39): "Orange",
    (192, 36, 53): "Transparent Red",
    (55, 184, 118): "Transparent Green",
    (37, 104, 71): "Green",
    (73, 174, 137): "Light green",
    (54, 63, 56): "Army (Dark Green)",
    (103, 151, 174): "Turquoise",
    (131, 203, 112): "Pastel Green",
    (240, 234, 55): "Pastel Yellow",
    (12, 189, 81): "Fluorescent Green",
    (6, 183, 60): "Neon Green",
    (48, 92, 176): "Light Blue",
    (73, 152, 188): "Azure",
    (98, 158, 215): "Pastel Blue",
    (35, 83, 176): "Neon Blue",
    (136, 109, 185): "Pastel Purple",
    (104, 62, 154): "Translucent Purple",
    (105, 74, 130): "Purple",
    (225, 136, 159): "Pink",
    (207, 112, 183): "Pastel Pink",
    (255, 32, 141): "Neon Pink (Fucsia)",
    (255, 57, 86): "Cerise",
    (89, 47, 56): "Burgundy",
    (185, 57, 94): "Claret",
    (182, 49, 54): "Red",
    (241, 242, 28): "Fluorescent Yellow",
    (229, 239, 19): "Neon Yellow",
    (238, 105, 114): "Pastel Red",
    (255, 40, 51): "Neon Red",
    (222, 155, 144): "Flesh",
    (222, 180, 139): "Beige",
    (135, 89, 61): "Translucent Brown",
}




class ColorChangeCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super(ColorChangeCheckBox, self).__init__(**kwargs)

    def on_active(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 1, 0, 1) if value else Color(1, 0, 0, 1)  # Green if checked, red if unchecked
            Rectangle(pos=self.pos, size=self.size)

class ColorSelectionWindow(BoxLayout):
    def __init__(self, callback, original_menu_callback, **kwargs):
        super(ColorSelectionWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.callback = callback
        self.original_menu_callback = original_menu_callback
        self.selected_colors = set()

        self.zero_to_one_color_map = {}
        for color_name, rgb_tuple in color_map.items():
            self.zero_to_one_color_map[color_name] = tuple(val / 255.0 for val in rgb_tuple) + (1.0,)

        grid_layout = GridLayout(cols=10, rows = 6, spacing=10, size_hint_y=0.8)  # Adjust size_hint_y value
        self.color_buttons = {}  # Dictionary to store color buttons

        for color_name, color_value in self.zero_to_one_color_map.items():
            color_button = Button(background_normal='', background_color=color_value, size_hint=(None, None), size=(50, 50))
            color_button.bind(on_release=self.toggle_color)
            self.color_buttons[color_value] = color_button
            grid_layout.add_widget(color_button)

        
        self.add_widget(grid_layout)
        self.add_widget(BoxLayout(size_hint_y=0.1))

        self.selected_colors_layout = BoxLayout(size_hint_y=0.1)
        self.add_widget(self.selected_colors_layout)


    def toggle_color(self, instance):
        color = tuple(instance.background_color)
        if color in self.selected_colors:
            self.selected_colors.remove(color)
        else:
            self.selected_colors.add(color)
        self.update_button_appearance(color)
        self.update_selected_colors_layout()
        # Update the callback with the selected colors
        self.callback(self.selected_colors)

    def update_selected_colors_layout(self):
        self.selected_colors_layout.clear_widgets()
        for color in self.selected_colors:
            selected_color_button = Button(background_normal='', background_color=color, size_hint=(None, None), size=(50, 50))
            self.selected_colors_layout.add_widget(selected_color_button)

    def get_color_name(self, color):
        for name, value in self.zero_to_one_color_map.items():
            if value == color:
                return name
        return 'Unknown'
    

    def update_button_appearance(self, color):
        button = self.color_buttons.get(color)
        if button:
            button.canvas.before.clear()
            with button.canvas.before:
                if color in self.selected_colors:
                    Color(1, 1, 1, 1)  # Border color (white)
                    Rectangle(pos=button.pos, size=button.size)
                Color(*color[:-1])  # Set the original color without alpha
                Rectangle(pos=button.pos, size=button.size)


    def exit_and_return(self, instance):
        self.original_menu_callback()
        App.get_running_app().popup.dismiss()

class ModernMenuApp(App):
    def __init__(self, **kwargs):
        super(ModernMenuApp, self).__init__(**kwargs)
        self.popup = None
        self.selected_colors = set()  # New instance variable to store selected colors
        self.selected_file_path = ""
        # self.results_label = None

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.original_menu_layout = layout

        # Menu
        menu_layout = BoxLayout(orientation='horizontal', spacing=10)
        # menu_layout.add_widget(Button(text='Pick Image'))
        choose_image_button = Button(text='Choose Image',background_normal='', background_color=(1, 0.8, 0.2, 1))
        choose_image_button.bind(on_release=self.choose_image_button_pressed)
        menu_layout.add_widget(choose_image_button)

        choose_color_button = Button(text='Choose Colour', background_normal='', background_color=(0.7, 0.8, 1, 1))
        choose_color_button.bind(on_release=self.show_color_selection)
        menu_layout.add_widget(choose_color_button)

        # Vertical BoxLayout for width and height input fields and grid checkbox
        size_input_layout = BoxLayout(orientation='vertical', spacing=5)

        # Vertical BoxLayout for width and height input fields and custom color-change checkbox
        size_input_layout = BoxLayout(orientation='vertical', spacing=5)

        # Width input field
        width_input = TextInput(multiline=False, input_type='number', input_filter='float', hint_text='Width')
        size_input_layout.add_widget(width_input)

        # Height input field
        height_input = TextInput(multiline=False, input_type='number', input_filter='float', hint_text='Height')
        size_input_layout.add_widget(height_input)

        # Custom color-change checkbox for grid
        grid_input = TextInput(multiline=False, input_type='number', input_filter='float', hint_text='Thick line how often')
        size_input_layout.add_widget(grid_input)

        # Add the vertical layout containing width, height inputs, and color-change checkbox to the menu layout
        menu_layout.add_widget(size_input_layout)


        pearlify_button = Button(text='Pearlify', background_normal='', background_color= (1, 0.5, 0.5, 1))
        pearlify_button.bind(on_release=lambda instance: self.pearlify_button_pressed(width_input.text, height_input.text, grid_input.text))
        menu_layout.add_widget(pearlify_button)
        layout.add_widget(menu_layout)


        #Empty space 
        blank = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.1)
        layout.add_widget(blank)

        # Buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        # button_layout.add_widget(Button(text='Edit Image'))
        edit_button = Button(text='Edit Image', background_normal='', background_color= (0.4, 0.8, 0.7, 1))
        edit_button.bind(on_release=lambda instance: self.edit_button_pressed())
        button_layout.add_widget(edit_button)
        button_layout.add_widget(Button(text='Button 2'))
        button_layout.add_widget(Button(text='Button 3'))
        
        layout.add_widget(button_layout)

        return layout

    def show_color_selection(self, instance):
        self.original_menu_layout = self.root
        color_selection_window = ColorSelectionWindow(callback=self.on_colors_selected, original_menu_callback=self.return_to_original_menu)
        self.popup = Popup(title='Select Color', content=color_selection_window, size_hint=(None, None), size=(700, 600))
        self.popup.open()

    def on_colors_selected(self, selected_colors):
        self.selected_colors = selected_colors
        # print(f"Selected Colors: {selected_colors}")

    def return_to_original_menu(self):
        self.root = self.original_menu_layout

    
 
    def choose_image_button_pressed(self, instance):
        script_directory = os.path.dirname(os.path.realpath(__file__))
        initial_path = script_directory
        file_chooser = FileChooserIconView(path=initial_path)
        
        # Corrected binding here
        file_chooser.bind(on_submit=self.on_file_submit)

        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(file_chooser)

        self.popup = Popup(title='Choose Image', content=popup_layout, size_hint=(0.9, 0.9))
        self.popup.open()

    def on_file_submit(self, instance, value, useless_arg):
        # print("instance", instance)
        # Do something with the selected file path (value)
        # print(f"Selected file: {value}")
        
        self.selected_file_path = os.path.relpath(value[0])

        # print(f"Selected file: {self.selected_file_path}")

        # Check if the file has an allowed extension
        allowed_extensions = ['.png', '.jpg', '.jpeg']
        if any(self.selected_file_path.lower().endswith(ext) for ext in allowed_extensions):
            # Close the popup if the file has an allowed extension
            self.dismiss_popup()

    def dismiss_popup(self):
        # Helper method to close the popup
        for widget in self.popup.content.children:
            if isinstance(widget, FileChooserIconView):
                widget.path = widget.path  # Workaround to update the path before dismissing
        self.popup.dismiss()
    
    def pearlify_button_pressed(self, width=60, height=60, grid=5):
        width = int(width)
        height = int(height)
        grid = int(grid)

        filename = os.path.basename(self.selected_file_path)
        rgb_values = [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b, _ in self.selected_colors]
        output_image_path = "pearl_images/" + filename + ".png"

        # Define a function that will run the time-consuming operation in a separate thread
        def process_image():
            nonlocal output_image_path

            new_image, colors_used = rgb_reformer(self.selected_file_path, output_image_path, width, height, list(rgb_values))

            if grid > 1:
                thick_line = grid
                new_image = upscale_and_add_grid(new_image, width, height, pixel_scaling=10, thick_line=thick_line)
                output_image_path = "pearl_images/grid_" + filename + ".png"

            transformed_dict = {inverted_color_map[key]: value for key, value in colors_used.items()}
            sorted_color_counts = dict(sorted(transformed_dict.items(), key=lambda x: x[1], reverse=True))

            # Update the GUI with the results
            # App.get_running_app().root.results_label.text = f"Colors used: {sorted_color_counts}"

            see_colors_used(sorted_color_counts, color_map)
            new_image.save(output_image_path)
            new_image.show()

        # Create a thread and start it
        processing_thread = Thread(target=process_image)
        processing_thread.start()


    def edit_button_pressed(self):
        subprocess.Popen(['python', 'code_scripts/edit_png.py'])


if __name__ == '__main__':
    ModernMenuApp().run()
