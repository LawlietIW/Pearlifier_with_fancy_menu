from PIL import Image
from tqdm import tqdm
def upscale_and_add_grid(original_image, width, height, pixel_scaling, thick_line):
    # Open the image
    # original_image = Image.open(image_path)

    # Get the width and height of the original image
    # width, height = original_image.size

    thick_line_extra_width = (width - 1) // thick_line 
    # print(thick_line_extra_width)
    thick_line_extra_height = (height - 1) // thick_line

    # Create a new image with the expanded size after upscaling
    new_width = width * pixel_scaling + (width - 1) + thick_line_extra_width # New width after upscaling and adding gaps
    new_height = height * pixel_scaling + (height - 1)  + thick_line_extra_height  # New height after upscaling and adding gaps
    new_image = Image.new("RGB", (new_width, new_height), color="black")

    # Iterate through each pixel in the original image
    for x in tqdm(range(width)):
        for y in range(height):
            # Get the color of the current pixel
            pixel_color = original_image.getpixel((x, y))

            # Calculate the position in the new image for the current pixel after upscaling
            new_x = x * (pixel_scaling + 1)  + x // thick_line
            new_y = y * (pixel_scaling + 1)  + y // thick_line

            # Set the color of the corresponding pixels in the new image after upscaling
            for i in range(pixel_scaling):
                for j in range(pixel_scaling):
                    new_image.putpixel((new_x + i, new_y + j), pixel_color)

    # Save the resulting image
    return new_image

# # Example usage
# input_image_path = "pearl_image/uselessthing.jpg"
# output_image_path = "grid.png"
# pixel_scaling = 5  # You can adjust this to change the size of the grid
# thick_line = 5

# upscale_and_add_grid(input_image_path, output_image_path, pixel_scaling, thick_line)
