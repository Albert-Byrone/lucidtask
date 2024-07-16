from fastapi import Response, APIRouter, status, Depends
from sqlalchemy.orm import Session
from backend.api.authentication.constants import INVALID_AUTHENTICATION_MESSAGE
from .responses import CreatePostResponse, GetPostResponse
from .schemas import CreatePost, UpdatePost
from .models import Post
from .crud import create_post_crud, get_posts_crud, update_post_crud, delete_post_crud
from .constants import CREATED_POST_SUCCESSFUL_MESSAGE, GET_POST_SUCCESSFUL_MESSAGE, POST_NOT_FOUND_MESSAGE, \
    UPDATE_POST_SUCCESSFUL_MESSAGE, POSTS_NOT_FOUND_MESSAGE, POST_DELETED_SUCCESSFUL_MESSAGE
from backend.api.authentication.helpers import verify_access_token
from backend.api.utils import get_token, get_db

router = APIRouter()
get = router.get
post = router.post
patch = router.patch
delete = router.delete
put = router.put



@post('/posts', response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(posts: CreatePost, response: Response, jwt_token: str = Depends(get_token()),
                      db: Session = Depends(get_db)):
    post_response = CreatePostResponse()
    user = verify_access_token(db, jwt_token)

    if user is None:
        post_response.message = INVALID_AUTHENTICATION_MESSAGE
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return post_response

    created_post = create_post_crud(db, posts)
    if created_post:
        post_response.success = True
        post_response.data.post = created_post
        post_response.message = CREATED_POST_SUCCESSFUL_MESSAGE
        return post_response


@get('/posts', status_code=status.HTTP_200_OK, response_model=GetPostResponse)
async def get_posts(response: Response, jwt_token: str = Depends(get_token()), db: Session = Depends(get_db)):
    posts_response = GetPostResponse()
    user = verify_access_token(db, jwt_token)
    if user is None:
        posts_response.message = INVALID_AUTHENTICATION_MESSAGE
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return posts_response
    posts = get_posts_crud(db)
    posts_response.success = True
    posts_response.data.posts = posts
    posts_response.message = GET_POST_SUCCESSFUL_MESSAGE
    return posts_response

@patch('/post/{post_id}', response_model=CreatePostResponse, status_code=status.HTTP_200_OK)
async def update_post(post_id: int, posts: UpdatePost, response: Response, jwt_token: str = Depends(get_token()),
                      db: Session = Depends(get_db)):
    post_response = CreatePostResponse()
    user = verify_access_token(db, jwt_token)
    post_instance = db.query(Post).filter(Post.id == post_id).first()

    if user is None:
        post_response.message = INVALID_AUTHENTICATION_MESSAGE
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return post_response

    if post_instance is None:
        post_response.message = POST_NOT_FOUND_MESSAGE
        response.status_code = status.HTTP_404_NOT_FOUND
        return post_response

    updated_post = update_post_crud(db, posts, post_id)
    if updated_post:
        post_response.message = UPDATE_POST_SUCCESSFUL_MESSAGE
        post_response.data.post = updated_post
        post_response.success = True
        return post_response



@delete('/post/{post_id}', response_model=CreatePostResponse, status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, response: Response, jwt_token: str = Depends(get_token()),
                      db: Session = Depends(get_db)):
    """
    Endpoint to permanently delete posts from the database.
    """
    user = verify_access_token(db, jwt_token)
    post_response = CreatePostResponse()
    if user is None:
        post_response.message = INVALID_AUTHENTICATION_MESSAGE
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return

    task_instance = db.query(Post).filter(Post.id == post_id).first()
    if task_instance is None:
        post_response.message = POSTS_NOT_FOUND_MESSAGE
        response.status_code = status.HTTP_404_NOT_FOUND
        return post_response
    deleted_task = delete_post_crud(db, task_instance)
    if deleted_task:
        post_response.message = POST_DELETED_SUCCESSFUL_MESSAGE
        post_response.success = True
        return post_response
