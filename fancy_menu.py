from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

class ColorSelectionWindow(BoxLayout):
    def __init__(self, callback, original_menu_callback, **kwargs):
        super(ColorSelectionWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.callback = callback
        self.original_menu_callback = original_menu_callback
        self.selected_colors = set()
        self.colors = {'Red': (1, 0, 0, 1), 'Green': (0, 1, 0, 1), 'Blue': (0, 0, 1, 1)}  # Example predefined colors

        grid_layout = GridLayout(cols=3, spacing=10)
        self.color_buttons = {}  # Dictionary to store color buttons

        for color_name, color_value in self.colors.items():
            color_button = Button(text=color_name, background_color=color_value, size_hint=(None, None), size=(50, 50))
            color_button.bind(on_release=self.toggle_color)
            self.color_buttons[color_value] = color_button
            grid_layout.add_widget(color_button)

        exit_button = Button(text='Exit', on_release=self.exit_and_return)
        self.add_widget(grid_layout)
        self.add_widget(exit_button)

    def toggle_color(self, instance):
        color = tuple(instance.background_color)
        if color in self.selected_colors:
            self.selected_colors.remove(color)
        else:
            self.selected_colors.add(color)
        self.update_button_appearance(color)
        # Update the callback with the selected colors
        self.callback(self.selected_colors)

    def update_button_appearance(self, color):
        button = self.color_buttons.get(color)
        if button:
            if color in self.selected_colors:
                button.canvas.before.clear()
                with button.canvas.before:
                    Color(1, 1, 1, 1)  # Border color (white)
                    Rectangle(pos=button.pos, size=button.size)
            else:
                button.canvas.before.clear()

    def exit_and_return(self, instance):
        self.original_menu_callback()
        App.get_running_app().popup.dismiss()

class ModernMenuApp(App):
    def __init__(self, **kwargs):
        super(ModernMenuApp, self).__init__(**kwargs)
        self.popup = None
        self.selected_colors = set()  # New instance variable to store selected colors

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.original_menu_layout = layout

        # Menu
        menu_layout = BoxLayout(orientation='horizontal', spacing=10)
        choose_color_button = Button(text='Choose Colour')
        choose_color_button.bind(on_release=self.show_color_selection)
        menu_layout.add_widget(choose_color_button)
        menu_layout.add_widget(Button(text='Choose Colour Scheme'))
        menu_layout.add_widget(Button(text='Pearlify'))
        layout.add_widget(menu_layout)

        # Buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        button_layout.add_widget(Button(text='Edit Image'))
        button_layout.add_widget(Button(text='Button 2'))
        button_layout.add_widget(Button(text='Button 3'))
        
        layout.add_widget(button_layout)

        return layout

    def show_color_selection(self, instance):
        self.original_menu_layout = self.root
        color_selection_window = ColorSelectionWindow(callback=self.on_colors_selected, original_menu_callback=self.return_to_original_menu)
        self.popup = Popup(title='Select Color', content=color_selection_window, size_hint=(None, None), size=(300, 400))
        self.popup.open()

    def on_colors_selected(self, selected_colors):
        self.selected_colors = selected_colors
        print(f"Selected Colors: {selected_colors}")

    def return_to_original_menu(self):
        self.root = self.original_menu_layout
    
    def pearlify_button_pressed(self, instance):
        print(f"Pearlifying with colors: {self.selected_colors}")
        # Implement your logic to use the selected colors for pearlify

if __name__ == '__main__':
    ModernMenuApp().run()
