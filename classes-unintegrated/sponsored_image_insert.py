from PIL import Image
from PIL import ImageFilter

class sponsoredImageInsertion:

    def insert(mg, sponsored_item):
        # retrieve the width and height of the image for the scale
        width, height = img.size

        # create a scale for insert to be resized to
        width_scale = round(width/4)
        height_scale = round(height/4)

        # create a copy of the original image
        img_copy = img.copy()

        # retrieve the proper sponsored item insert
        insert = Image.open('sponsored_items/' + sponsored_item + '.jpg')

        # resize the sponsored item
        insert = insert.resize((width_scale,height_scale), Image.ANTIALIAS)

        for x in range(width_scale):
            for y in range(height_scale):
                pixel = insert.getpixel((x, y))
                img_copy.putpixel((x, y), pixel)

        # return the image with the sponsored content inserted
        return img_copy

# Main which is just here for testing
if __name__ == '__main__':
    # Open the image file and read in its data so that we can access it
    img = Image.open('../fisher.jpeg')

   # new_img_one = sponsoredImageInsertion.insert(img, "pepsi")
    new_img_one = sponsoredImageInsertion.insert(img, "amazon")
    new_img_two = sponsoredImageInsertion.insert(img, "coca cola")


    # Save the image file so that we can view it
    new_img_one.save('amazon pic.jpg')
    new_img_two.save('coca cola pic.jpg')
