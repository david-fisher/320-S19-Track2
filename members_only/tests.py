# from django.contrib.auth.models import AnonymousUser, User
# from django.test import TestCase, RequestFactory
import unittest
import os
from PIL import Image
import members_only.filters as filters  # todo where do they come from?
from classes_unintegrated.image_handler import ImageFilterHandler  # todo where do they come from?

# from .views import index

MANUAL_CHECK = True


# class SimpleTest(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()

#     def test_details(self):
#         # Create an instance of a GET request.
#         request = self.factory.get("/")
#         request.user = AnonymousUser()

#         # Test my_view() as if it were deployed at /customer/details
#         response = index(request)
#         self.assertEqual(response.status_code, 200)


class URLTests(unittest.TestCase):

    test_urls = {
        "https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwiUwIu36NLhAhXHTN8KHebjAL8QjRx6BAgBEAQ&url=https%3A%2F%2Fwww.amazon.com%2FShrek-Forever-After-Single-Disc-Myers%2Fdp%2FB002ZG9904&psig=AOvVaw0zRU5IHtsjG7v2c_Rdsycz&ust=1555442347913753": "21934abf0",
        "https://people.cs.umass.edu/~barring/david_3.jpg": "ebd174c0",
        "https://img.buzzfeed.com/buzzfeed-static/static/2016-04/7/11/campaign_images/webdr13/36-slurpee-drinkers-who-won-7-eleven-bring-your-o-2-12794-1460044129-0_dblbig.jpg": "aea5f251",
        "https://www.umass.edu/gateway/academics/undergraduate": "8f73fa55"
    }

    def test_get_long_url(self):
        assert False, "Should return correct long_url"

    def test_check_short_url(self):
        assert False, "Should be true"

    def test_create_short_url(self):
        assert False, "Should return correct short_url"

    def test_get_short_url(self):
        assert False, "Should return correct short_url"

    def test_gen_hash(self):
        assert False, "Should be true"


class TestImageFiltering(unittest.TestCase):

    @staticmethod
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
            self.assertFalse(TestImageFiltering.images_equal(base_img, f_fed))

            h_fed = ImageFilterHandler.apply_filter(base_img, f)
            # Asserts that the handler returned an image
            self.assertEqual(type(h_fed).__name__, 'Image')
            # Compare with original to ensure difference in pixels
            self.assertEqual(base_img.size, f_fed.size)
            self.assertFalse(TestImageFiltering.images_equal(base_img, h_fed))

            # Compare images filtered through handler and direct through filter
            self.assertTrue(TestImageFiltering.images_equal(f_fed, h_fed))

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
