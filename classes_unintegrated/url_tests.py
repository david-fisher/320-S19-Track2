import unittest


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

if __name__ == "__main__":
    unittest.main()