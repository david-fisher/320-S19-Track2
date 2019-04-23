import unittest
#

def test_comment_was_changed(id, edit):
    original = get_comment(id)
    # assuming this is a void
    set_comment(id,edit)
    modified = get_comment(id)
    assertNotEqual(modified,original,'Comment was Changed')
def test_calls(id, edit):
    # setter for comment
    set_comment(id,edit)
    # getter to test
    assertEqual(get_comment(id),edit,'Getters/Setters Work')

def cmp_edit(id):
    get_comment(id)
    get_edited_comment(id)

# dummy functions
def get_comment(x):
    return 0
def set_comment(id,edit):
    return 0
def get_edited_comment(id)