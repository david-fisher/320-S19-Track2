from django.test import TestCase
from database.models import Member
# Create your tests here.

class DataTestCase(TestCase): 

    # Test creating an member object
    def create_member(self,title="df"):
        return Member.objects.create(visibility=True,
                                    email="email@email.com",
                                    password="pwd",
                                    username="test-user",
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")

    def test_create(self):
        new_member = self.create_member()
        self.assertTrue(isinstance(new_member, Member))
        # since we created a new member, the number should increase to 1
        self.assertEqual(Member.objects.count(),1)

    # Get the object
    def test_get(self):
        new_member = self.create_member()
        # # get the username
        username = new_member.data()['username']
        # make sure I get the expected value 
        self.assertEqual("test-user",username)
    
    # Edit the object
    def test_edit(self):
        new_member = self.create_member()
        # update the value
        new_member.set_username("new-user")
        # get new username
        new_name = new_member.data()['username']
        self.assertEqual("new-user",new_name)

    # Delete the object
    def test_delete(self):
        new_member = self.create_member()

        # make sure the new object exists
        self.assertEqual(Member.objects.count(),1)
        
        # delete the object by id
        id = new_member.data()['id']
        Member.objects.filter(id=id).delete()
        
        # since we delete the object, there should be no member in the table.
        self.assertEqual(Member.objects.count(),0)