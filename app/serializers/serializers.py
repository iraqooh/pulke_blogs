def serialize_post(post):
    return {
        'id': post.id,
        'title': post.title,
        'slug': post.slug,
        'content': post.content,
        'likes': len(post.likes),
        # ... 
    }


def serialize_comment(comment):
    return {
        'id': comment.id,
        'post_id': comment.post_id,
        'content': comment.content,
        'likes': len(comment.likes),
        # ... 
    }