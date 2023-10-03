from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import models

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

    def save(self):
        """saves it's current state"""
        models.storage.save()

    def delete(self):
        """Deletes self from db"""
        models.storage.delete(self)
