import models
from models.video import Base, Video
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DB:
    """The DB"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate the db"""
        self.__engine = create_engine("sqlite:///videos.db")
    
    def load(self):
        """Loads the db to a session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def save(self):
        """Saves all objects in session to db"""
        self.__session.commit()

    def new(self, obj):
        """Creates a new instance of the object"""
        self.__session.add(obj)
        self.save()

    def get(self, id):
        """Returns the video object with the given id"""
        return self.__session.query(Video).filter_by(id=id).first()

    def all(self):
        """Returns all recordings in db"""
        return self.__session.query(Video).all()

    def delete(self, obj):
        """Deletes the instance from db"""
        self.__session.delete(obj)
        self.save()