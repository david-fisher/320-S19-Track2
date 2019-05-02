from PIL import Image
from os import listdir
from os.path import isfile, join
import re

sponsored_item_path = 'sponsored_items/'
items_dir_path = 'sponsored_items'

# retrieves sponsored_items files names from sponsored_items directory
sponsored_items = [f for f in listdir(items_dir_path) if isfile(join(items_dir_path, f))]


def item_info(i):
    name = re.sub('(\.[a-z]*)', '', i).title()
    return {'name': name}


sponsored_item_choices = dict((item, item_info(item)) for item in sponsored_items)


class SponsoredImageInsertion:

    filter_name = 'Sponsored Items'
    filter_args = {
        'Item': {
            'type': 'option',
            'choices': sponsored_item_choices
        }
    }

    @staticmethod
    def filter(img, sponsored_item):
        # create a copy of the original image
        img_copy = img.copy()

        # retrieve the proper sponsored item insert
        insert = Image.open(sponsored_item_path + sponsored_item)

        # retrieve the width and height of the image for the scale
        width, height = insert.size

        # decide the factor by which we want to scale the insert
        factor = .2

        # create a scale for insert to be re-sized to
        scaled_size = scale(width, height, factor)

        # resize the sponsored item
        insert = insert.resize(scaled_size)

        # decide where the upper left corner of the insert should be
        insert_place = (0, 0)

        # paste the insert into the image at insert_place
        img_copy.paste(insert, insert_place)

        # return the image with the sponsored content inserted
        return img_copy



def scale(width, height, factor):
    scaled_height = round(height * factor)
    scaled_width = round(width * factor)
    return (scaled_width, scaled_height)


# Main which is just here for testing
if __name__ == '__main__':
    # Open the image file and read in its data so that we can access it
    img = Image.open('../fisher.jpeg')

    # new_img_one = sponsoredImageInsertion.insert(img, "pepsi")
    new_img_one = SponsoredImageInsertion.filter(img, "amazon.jpg")
    new_img_two = SponsoredImageInsertion.filter(img, "coca cola.jpg")
    new_img_three = SponsoredImageInsertion.filter(img, 'cokecan.jpg')


    # Save the image file so that we can view it
    new_img_one.save('amazon pic.jpg')
    new_img_two.save('coca cola pic.jpg')
    new_img_three.save('coke can.jpg')
