from PIL import Image

class SponsoredImageInsertion:

    @staticmethod
    def insert(img, sponsored_item):
        # create a copy of the original image
        img_copy = img.copy()

        # retrieve the proper sponsored item insert
        insert = Image.open('sponsored_items/' + sponsored_item + '.jpg')

        # retrieve the width and height of the image for the scale
        width, height = insert.size

        # decide the factor by which we want to scale the insert
        factor = .2

        # create a scale for insert to be re-sized to
        scaled_size = SponsoredImageInsertion.scale(width, height, factor)

        # resize the sponsored item
        insert = insert.resize(scaled_size)

        # decide where the upper left corner of the insert should be
        insert_place = (0, 0)

        # paste the insert into the image at insert_place
        img_copy.paste(insert, insert_place)

        # return the image with the sponsored content inserted
        return img_copy

    @staticmethod
    def insert_png(img, sponsored_item):
        # create a copy of the original image
        img_copy = img.copy()

        # retrieve the proper sponsored item insert
        insert = Image.open('sponsored_items/' + sponsored_item + '.png')

        # retrieve the width and height of the image for the scale
        width, height = insert.size

        # decide factor for which to scale the insert to
        factor = .2

        # create a scale for insert to be re-sized to
        scaled_size = SponsoredImageInsertion.scale(width, height, factor)

        # resize the sponsored item
        insert = insert.resize(scaled_size)

        # paste the insert over the image
        img_copy.paste(insert, (0, 0), insert)

        # return the image with the sponsored content inserted
        return img_copy

    @staticmethod
    def scale(width, height, factor):
        scaled_height = round(height * factor)
        scaled_width = round(width * factor)
        return (scaled_width, scaled_height)


class ClubFilter:

    # Class' attributes
    filter_name = "club_filter"
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
    filter_name = "grayscale"
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
    filter_name = "sepia"
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
                # Subtract the r g b values from 255 in order to get the inverted values
                sepiaR = (r * 0.393 + g * 0.769 + b * 0.189)
                sepiaG = (r * 0.349 + g * 0.686 + b * 0.168)
                sepiaB = (r * 0.272 + g * 0.534 + b * 0.131)
                if sepiaR > 255:
                    sepiaR = 255
                if sepiaG > 255:
                    sepiaG = 255
                if sepiaB > 255:
                    sepiaB = 255
                img_copy.putpixel((x,y), (int(sepiaR), int(sepiaG), int(sepiaB)))

        return img_copy
