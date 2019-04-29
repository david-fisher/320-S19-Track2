import unittest
import classes_unintegrated.comment_edit as CommentEdit
import classes_unintegrated.adapter as DBAdapter

class TestEditComment(unittest.TestCase):


    def test_comment_was_changed(self, id, edit):
        original = get_comment(id)
        # assuming this is a void
        CommentEdit.edit_comment(id,edit)
        modified = get_comment(id)
        self.assertNotEqual(modified,original,'Comment was Changed')

    def test_calls(self, id, edit):
        # setter for comment
        DBAdapter.set_comment(id,edit)
        # getter to test
        self.assertEqual(get_comment(id),edit,'Getters/Setters Work')

    def cmp_edit(self, id):
        DBAdapter.get_comment(id)
        DBAdapter.get_edited_comment(id)
        self.assertNotEqual(get_comment,get_edited_comment,'Compare edited comment with original')

# dummy functions
def get_comment(x):
    return 0
def set_comment(id,edit):
    return 0
def get_edited_comment(id):
    return 0