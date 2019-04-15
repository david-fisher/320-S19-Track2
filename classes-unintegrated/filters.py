from PIL import Image
from PIL import ImageFilter

def clubFilter(img):
    width, height = img.size
    new_img = img.copy()
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x,y))
            new_img.putpixel((x,y), (r, 0, b))

    return new_img


def filter_name(img):
    # Get the width and height (number of columns and rows) of the image
    width, height = img.size
    # Make a copy of the image so that we don't write over the original data.
    new_img = img.copy()

    # PUT YOUR CODE HERE

    return new_img

# The entry point for our application. This is where the computer will
# begin running our code.

if __name__ == '__main__':
    # Open the image file and read in its data so that we can access it
    img = Image.open('../fisher.jpeg')

    # Run the code for the filter. We should replace filter_name
    # with the name of our filter.
    new_img = mask(img)

    # Save the image file so that we can view it
    new_img.save('OutputImage.bmp')
