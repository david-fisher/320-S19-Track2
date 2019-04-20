import classes_unintegrated.adapter as DBAdapter

class EditComment:

    def edit_comment(comment_id, edit):
        original_comment = DBAdapter.get_comment(comment_id)
        new_comment = original_comment + edit
        DBAdapter.store_comment(new_comment)

    def get_original_comment(comment_id):
        // TODO

    def get_edited_comment(comment_id):
        // TODO


