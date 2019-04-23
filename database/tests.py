from django.test import TestCase
from database.models import Member, Post, Comment, CreditCard, Image, Filter
import tempfile


class MemberTestCase(TestCase): 

    # Test creating an member object
    def create_member(self,name,invitedby=None):
        return Member.objects.create(visibility=True,
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
        self.assertTrue(isinstance(new_member, Member))
        # since we created a new member, the number should increase to 1
        self.assertEqual(Member.objects.count(),1)

    # Get the object
    def test_get(self):
        new_member = self.create_member("new-user")
        # # get the username
        username = new_member.data()['username']
        # make sure I get the expected value 
        self.assertEqual("new-user",username)

    # Get the object by id
    def test_get_byid(self):
        new_member = self.create_member("new-user")
        # get id
        new_member_id = new_member.data()['id']
        # get member model by the id
        username = Member.objects.get(id=new_member_id).data()['username']
        # make sure I get the expected value 
        self.assertEqual("new-user",username)
    
    # Edit the object
    def test_edit(self):
        new_member = self.create_member("new-user")
        # update the value
        new_member.set_username("new-user")
        # get new username
        new_name = new_member.data()['username']
        self.assertEqual("new-user",new_name)

    # Delete the object
    def test_delete(self):
        new_member = self.create_member("new-user")

        # make sure the new object exists
        self.assertEqual(Member.objects.count(),1)
        
        # delete the object by id
        id = new_member.data()['id']
        Member.objects.filter(id=id).delete()
        
        # since we delete the object, there should be no member in the table.
        self.assertEqual(Member.objects.count(),0)
    
    # Test Invite by 
    def test_inviteby(self):
        idol = self.create_member('idol')
        member = self.create_member('member',idol)

        # check who invited member
        invitedby_id = member.data()['invitedby_id']
        who_invited_member = Member.objects.get(id=invitedby_id).data()['username']

        # Idol Invited Member
        self.assertEqual("idol",who_invited_member)

class PostTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return Member.objects.create(visibility=True,
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
        writer_id = new_post.data()['user_id']
        writer_name = Member.objects.get(id=writer_id).data()['username']
        self.assertEqual("new-user",writer_name)

class CommentTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return Member.objects.create(visibility=True,
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
                                      replies = replies,
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
        
        post_id = new_comment.data()['post_id']
        post_content = Post.objects.get(id=post_id).data()['content']

        self.assertEqual("hello",post_content)

class CreditCardTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return Member.objects.create(visibility=True,
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
        return Member.objects.create(visibility=True,
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
        return Member.objects.create(visibility=True,
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
          
       

    