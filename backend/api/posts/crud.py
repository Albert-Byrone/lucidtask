from backend.api.posts.schemas import CreatePost
from sqlalchemy.orm import Session
from .models import Post
from .schemas import GetPost


def create_post_crud(db: Session, post: CreatePost):
    if len(post.text) > 1048576:  # 1 MB in bytes
        raise HTTPException(status_code=400, detail="Text payload size exceeds")

    post_instance = Post(text=post.text)
    db.add(post_instance)
    db.commit()
    db.refresh(post_instance)
    return GetPost(id=post_instance.id, text=post_instance.text)


def get_posts_crud(db: Session):
    posts = db.query(Post).all()
    return [GetPost(id=post_instance.id, text=post_instance.text) for post in posts]
