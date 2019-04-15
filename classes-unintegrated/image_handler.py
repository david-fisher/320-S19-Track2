# from PIL import Image
from os import listdir
from os.path import isfile, join

items_dir_path = 'sponsored_items'
item_files = [f for f in listdir(items_dir_path) if isfile(join(items_dir_path, f))]


def get_filters():
    pass


def get_sponsored_items():
    pass


def apply_filter(image, filter_id, *args):
    pass


def remove_filters(image):
    pass


if __name__ == '__main__':
    print(item_files)

