from django.test import TestCase
from database.models import Member
# Create your tests here.

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
  
    