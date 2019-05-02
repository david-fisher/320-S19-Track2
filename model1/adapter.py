# GET request to check if short_url exists

from members_only.models import ShortLink, Comment, Image

test_database = {"www.google.com": "1LfIc2e5AGfyMCZ5",
                 "www.moodle.umass.edu": "SAgQoYRsvSKNVXwd",
                 "www.umass.edu": "fQCPeau1TeR643Ft"}


class DBAdapter:

    @staticmethod
    def store_url(short_url, long_url):
        url = ShortLink.objects.create(short_token=short_url, originalURL=long_url)
        url.save()

    @staticmethod
    def check_short_url(short_url):
        if ShortLink.objects.filter(short_token=short_url).exists:
            return True
        else:
            return False

    @staticmethod
    # GET request to check if long_url exists
    def check_long_url(long_url):
        if ShortLink.objects.filter(originalURL=long_url).exists:
            return True
        else:
            return False

    @staticmethod
    # GET request to get long_url by short_url
    def get_long_url(short_url):
        long_url = ShortLink.objects.get(short_url=short_url)
        return long_url

    @staticmethod
    # GET request to get short_url by long_url
    def get_short_url(long_url):
        short_url = ShortLink.objects.get(originalURL=long_url)
        return short_url

    @staticmethod
    def store_comment(comment):
        comment_to_store = Comment.objects.create(content=comment)
        comment_to_store.save()

    @staticmethod
    def get_original_comment(comment_id):
        original_comment = Comment.objects.get(comment_id=comment_id)
        return original_comment

    @staticmethod
    def get_edited_comment(comment_id):
        original_comment = Comment.objects.get(comment_id=comment_id)
        return original_comment

    @staticmethod
    def store_image(image):
        image_to_store = Image.objects.create(current_image=image)
        image_to_store.save()

    @staticmethod
    def get_original_image(image_id):
        original_image = Image.objects.get(image_id=image_id)
        return original_image

    @staticmethod
    def get_filtered_image(image_id):
        filtered_image = Image.objects.get(image_id=image_id)
        return filtered_image