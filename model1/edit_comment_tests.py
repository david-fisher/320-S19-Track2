import unittest

import model1.comment_edit as CommentEdit
from members_only.models import Comment


class TestEditComment(unittest.TestCase):


    def test_comment_was_changed(self, id, edit):
        original = get_comment(id)
        # assuming this is a void
        CommentEdit.edit_comment(id,edit)
        modified = get_comment(id)
        self.assertNotEqual(modified,original,'Comment was Changed')

    def test_calls(self, id, edit):
        # setter for comment
        set_comment(id,edit)
        # getter to test
        self.assertEqual(get_comment(id),edit,'Getters/Setters Work')

    def cmp_edit(self, original_id, edited_id):
        original_comment = Comment.objects.get(id=original_id).content
        edited_comment = Comment.objects.get(id=edited_id).content
        self.assertNotEqual(original_comment, edited_comment,'Compare edited comment with original')

# helper functions
def get_comment(comment_id):
    comment = Comment.objects.get(id=comment_id)
    return comment
def set_comment(comment_id,edit):
    Comment.objects.create(id=comment_id, content=edit)