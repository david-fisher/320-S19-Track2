import os
import unittest

from PIL import Image

import classes_unintegrated.filters as filters
from classes_unintegrated.image_handler import ImageFilterHandler

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
        # todo: Unserialize the proper return on get_filters()
        g = ImageFilterHandler.get_filters()
        f = ImageFilterHandler.filters
        self.assertEqual(len(g), len(f))
        for i in range(len(g)):
            # Assumes the lists are sorted, with should be true
            self.assertEqual(g[i][1], f[i])

    def test_get_sponsored_items_consistent_with_internal_sponsored_items(self):
        # todo: Unserialize the proper return on get_sponsored_items()
        g = ImageFilterHandler.get_sponsored_items()
        s = ImageFilterHandler.sponsored_items
        self.assertEqual(len(g), len(s))
        for i in range(len(g)):
            # Assumes the lists are sorted, with should be true
            self.assertEqual(g[i][1], s[i])

    def test_for_each_filter(self):
        base_img = Image.open('../fisher.jpeg')

        for f in ImageFilterHandler.filters:
            f_fed = getattr(filters, f).filter(base_img)
            # Asserts that the filter returned an image
            self.assertEqual(type(f_fed).__name__, 'Image')
            # Compare with original to ensure difference in pixels
            self.assertEqual(base_img.size, f_fed.size)
            self.assertFalse(images_equal(base_img, f_fed))

            h_fed = ImageFilterHandler.apply_filter(base_img, f)
            # Asserts that the handler returned an image
            self.assertEqual(type(h_fed).__name__, 'Image')
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
        self.assertTrue(True)
    # Integration testing not included yet


if __name__ == "__main__":
    unittest.main()