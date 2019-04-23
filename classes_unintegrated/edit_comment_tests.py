import unittest

class TestEditComment(unittest.TestCase):


    def test_comment_was_changed(self, id, edit):
        original = get_comment(id)
        # assuming this is a void
        set_comment(id,edit)
        modified = get_comment(id)
        self.assertEqual(modified,original,'Comment was Changed')

    def test_calls(self, id, edit):
        # setter for comment
        set_comment(id,edit)
        # getter to test
        self.assertEqual(get_comment(id),edit,'Getters/Setters Work')

    def cmp_edit(id):
        get_comment(id)
        get_edited_comment(id)

# dummy functions
def get_comment(x):
    return 0
def set_comment(id,edit):
    return 0
def get_edited_comment(id):
    return 0