import models
from models.video import Video
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class DB:
    """The DB"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate the db"""
        self.__engine = create_engine("sqlite:///videos.db")
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()