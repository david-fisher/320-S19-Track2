from PIL import Image
from os import listdir
from os.path import isfile, join
import re


class ClubFilter:

    # Class' attributes
    filter_name = "Club"
    filter_preview_url = ""

    # Filter method
    @staticmethod
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
    filter_name = "Grayscale"

    # Filter method
    @staticmethod
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
    filter_name = "Negative"

    # Filter method
    @staticmethod
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


class Sepia:

    # Class' attributes
    filter_name = "Sepia"

    # Filter method
    @staticmethod
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
                sepia_r = (r * 0.393 + g * 0.769 + b * 0.189)
                sepia_g = (r * 0.349 + g * 0.686 + b * 0.168)
                sepia_b = (r * 0.272 + g * 0.534 + b * 0.131)
                if sepia_r > 255:
                    sepia_r = 255
                if sepia_g > 255:
                    sepia_g = 255
                if sepia_b > 255:
                    sepia_b = 255
                img_copy.putpixel((x,y), (int(sepia_r), int(sepia_g), int(sepia_b)))

        return img_copy

class Flip:

    # Class' attributes
    filter_name = "Flip"

    # Filter method
    @staticmethod
    def filter(img):
        # Retrieve the width and height of the image
        width, height = img.size

        # Create a copy of the original image
        img_copy = img.copy()

        # Two for loops in order to change each pixel
        for x in range(width):
            for y in range(height):
                # Take the pixel at (x, y)
                r, g, b = img.getpixel((width-x-1, y))
                # Subtract the r g b values from 255 in order to get the inverted values
                img_copy.putpixel((x, y), (r, g, b))

        return img_copy

class Mirror:

    # Class' attributes
    filter_name = "Mirror"

    # Filter method
    @staticmethod
    def filter(img):
        # Retrieve the width and height of the image
        width, height = img.size

        # Create a copy of the original image
        img_copy = img.copy()

        # Two for loops in order to change each pixel
        for x in range(width//2):
            for y in range(height):
                # Take the pixel at (x, y)
                r, g, b = img.getpixel((width-x-1, y))
                # Subtract the r g b values from 255 in order to get the inverted values
                img_copy.putpixel((x, y), (r, g, b))

        return img_copy


sponsored_item_path = 'sponsored_items/'
items_dir_path = 'sponsored_items'

# retrieves sponsored_items files names from sponsored_items directory
sponsored_items = [f for f in listdir(items_dir_path) if isfile(join(items_dir_path, f))]


def item_info(i):
    name = re.sub('(\.[a-z]*)', '', i).title()
    return {'name': name}


sponsored_item_choices = dict((item, item_info(item)) for item in sponsored_items)


class SponsoredImageInsertion:
    @staticmethod
    def __scale(width, height, factor):
        scaled_height = round(height * factor)
        scaled_width = round(width * factor)
        return scaled_width, scaled_height

    filter_name = 'Sponsored Items'
    filter_args = {
        'item': {
            'name': 'Item',
            'type': 'option',
            'choices': sponsored_item_choices
        }
    }

    @staticmethod
    def filter(img, item='default'):
        if item == 'default' or item not in sponsored_items:
            item = sponsored_items[0]

        # create a copy of the original image
        img_copy = img.copy()

        # retrieve the proper sponsored item insert
        insert = Image.open(sponsored_item_path + item)

        # retrieve the width and height of the image for the scale
        width, height = insert.size

        # decide the factor by which we want to scale the insert
        factor = .2

        # create a scale for insert to be re-sized to
        scaled_size = SponsoredImageInsertion.__scale(width, height, factor)

        # resize the sponsored item
        insert = insert.resize(scaled_size)

        # decide where the upper left corner of the insert should be
        insert_place = (0, 0)

        # paste the insert into the image at insert_place
        img_copy.paste(insert, insert_place)

        # return the image with the sponsored content inserted
        return img_copy


if __name__ == '__main__':
    # Open the image file and read in its data so that we can access it
    img = Image.open('../fisher.jpeg')

    new_img_one = ClubFilter.filter(img)
    new_img_two = Grayscale.filter(img)
    new_img_three = Negative.filter(img)
    new_img_four = Sepia.filter(img)
    new_img_five = Mirror.filter(img)
    new_img_six = Flip.filter(img)
    new_img_seven = Blur.filter(img)

    new_img_one.save('club_filter.jpg')
    new_img_two.save('grayscale.jpg')
    new_img_three.save('negative.jpg')
    new_img_four.save('sepia.jpg')
    new_img_five.save('mirror.jpg')
    new_img_six.save('flip.jpg')
    new_img_seven.save('blur.jpg')