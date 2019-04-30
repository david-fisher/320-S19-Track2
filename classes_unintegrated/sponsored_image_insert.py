from PIL import Image


class SponsoredImageInsertion:

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
        scaled_size = scale(width, height, factor)

        # resize the sponsored item
        insert = insert.resize(scaled_size)

        # decide where the upper left corner of the insert should be
        insert_place = (0, 0)

        # paste the insert into the image at insert_place
        img_copy.paste(insert, insert_place)

        # return the image with the sponsored content inserted
        return img_copy

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
        scaled_size = scale(width, height, factor)

        # resize the sponsored item
        insert = insert.resize(scaled_size)

        # paste the insert over the image
        img_copy.paste(insert, (0, 0), insert)

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
    new_img_one = sponsoredImageInsertion.insert(img, "amazon")
    new_img_two = sponsoredImageInsertion.insert(img, "coca cola")
    new_img_three = sponsoredImageInsertion.insert_png(img, 'cokecan')


    # Save the image file so that we can view it
    new_img_one.save('amazon pic.jpg')
    new_img_two.save('coca cola pic.jpg')
    new_img_three.save('coke can.jpg')
