# from PIL import Image
from os import listdir
from os.path import isfile, join

import classes_unintegrated.adapter as Adapter
import classes_unintegrated.filters as Filters

items_dir_path = 'sponsored_items'
item_files = [f for f in listdir(items_dir_path) if isfile(join(items_dir_path, f))]

class ImageFilterHandler:

    filters = "grayscale", "club filter", "sepia", "negative", "flip", "mirror"
    sponsored_items = "coca cola", "coca cola can", "amazon", "pepsi"
    original_image = ""
    modified_image = ""
    done_by_admin = False


    def get_filters(self):
        # Currently only returns a list of filter names
        return self.filters


    def get_sponsored_items(self):
        # Currently only returns a list of sponsored item names
        return self.sponsored_items

    def apply_filter(self, image, filter_id, *args):
        # Currently just comparing against a string.
        # Eventually should be implemented with filter list from DB
        if filter_id == "grayscale":
            modified_image = Filters.Grayscale.filter(image)

        if filter_id == "club filter":
            modified_image = Filters.ClubFilter.filter(image)

        if filter_id == "sepia":
            modified_image = Filters.Sepia.filter(image)

        if filter_id == "negative":
            modified_image = Filters.Negative.filter(image)

        if filter_id == "flip":
            modified_image = Filters.Flip.filter(image)

        if filter_id == "mirror":
            modified_image = Filters.Mirror.filter(image)

        return modified_image


    def remove_filters(image):
        pass

    def __save_image(image):
        Adapter.store_image(image)


if __name__ == '__main__':
    print(item_files)

