from PIL import Image
import numpy as np
from tqdm import tqdm

def get_colors(color_names, color_map):
    result = []
    
    for color_name in color_names:
        if color_name in color_map:
            result.append(color_map[color_name])
        else:
            result.append(None)  # or any default value if the color name is not found
    
    return result




def get_closest_color(target_color, available_colors):
    # distances = [((c[0] - target_color[0]) ** 2 + (c[1] - target_color[1]) ** 2 + (c[2] - target_color[2]) ** 2) ** 0.5 for c in available_colors]
    # closest_color_index = distances.index(min(distances))
    # return available_colors[closest_color_index]
    available_colors = np.array(available_colors)
    target_color = np.array(target_color)
    # print(available_colors)
    # print(target_color)
    distances = np.sqrt(np.sum((available_colors-target_color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))[0][0]
    # print("index", index_of_smallest)
    smallest_distance = available_colors[index_of_smallest]
    # return smallest_distance 

    # closest_color = closest(list_of_colors,color)
    # print("sl", smallest_distance)
    return tuple(smallest_distance)


def resize_image(input_image_path, output_image_path, new_width, new_height, available_colors):
    # Open the input image
    original_image = Image.open(input_image_path)
    original_image = original_image.convert('RGB')
    # Resize the image
    
    resized_image = original_image.resize((new_width, new_height))
    # resized_image.save("preprocessed.png")
    # Create a new image with the same mode and size as the resized image
    new_image = Image.new(resized_image.mode, resized_image.size)
    
    colors_used = {}
    # Iterate over each pixel in the resized image
    # print("HAHAHAHA")
    for x in range(new_width):
        for y in range(new_height):
            # Get the pixel color at the current position
            pixel_color = resized_image.getpixel((x, y))
            # print("pixel color: ",pixel_color)

            # Apply the color transformation function
            new_color = get_closest_color(pixel_color,available_colors)
            if new_color in colors_used:
                # If yes, increment the value by 1
                colors_used[new_color] += 1
            else:
                # If no, set the value to 1
                colors_used[new_color] = 1
            # print("new_color", new_color)
            # Set the pixel color in the new image
            new_image.putpixel((x, y), new_color)

    # Save the new image
    return new_image, colors_used
    # new_image.show()

if __name__ == "__main__":
    # Input image path
    input_image_path = "images/tut.png"

    # Output image path
    output_image_path = "pearl_image/uselessthing.jpg"

    # New width and height
    new_width = 60
    new_height = 60

    # Available colors (RGB values)
    color_names = ['red', 'blue', 'green', 'black', 'white']

    available_colors = get_colors(color_names, color_map)
    # print(result)
    # available_colors = [
    #     (0,200,0),
    #     (0,0,200),
    #     (200,0,0),
    #     # Add more colors as needed
    # ]

    # Resize the image using the closest available color and save the result
    resize_image(input_image_path, output_image_path, new_width, new_height, available_colors)

    print(f"Image resized and saved at {output_image_path} using the provided colors.")
