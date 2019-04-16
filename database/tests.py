from django.test import TestCase
from database.models import Member
# Create your tests here.

class DataTestCase(TestCase): 
    ## create test-user
    def create_member(self,title="df"):
        return Member.objects.create(ccid=[1,2],
                                    postid=[2,3,4], 
                                    visibility=[1,2,3],
                                    invitedby=[1],
                                    email="email@email.com",
                                    password="pwd",
                                    username="test-user",
                                    points="10",
                                    usertype="Member",
                                    logintime="201902101120",
                                    logouttime="201902101121",
                                    isVerified=True,
                                    birthday="19980903",
                                    address="earth")

    # Test creating an member object
    def test_create(self):
        new_member = self.create_member()
        self.assertTrue(isinstance(new_member, Member))
        # since we created a new member, the number should increase to 1
        self.assertEqual(Member.objects.count(),1)

    # Get the object
    def test_get(self):
        new_member = self.create_member()
        # get the username
        original_username = new_member.get_username()
        # make sure I get the expected value 
        self.assertEqual("test-user",original_username)
    
    # # Edit the object
    def test_edit(self):
        new_member = self.create_member()
        # update the value
        new_member.set_username("new-user")
        self.assertEqual("new-user",new_member.get_username())

    # Delete the object
    def test_delete(self):
        new_member = self.create_member()

        # make sure the new object exists
        self.assertEqual(Member.objects.count(),1)
        
        # delete the object
        name = new_member.get_username()
        Member.objects.filter(username=name).delete()
        
        # since we delete the object, there should be no member in the table.
        self.assertEqual(Member.objects.count(),0)