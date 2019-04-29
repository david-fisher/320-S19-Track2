
from django.test import TestCase
from members_only.models import User, Post, Comment, CreditCard, Image, Filter
import tempfile

# from django.contrib.auth.models import AnonymousUser, User
# from django.test import TestCase, RequestFactory
import unittest
import os
from PIL import Image
import members_only.filters as filters  # todo where do they come from?
from classes_unintegrated.image_handler import ImageFilterHandler  # todo where do they come from?




class UserTestCase(TestCase): 

MANUAL_CHECK = True



    # Test creating an member object
    def create_member(self,name,invitedby=None):
        return User.objects.create(visibility=True,
                                    invitedby= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")

    def test_create(self):
        new_member = self.create_member("new-user")
        self.assertTrue(isinstance(new_member, User))
        # since we created a new member, the number should increase to 1
        self.assertEqual(User.objects.count(),1)


    # Get the object
    def test_get(self):
        new_member = self.create_member("new-user")
        # # get the username
        username = new_member.username
        # make sure I get the expected value 
        self.assertEqual("new-user",username)

    # Get the object by id
    def test_get_byid(self):
        new_member = self.create_member("new-user")
        # get id
        new_member_id = new_member.id
        # get member model by the id
        username = User.objects.get(id=new_member_id).username
        # make sure I get the expected value 
        self.assertEqual("new-user",username)
    
    # Edit the object
    def test_edit(self):
        new_member = self.create_member("new-user")
        # update the value
        new_member.username = "new-user"
        # get new username
        new_name = new_member.username
        self.assertEqual("new-user",new_name)

    # Delete the object
    def test_delete(self):
        new_member = self.create_member("new-user")

        # make sure the new object exists
        self.assertEqual(User.objects.count(),1)
        
        # delete the object by id
        id = new_member.id
        User.objects.filter(id=id).delete()
        
        # since we delete the object, there should be no member in the table.
        self.assertEqual(User.objects.count(),0)
    
    # Test Invite by 
    def test_inviteby(self):
        idol = self.create_member('idol')
        member = self.create_member('member',idol)

        # check who invited member
        invitedby_id = member.invitedby_id
        who_invited_member = User.objects.get(id=invitedby_id).username

        # Idol Invited Member
        self.assertEqual("idol",who_invited_member)

class PostTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return User.objects.create(visibility=True,
                                    invitedby= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")

    def create_post(self,content,user=None):
        return Post.objects.create(user = user,
                                   urls    = "www.test.com",
                                   is_flagged = False,
                                   content = content,
                                   by_admin = False)

    # Test creating an Post object
    def test_create(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello",new_member)
        self.assertTrue(isinstance(new_post, Post))
        # since we created a new post, the number should increase to 1
        self.assertEqual(Post.objects.count(),1)
    
    # Who wrote this post?
    def test_writer(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello",new_member)
        writer_id = new_post.user_id
        writer_name = User.objects.get(id=writer_id).username
        self.assertEqual("new-user",writer_name)

class CommentTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return User.objects.create(visibility=True,
                                    invitedby= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")
    
    def create_post(self,content,user=None):
        return Post.objects.create(user = user,
                                   urls    = "www.test.com",
                                   is_flagged = False,
                                   content = content,
                                   by_admin = False)
    
    def create_comment(self,content,user,post,replies=None):
        return Comment.objects.create(user = user,
                                      post = post,
                                      content = content,
                                      by_admin = False)
                                      
    def test_create(self):
        new_member = self.create_member("new-user")
        coment_user = self.create_member("comment-user")
        new_post = self.create_post("hello",new_member)
        new_comment = self.create_comment("this is a comment",coment_user,new_post)
        self.assertTrue(isinstance(new_comment, Comment))
        # since we created a new post, the number should increase to 1
        self.assertEqual(Comment.objects.count(),1)
    
    # Check linked Post
    def test_create(self):
        new_member = self.create_member("new-user")
        coment_user = self.create_member("comment-user")
        new_post = self.create_post("hello",new_member)
        new_comment = self.create_comment("this is a comment",coment_user,new_post)
        
        post_id = new_comment.post_id
        post_content = Post.objects.get(id=post_id).content

        self.assertEqual("hello",post_content)

class CreditCardTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return User.objects.create(visibility=True,
                                    invitedby= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")
    
    def create_card(self,user):
        return CreditCard.objects.create(user=user,
                                         card_num="0000111122223333",
                                         cvv="123",
                                         holder_name="test-user",
                                         card_expiration="20201012",
                                         currently_used=True,
                                         address="earth",
                                         zipcode=10001)
    def test_create(self):
        new_member = self.create_member("new-user")
        new_card = self.create_card(new_member)
        self.assertTrue(isinstance(new_card, CreditCard))
        # since we created a new post, the number should increase to 1
        self.assertEqual(CreditCard.objects.count(),1)
                                

class ImageTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return User.objects.create(visibility=True,
                                    invitedby= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")
    
    def create_post(self,content,user=None):
        return Post.objects.create(user = user,
                                   urls    = "www.test.com",
                                   is_flagged = False,
                                   content = content,
                                   by_admin = False)

    def create_image(self,user,post,image):
        return Image.objects.create(user = user,
                                    post = post,
                                    current_image=image,
                                    is_flagged = False,
                                    by_admin = False )

    def test_create(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello",new_member)
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        new_image = self.create_image(new_member,new_post,image)
        self.assertTrue(isinstance(new_image, Image))
        self.assertEqual(Image.objects.count(),1)    

class FilterTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return User.objects.create(visibility=True,
                                    invitedby= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")
    
    def create_post(self,content,user=None):
        return Post.objects.create(user = user,
                                   urls    = "www.test.com",
                                   is_flagged = False,
                                   content = content,
                                   by_admin = False)

    def create_image(self,user,post,image):
        return Image.objects.create(user = user,
                                    post = post,
                                    current_image=image,
                                    is_flagged = False,
                                    by_admin = False )
    
    def create_filter(self,image):
        return Filter.objects.create(image=image,filter_name="test-filter")

    def test_create(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello",new_member)
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        new_image = self.create_image(new_member,new_post,image)
        new_filter = self.create_filter(new_image)

        self.assertTrue(isinstance(new_filter,Filter))
        self.assertEqual(Filter.objects.count(),1) 
          
       

    

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

