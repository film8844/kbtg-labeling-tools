import colorsys

def generate_colors(num_classes):
    """
    Generate a list of distinct colors for a specified number of classes.

    Parameters:
    - num_classes (int): The number of classes for which colors are needed.

    Returns:
    - colors (list of tuples): A list containing RGB tuples.
    """
    colors = []

    for i in range(num_classes):
        hue = i/num_classes
        lightness = 0.5  # You might adjust lightness as per your requirement
        saturation = 0.9  # Keeping saturation high to get vivid colors

        # Converting HSL to RGB, as it's often more useful in graphic libraries
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)

        # Scaling RGB to be in 0-255 range
        rgb = (int(r*255), int(g*255), int(b*255))

        # Converting RGB to Hexadecimal color code
        hex_color = "#{:02x}{:02x}{:02x}".format(*rgb)

        colors.append(hex_color)

    return colors


if __name__ == "__main__":

    # Example Usage:
    num_classes = 5
    colors = generate_colors(num_classes)

    print(colors)