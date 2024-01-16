from PIL import Image

def create_outline(image_path, outline_color=(0, 0, 0), target_color=(236, 237, 237)):
    # Open the image
    image = Image.open(image_path)
    
    # Get the image dimensions
    width, height = image.size
    
    # Convert the image to a list of pixels
    pixels = list(image.getdata())
    
    # Convert the pixels to a 2D list
    pixels_2d = [pixels[i:i+width] for i in range(0, len(pixels), width)]
    
    # Function to check if a pixel is the target color
    def is_close_to_edge(x, y):
        # Check if the pixel is on the edge
        left = pixels_2d[y][x - 1]
        right = pixels_2d[y][x + 1]
        top = pixels_2d[y - 1][x]
        bottom = pixels_2d[y + 1][x]
        if left not in [target_color, outline_color] or right not in [target_color, outline_color] or top not in [target_color, outline_color] or bottom not in [target_color, outline_color]:
            return True
        return False
    
    # Function to check if a pixel is black
    # def is_black(x, y):
    #     return pixels_2d[y][x] == (0, 0, 0)
    
    # Iterate through each pixel and apply the outline
    for y in range(height):
        for x in range(width):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                continue
            if pixels_2d[y][x] == target_color and is_close_to_edge(x, y):
                pixels_2d[y][x] = outline_color
    
    # Flatten the 2D list back to a 1D list
    pixels = [pixel for row in pixels_2d for pixel in row]
    
    # Create a new image with the modified pixels
    new_image = Image.new("RGB", (width, height))
    new_image.putdata(pixels)
    
    # Save the new image
    new_image.save("outlined_image.png")

# Replace "input_image.png" with the path to your PNG image
create_outline("pearl_images\pearlified_ocarina.png")