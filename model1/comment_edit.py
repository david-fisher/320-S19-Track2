from members_only.models import Comment

class EditComment:

    def edit_comment(comment_id, edit):
        parent_comment = Comment.objects.get(id=comment_id)
        original_comment = parent_comment.content
        new_comment = original_comment + edit
        Comment.objects.create(parent_id = parent_comment.id, content=new_comment)

    def parse_hashtags(hashtags):
        list_of_hashtags = []
        for word in hashtags.split():
            if word[0] == "#":
                list_of_hashtags.append(word)
        return list_of_hashtags
