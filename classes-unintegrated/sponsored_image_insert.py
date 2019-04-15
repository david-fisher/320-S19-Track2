from PIL import Image
from PIL import ImageFilter

class sponsored_image_insertion:

    def insert(img, sponsored_item):
        width, height = img.size;
        scale = (width/5)
        new_img = img.copy()
        insert = Image.open("/sponsored_items/" + sponsored_item + '.jpg')
        # resize the sponsored item
        insert = insert.resize(scale, Image.ANTIALIAS)

        for x in range(scale):
            for y in range(scale):
                new_img = new_img.putpixel((x, y), insert.getpixel(x, y))

        return new_img

# The entry point for our application. This is where the computer will
# begin running our code.

if __name__ == '__main__':
    # Open the image file and read in its data so that we can access it
    img = Image.open('../fisher.jpeg')

    # Run the code for the filter. We should replace filter_name
    # with the name of our filter.
    new_img = sponsored_image_insertion.insert(img, "coca cola")

    # Save the image file so that we can view it
    new_img.save('sponsored_item_pic.jpg')
