import inspect
from os import listdir
from os.path import isfile, join

import filters

import classes_unintegrated.adapter as DBAdapter

items_dir_path = 'sponsored_items'


class ImageFilterHandler:

    # retrieves filter class names from filters module
    filters = [f[0] for f in inspect.getmembers(filters, inspect.isclass) if f[1].__module__ == filters.__name__]
    # retrieves sponsored_items files names from sponsored_items directory
    sponsored_items = [f for f in listdir(items_dir_path) if isfile(join(items_dir_path, f))]
    original_image = ""
    modified_image = ""
    done_by_admin = False

    def get_filters(self):
        # Currently only returns a list of filter names
        return self.filters

    def get_sponsored_items(self):
        # Currently only returns a list of sponsored item names
        return self.sponsored_items

    @staticmethod
    def apply_filter(image, filter_id, *args):
        # Eventually should be implemented with filter list from DB
        if hasattr(filters, filter_id):
            filter_class = getattr(filters, filter_id)
            return filter_class.filter(image)
        else:
            # invalid filter_id
            print('invalid filter_id')
            return "uh oh, should probably do something about this"

    def remove_filters(self, image):
        pass

    def __save_image(self, image):
        DBAdapter.store_image(image)


if __name__ == '__main__':
    print([f[0] for f in inspect.getmembers(filters, inspect.isclass) if f[1].__module__ == filters.__name__])
    print(ImageFilterHandler.filters)
    print(ImageFilterHandler.sponsored_items)

    # img = Image.open('../fisher.jpeg')
    # new_img_one = ImageFilterHandler.apply_filter(img, 'ClubFilter')
    # new_img_one.save('club_filter.jpg')

