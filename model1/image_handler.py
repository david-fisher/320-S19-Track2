import inspect
from os import listdir
from os.path import isfile, join
import re
import json
from members_only.models import User, Post, Comment, CreditCard, Image, Filter

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
    # Format should look like:
    # {
    #     'FilterOne': {
    #         'name': 'One',
    #         'args': {}
    #     },
    #     'FilterTwo': {
    #         'name': 'Two',
    #         'args': {
    #             'arg1': {
    #                 'name': 'Argument 1'
    #                 'type': 'option',
    #                 'choices': {
    #                     'choice1': {
    #                         'name': 'Choice 1'
    #                     }
    #                 }
    #             }
    #         }
    #     }
    # }
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
                args = getattr(filters, f).filter_args
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

    # @staticmethod
    # def get_sponsored_items():  # todo: make private and provide as arguments for get_filters
    #     # Currently only returns a list of sponsored item names
    #     def item_info(i):
    #         name = re.sub('(\.[a-z]*)', '', i).title()
    #         return name, i
    #
    #     item_info_list = list(map(item_info, ImageFilterHandler.sponsored_items))
    #     # todo: First pass list through serializer
    #     return item_info_list

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
                    filtered_image = filter_class.filter(filtered_image, **filter_args)
                # invalid filter arguments
                except TypeError:
                    print('invalid filter_args: ')
                    print(filter_args)
                    continue
            else:
                filtered_image = filter_class.filter(filtered_image)
        return filtered_image

    @staticmethod
    def apply_filters(image, filter_ids):  # todo: Should take in arguments needed to post
        filters_dic = filter_ids  # todo: see __apply_filters() for format
        filtered_image = ImageFilterHandler.__apply_filters(image, filters_dic)
        filters_as_str = ImageFilterHandler.__dic_to_string(filters_dic)
        # todo: Post the filtered image

        return filtered_image

    @staticmethod
    def remove_filters(image_id, bad_filters):
        # todo: to remove filters, may need a method to give frontend current applied filters
        # todo: get image's curr filters from db and parse into dict
        image_obj = Image.objects.get(id=image_id)
        curr_filters_used = image_obj.filters_used  # todo
        curr_filters_dic = ImageFilterHandler.__string_to_dic(curr_filters_used)

        # only remove if there are any filters currently applied
        if curr_filters_dic:
            unwanted_filters = bad_filters  # todo
            new_filters_dic = [f for f in curr_filters_dic if f not in unwanted_filters]

            curr_image = image_obj.image_original.current_image  # todo Not very sure about this
            new_image = ImageFilterHandler.__apply_filters(curr_image, new_filters_dic)

            new_filters_used = ImageFilterHandler.__dic_to_string(new_filters_dic)

            # update the Image with the new filtered_image and filters_Used
            updated_image = Image(id=image_id, current_image=new_image, filters_used=new_filters_used)
            updated_image.save()

            return new_image


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

