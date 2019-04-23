import inspect
from os import listdir
from os.path import isfile, join
import re

import adapter as DBAdapter
import filters as filters

items_dir_path = 'sponsored_items'


class ImageFilterHandler:

    # retrieves filter class names from filters module
    filters = [f[0] for f in inspect.getmembers(filters, inspect.isclass) if f[1].__module__ == filters.__name__]
    # retrieves sponsored_items files names from sponsored_items directory
    sponsored_items = [f for f in listdir(items_dir_path) if isfile(join(items_dir_path, f))]
    original_image = ""
    modified_image = ""
    done_by_admin = False

    @staticmethod
    def get_filters():
        # Currently only returns a list of filter names
        def f_info(f):
            # Try pulling the name from the filter class
            try:
                name = getattr(filters, f).filter_name
            except AttributeError:
                name = re.sub('([a-z])([A-Z])', '\g<1> \g<2>', f)
            # Try pulling the preview_url from the filter class
            try:
                preview_loc = getattr(filters, f).filter_preview_url
            except AttributeError:
                preview_loc = re.sub('([a-z])([A-Z])', '\g<1> \g<2>', f)

            return name, f, preview_loc

        f_info_list = list(map(f_info, ImageFilterHandler.filters))
        return f_info_list

    @staticmethod
    def get_sponsored_items():
        # Currently only returns a list of sponsored item names
        def item_info(i):
            name = re.sub('(\.[a-z]*)', '', i).title()
            item_loc = ''
            return name, i, item_loc

        item_info_list = list(map(item_info, ImageFilterHandler.sponsored_items))
        return item_info_list

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
    print()
    print(ImageFilterHandler.sponsored_items)
    print()
    print(ImageFilterHandler.get_sponsored_items())
    print()
    print(ImageFilterHandler.get_filters())

