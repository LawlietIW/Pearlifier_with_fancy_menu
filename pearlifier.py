from code_scripts.see_color import create_color_image, see_colors_used
from code_scripts.hsv_pearl import resize_image as hsv_reformer
from code_scripts.rgb_pearl import resize_image as rgb_reformer
from code_scripts.hsl_pearl import resize_image as hsl_reformer
from code_scripts.add_grid import upscale_and_add_grid
import os


def get_colors(color_names, color_map):
    """Returns a list of RGB colors corresponding to the color names"""
    result = []
    
    for color_name in color_names:
        if color_name in color_map:
            result.append(color_map[color_name])
        else:
            result.append(None)  # or any default value if the color name is not found
    return result

# color_map = {
#     'black': (0, 0, 0),
#     'grey': (145, 150, 155),
#     'white': (255, 255, 255),
#     'yellow': (255, 215, 90),
#     'pastel yellow': (245, 240, 125),
#     'cream': (250, 240, 195),
#     'teddy bear': (240, 175, 95),
#     'beige': (225, 185, 150),
#     'light brown': (190, 130, 100),
#     'burgundy': (115, 75, 85),
#     'brown': (100, 75, 80),
#     'red brown': (170, 85, 80),
#     'raspberry': (195, 80, 115),
#     'dark red': (175, 75, 85),
#     'red': (200, 65, 80),
#     'orange': (240, 105, 95),
#     'fuchsia': (255, 95, 200),
#     'pastel coral': (255, 120, 140),
#     'flesh': (240, 170, 165),
#     'pastel pink': (230, 135, 200),
#     'pink': (245, 155, 175),
#     'pastel purple': (165, 140, 205),
#     'light blue': (25, 105, 180),
#     'blue': (35, 85, 160),
#     'purple': (120, 90, 145),
#     'turquoise': (105, 160, 175),
#     'pastel blue': (80, 170, 225),
#     'pastel green': (150, 230, 160),
#     'dark green': (70, 85, 90),
#     'green': (35, 125, 95),
#     'light green': (70, 195, 165),
#     'grass': (106, 160, 46),
# }



color_map = {
    "Line Color": (0, 0, 1),
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


inverted_color_map = {
    (0,0,1): "Line Color",
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


#The colors that we want to use
color_names = ["White", "Cream", "Yellow", "Red", "Pink", "Purple", "Pink", "Dark Blue (Blue)", "Light Blue", "Green", "Light green", "Brown", "Grey", "Black", "Reddish Brown", "Light Brown", "Dark Red", "Flesh", "Beige", "Army (Dark Green)", "Claret", "Burgundy", "Turquoise", "Neon Pink (Fucsia)", "Neon Yellow", "Neon Red", "Neon Blue", "Neon Green", "Neon Orange", "Fluorescent Yellow", "Fluorescent Orange", "Fluorescent Blue", "Fluorescent Green", "Pastel Yellow", "Pastel Red", "Pastel Purple", "Pastel Blue", "Pastel Green", "Pastel Pink", "Azure"]
pixel_scaling = 5

if __name__ == "__main__":
    while True:
        print("What do you want to do?")
        print("1. View color palette")
        print("2. Convert to HSV")
        print("3. Convert to HSL")
        print("4. Convert to RGB")
        # print("5. Add grid")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            print("Color Palette:")
            create_color_image(color_map)
            print("Also saved to color_palette.png")

        elif choice == 2 or choice == 3 or choice == 4:
            file_name = input("Enter the name of the image: ")
            # input_image_path = "images/" + input_path
            directory = "images/"

            # List all files in the directory
            files = os.listdir(directory)

            # Check each file to find a match
            for file in files:
                # Check if the file starts with the given filename
                if file.startswith(file_name):
                    # Check if the file has a valid image extension
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        input_image_path = os.path.join(directory, file)

            # Output image path
            # output_path = input("Enter the name of the output image (remember png or jpg): ")
            output_image_path = "pearl_images/pearlified_" + file_name + ".png"
            new_width = int(input("Enter the new width: "))
            new_height = int(input("Enter the new height: "))
            available_colors = get_colors(color_names, color_map)
            if choice == 2:
                print("Converting to HSV...")
                new_image, colors_used = hsv_reformer(input_image_path, output_image_path, new_width, new_height, available_colors)
                # print(f"Saved to grid_{input_path}")

            elif choice == 3:
                print("Converting to HSL...")
                new_image, colors_used = hsl_reformer(input_image_path, output_image_path, new_width, new_height, available_colors)
                # print(f"Saved to grid_{input_path}")
            elif choice == 4:
                print("Converting to RGB...")
                new_image, colors_used = rgb_reformer(input_image_path, output_image_path, new_width, new_height, available_colors)
                # print(f"Saved to grid_{input_path}")

            grid_or_not = input("Do you want a grid? (y/n): ")
            if grid_or_not == "y":
                # output_image_path = "pearl_images/grid_" + input_path
                thick_line = int(input("Enter how often you want a thick line: "))
                new_image = upscale_and_add_grid(new_image, new_width, new_height, pixel_scaling, thick_line)
                output_image_path = "pearl_images/grid_pearlified_" + file_name + ".png"

            print(f"Saved to pearlified_{file_name}")
            transformed_dict = {inverted_color_map[key]: value for key, value in colors_used.items()}
            sorted_color_counts = dict(sorted(transformed_dict.items(), key=lambda x: x[1], reverse=True))
            # # Print the sorted dictionary
            # for color, count in sorted_color_counts.items():
            #     print(f'{color}: {count}')
            see_colors_used(sorted_color_counts, color_map)
            new_image.save(output_image_path)


        elif choice == 0:
            print("Exit")
            break
        else:  
            print("Invalid input")
            print("Try again")
        print()