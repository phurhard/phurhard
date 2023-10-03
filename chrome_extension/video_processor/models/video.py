from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Video(Base):
    __tablename__ = 'videos'

    id = Column(String, primary_key=True)
    filePath = Column(String)
    videoName = Column(String)
    transcript = Column(String, default=None)

    def to_json(self):
        return ({"id": self.id,
                "filepath": self.filePath,
                "videoName": self.videoName,
                "Transcript": self.transcript
                })

engine = create_engine('sqlite:///videos.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
