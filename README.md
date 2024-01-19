# Pearlifier
Run the fancy_menu.py to start

pip install kivy
pip install pillow

or

conda env create -f environment.yml

Then pick a file, choose the colours, pick width height and grid. If 1 or 0 you get no grid. Else you get a grid with thick line as often as you say. Then pearlify!!!!!!!


# To make the app
py -m PyInstaller fancy_menu.py

## Features
### Choose Image:
Allows users to select an image file (PNG, JPG, JPEG) from their system.

### Choose Colour:
Opens a color selection window where users can choose colors for further processing.

### Pearlify:
Applies the selected colors to the chosen image and saves the result in the "pearl_images" directory. Users can specify width, height, and grid parameters.

### Edit Image:
Opens a separate script (edit_png.py) for additional image editing capabilities.
