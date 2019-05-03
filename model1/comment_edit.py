from members_only.models import Comment

class EditComment:

    def edit_comment(comment_id, edit):
        # Retrieve the original comment to be modified
        parent_comment = Comment.objects.get(id=comment_id)

        # Sets original_comment as a string of the content in the parent_comment
        original_comment = parent_comment.content

        # Creates a new string by appending the edit to the end of the original comment string
        new_comment = original_comment + edit

        # Creates a new Comment object with a parent_id value as well as the content to be stored
        edited_comment = Comment.objects.create(parent_id = parent_comment.id, content=new_comment)

        # Save the Comment Object to the DB
        edited_comment.save()


    """Currently unnecessary but if Front End decides that they want 
    the edits displayed as a list then we would use this method."""

    def parse_hashtags(hashtags):
        list_of_hashtags = []
        for word in hashtags.split():
            if word[0] == "#":
                list_of_hashtags.append(word)
        return list_of_hashtags
