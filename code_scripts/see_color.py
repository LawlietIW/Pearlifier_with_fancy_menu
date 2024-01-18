from PIL import Image, ImageDraw, ImageFont

def create_color_image(color_map):
    # Set the image size and font size
    image_size = (500, len(color_map) * 30)
    font_size = 20
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Draw each color and its name on the image
    y_position = 10
    for color_name, rgb_value in color_map.items():
        draw.rectangle([10, y_position, 200, y_position + 20], fill=rgb_value)
        draw.text((220, y_position), f"{color_name}", font=font, fill="black")
        y_position += 30

    # Save the image or display it
    image.save("color_palettes/color_palette.png")
    image.show()

# Example usage


# create_color_image(color_map)


def see_colors_used(sorted_color_counts, color_map):
    # Set the image size and font size
    image_size = (500, len(sorted_color_counts) * 30)
    font_size = 20
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Draw each color and its name on the image
    y_position = 10
    for color_name, count in sorted_color_counts.items():
        rgb_value = color_map[color_name]
        draw.rectangle([10, y_position, 200, y_position + 20], fill=rgb_value)
        draw.text((220, y_position), f"{color_name}: {count}", font=font, fill="black")
        y_position += 30

    # Save the image or display it
    image.save("sorted_color_palette.png")
    image.show()