
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

Base.metadata.create_all(engine)
