import inspect
from os import listdir
from os.path import isfile, join
import re
import json

import filters as filters

items_dir_path = 'sponsored_items'


class ImageFilterHandler:

    # retrieves filter class names from filters module
    filters = [f[0] for f in inspect.getmembers(filters, inspect.isclass) if f[1].__module__ == filters.__name__]
    # retrieves sponsored_items files names from sponsored_items directory
    sponsored_items = [f for f in listdir(items_dir_path) if isfile(join(items_dir_path, f))]

    @staticmethod
    def __dic_to_string(dic):
        return json.dumps(dic, separators=(',', ':'))

    @staticmethod
    def __string_to_dic(s):
        return json.loads(s)

    @staticmethod
    def get_filters():  # todo: each filters arguments should also be included
        # todo: probably want the filter classes to provide their argument formats in their attributes
        # Currently only returns a list of filter names
        def f_info(f):
            # Try pulling the name from the filter class
            try:
                name = getattr(filters, f).filter_name
            except AttributeError:
                name = re.sub('([a-z])([A-Z])', '\g<1> \g<2>', f)
            # Try pulling the args format from the filter class
            try:
                args = getattr(filters, f).filer_args
            except AttributeError:
                args = {}

            dic = {
                'name': name,
                'args': args
            }

            return dic

        # f_info_list = list(map(f_info, ImageFilterHandler.filters))
        f_info_list = dict((f, f_info(f)) for f in ImageFilterHandler.filters)
        # todo: First pass list through serializer
        return f_info_list

    @staticmethod
    def get_sponsored_items():  # todo: make private and provide as arguments for get_filters
        # Currently only returns a list of sponsored item names
        def item_info(i):
            name = re.sub('(\.[a-z]*)', '', i).title()
            return name, i

        item_info_list = list(map(item_info, ImageFilterHandler.sponsored_items))
        # todo: First pass list through serializer
        return item_info_list

    @staticmethod
    # applies all filter: arguments pairs in filters_dic to image
    # filters_dic assumed to be formatted like:
    # {
    #     'filter_id1': {
    #         'name': 'Filter ID1',
    #         'args': {
    #             'arg1': 'val1',
    #             'arg2': 'val2'
    #         }
    #     },
    #     'filter2_id2': {
    #         'name': 'Filter ID2',
    #         'args': {}
    #     }
    # }
    def __apply_filters(image, filters_dic):
        filtered_image = image
        for f_id in filters_dic:
            # checking for filter class of name f_id
            try:
                filter_class = getattr(filters, f_id)
            # invalid filter name
            except AttributeError:
                print('invalid filter_id: ' + f_id)
                continue

            filter_args = filters_dic[f_id]['args']
            if filter_args:
                # trying to call filter w/ filter_args
                try:
                    filtered_image = filter_class.filter(image, **filter_args)
                # invalid filter arguments
                except TypeError:
                    print('invalid filter_args: ')
                    print(filter_args)
                    continue
            else:
                filtered_image = filter_class.filter(image)
        return filtered_image

    @staticmethod
    def apply_filters(image, filter_ids, *args):  # todo: Should take in arguments needed to post
        filters_dic = filter_ids  # todo: see __apply_filters() for format
        filtered_image = ImageFilterHandler.__apply_filters(image, filters_dic)
        filters_as_str = ImageFilterHandler.__dic_to_string(filters_dic)
        # todo: Post the filtered image
        return filtered_image

    @staticmethod
    def remove_filters(image_id, bad_filters):
        # todo: to remove filters, may need a method to give frontend current applied filters
        # todo: get image's curr filters from db and parse into dict
        curr_filters = ImageFilterHandler.__string_to_dic(image_id.filters)
        # only remove if there are any filters currently applied
        if curr_filters:
            image = image_id.image  # todo
            unwanted_filters = bad_filters  # todo
            filters_to_apply = [f for f in curr_filters if f not in unwanted_filters]
            filtered_image = ImageFilterHandler.__apply_filters(image, filters_to_apply)
            filters_as_str = ImageFilterHandler.__dic_to_string(filters_to_apply)
            # todo: put the filtered_image to the original
            return filtered_image
        # if not image_id.filters:
        #     return "No can do"
        # else:
        #     original = image_id.parent
        #     applied_filters = image_id.filters
        #     for each filter in applied_filters:
        #         if filter != bad_filter:
        #             original = apply_filter(original, filter)
        #     put(original, image_id)


if __name__ == '__main__':
    # print([f[0] for f in inspect.getmembers(filters, inspect.isclass) if f[1].__module__ == filters.__name__])
    # print(ImageFilterHandler.filters)
    # print()
    # print(ImageFilterHandler.sponsored_items)
    # print()
    # print(ImageFilterHandler.get_sponsored_items())
    # print()
    print(ImageFilterHandler.get_filters())
    # d = {'hello': 'my', 'name': 'is'}
    # print(d)
    # print()
    # j = json.dumps(d, separators=(',', ':'))
    # print(j)
    # print()
    # b = json.loads(j)
    # print(b)

