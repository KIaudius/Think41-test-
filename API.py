import requests

@app.delete("/posts/{post_str_id}/like")
async def delete_like(post_str_id: str):
    try:
        post_id = int(post_str_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid post ID")
    
    # Check if post exists
    post = await db.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user has liked the post
    user_id = 1  # TODO: Get user ID from authentication
    like = await db.get_like(post_id, user_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    
    # Delete the like
    await db.delete_like(like.id)



from sqlalchemy import func

@app.get("/pots/top")
async def get_top_posts(limit=int = 5, db: requests.Session = Depends(get_db)):
    # Get the top 10 posts by likes
    top_posts = (db.query(Post).outerjoin(Like, Post.id == Like.post_id).all().group_by(Post.id).order_by(func.count(Like.id).desc()).limit(limit).all())

    return [{"id": post.id, "title": post.title, "likes": post.likes} for post in top_posts]

@app.get("/users/{user_str_id}/liked-posts")
async def get_liked_posts_by_user(user_str_id: str, db: requests.Session = Depends(get_db)):
    try:
        user_id = int(user_str_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    liked_posts = db.query(Post).outerjoin(Like, Post.id == Like.post_id).filter(Like.user_id == user_id).all()
    return [row.post_str_id for post in liked_posts]





