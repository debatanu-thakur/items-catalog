import sys
import datetime
import random
import string
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy import SmallInteger
from sqlalchemy.orm import relationship
from .base import Base
from itsdangerous import(
    TimedJSONWebSignatureSerializer as
    Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

secret_key = ''.join(random.choice(
    string.ascii_uppercase + string.digits) for x in range(32))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=True)
    email = Column(String(250), nullable=False, index=True)
    username = Column(String(250), nullable=False, index=True)
    password_hash = Column(String(64), nullable=True)
    image = Column(String(250), nullable=True)
    user_type = Column(SmallInteger, nullable=False, default=2)
    # user_type 1 - admin, 2 - normal user
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = Column(DateTime, nullable=True,
                          default=datetime.datetime.now,
                          onupdate=datetime.datetime.now)

    def has_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def is_admin(self):
        return True if self.user_type == 1 else False

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'createdAt': self.created_at,
            'lastUpdated': self.last_updated,
            'username': self.username,
            'email': self.email,
        }
