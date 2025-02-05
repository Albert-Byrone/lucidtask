from sqlalchemy.orm import Session

from .helpers import get_password_hash
from .models import User, PasswordResetToken
from .schemas import UserCreate


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, username=user.username,
                   first_name=user.first_name, last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def change_password_crud(db: Session, user, new_password):
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return True


def create_reset_token_crud(db: Session, user):
    token = db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user.id).first()
    if token:
        return token
    token = PasswordResetToken(user_id=user.id)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def reset_password_crud(db: Session, user, new_password):
    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return True



