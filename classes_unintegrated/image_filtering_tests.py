import unittest
from PIL import Image
from image_handler import ImageFilterHandler
import filters
import os

MANUAL_CHECK = True


def images_equal(img1, img2):
    if img1.size == img2.size:
        width, height = img1.size
        for i in range(width):
            for j in range(height):
                r1, g1, b1 = img1.getpixel((i, j))
                r2, g2, b2 = img2.getpixel((i, j))
                if r1 != r2 or g1 != g2 or b1 != b2:
                    return False
        return True
    else:
        return False


class TestImageFiltering(unittest.TestCase):

    def test_get_filters_consistent_with_internal_filters(self):
        x = ImageFilterHandler.get_filters()
        y = ImageFilterHandler.filters
        self.assertEqual(len(x), len(y))

    def test_get_sponsored_items_consistent_with_internal_sponsored_items(self):
        self.assertTrue(False)

    def test_for_each_filter(self):
        base_img = Image.open('../fisher.jpeg')

        for f in ImageFilterHandler.filters:
            f_fed = getattr(filters, f).filter(base_img)
            # Asserts that the filter returned an image
            # self.assertTrue(isinstance(f_fed, Image))
            # Compare with original to ensure difference in pixels
            self.assertEqual(base_img.size, f_fed.size)
            self.assertFalse(images_equal(base_img, f_fed))

            h_fed = ImageFilterHandler.apply_filter(base_img, f)
            # Asserts that the handler returned an image
            # self.assertTrue(isinstance(h_fed, Image))
            # Compare with original to ensure difference in pixels
            self.assertEqual(base_img.size, f_fed.size)
            self.assertFalse(images_equal(base_img, h_fed))

            # Compare images filtered through handler and direct through filter
            self.assertTrue(images_equal(f_fed, h_fed))

            # Save filtered images for a manual visual check
            if MANUAL_CHECK:
                if not os.path.exists('test_image_output/'):
                    os.makedirs('test_image_output/')
                f_fed.save('test_image_output/' + f + '_f.jpg')
                h_fed.save('test_image_output/' + f + '_h.jpg')

    def test_apply_filter_on_invalid_id(self):
        self.assertTrue(False)
    # Integration testing not included yet


if __name__ == "__main__":
    unittest.main()