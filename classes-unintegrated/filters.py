from PIL import Image

class Filters:

    def club_filter(img):

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


if __name__ == '__main__':
    # Open the image file and read in its data so that we can access it
    img = Image.open('../fisher.jpeg')

    # Run the code for the filter. We should replace filter_name
    # with the name of our filter.
    new_img = Filters.clubFilter(img)

    # Save the image file so that we can view it
    new_img.save('OutputImage.bmp')
