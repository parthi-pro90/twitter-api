# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from sqlalchemy import String, JSON
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import app, db

Base = declarative_base()

def get_session(bind='new'):
    Session = sessionmaker(db.get_engine(bind=bind))
    return Session()

def close_session(session):
    session.close()

class AuditMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())    

class User(Base, AuditMixin):
    __bind_key__ = 'new'
    __tablename__ = 'user'
    __table_args__ = (
        db.UniqueConstraint('user_id'),
      )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)


class Timeline(Base, AuditMixin):
    __bind_key__ = 'new'
    __tablename__ = 'timeline'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author_id = db.Column(db.String(100), nullable=False)
    conversation_id = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    reply_settings = db.Column(db.String(255), nullable=False)
    text=db.Column(db.Text(4294000000), nullable=False)
    timeline_at=db.Column(db.DateTime(timezone=True), nullable=False) 
    json = db.Column(JSON, nullable=False)

class Sync(Base, AuditMixin):
    __bind_key__ = 'new'
    __tablename__ = 'sync'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_sync_at=db.Column(db.DateTime(timezone=True), nullable=False)     

        