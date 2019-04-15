from PIL import Image

class ClubFilter:

    # Class' attributes
    filter_name = "club_filter"
    filter_preview_url = ""

    # Filter method
    def filter(img):
        # Retrieve the width and height of the image
        width, height = img.size

        # Create a copy of the original image
        img_copy = img.copy()

        # Two for loops in order to change each pixel
        for x in range(width):
            for y in range(height):
                # Take the pixel at (x, y)
                r, g, b = img.getpixel((x,y))
                # Remove the Green values from that pixel and apply the change to the image
                img_copy.putpixel((x,y), (r, 0, b))

        return img_copy

class Grayscale:

    # Class attributes
    filter_name = "grayscale"
    filter_preview_url = ""

    # Filter method
    def filter(img):
        # Retrieve the width and height of the image
        width, height = img.size

        # Create a copy of the original image
        img_copy = img.copy()

        # Two for loops in order to change each pixel
        for x in range(width):
            for y in range(height):
                # Take the pixel at (x, y)
                r, g, b = img.getpixel((x, y))
                average = round(((r + b + g)/3))
                # Change the RGB values to make the photo gray
                img_copy.putpixel((x, y), (average, average, average))

        return img_copy

class Negative:

    # Class' attributes
    filter_name = "negative"
    filter_preview_url = ""

    # Filter method
    def filter(img):
        # Retrieve the width and height of the image
        width, height = img.size

        # Create a copy of the original image
        img_copy = img.copy()

        # Two for loops in order to change each pixel
        for x in range(width):
            for y in range(height):
                # Take the pixel at (x, y)
                r, g, b = img.getpixel((x,y))
                # Subtract the r g b values from 255 in order to get the inverted values
                img_copy.putpixel((x,y), (255-r, 255-g, 255-b))

        return img_copy

if __name__ == '__main__':
    # Open the image file and read in its data so that we can access it
    img = Image.open('../fisher.jpeg')

    new_img_one = ClubFilter.filter(img)
    new_img_two = Grayscale.filter(img)
    new_img_three = Negative.filter(img)

    new_img_one.save('club_filter.jpg')
    new_img_two.save('grayscale.jpg')
    new_img_three.save('negative.jpg')
