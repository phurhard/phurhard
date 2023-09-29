from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
import os
from datetime import datetime

engine = create_engine('sqlite:///.videos.db')

app = Flask(__name__)

Base = declarative_base()

a = Path.home()
if (a / '.videos').is_dir():
    print('passing')
    pass

else:
    directory = os.makedirs(a / '.videos')
    print('created')


class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    filePath = Column(String)
    videoName = Column(String)
    
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def status():
    '''Status of the app'''
    return jsonify({"message": "Up and running"})

@app.route('/upload', methods=["POST"])
def vid_upload():
    '''Saves uploaded video to disk n returns it's path'''
    if 'image' not in request.files:#chamge it to video later
        return jsonify({"error": "No video file available in request"}), 400

    videos = request.files['image']
    if videos.filename == '':
        return jsonify({"error": "video file not found"}), 400

    try:
        videos.filename = f'Untitled_{datetime.now().isoformat()}'
        path = Path.home() / '.videos'  / videos.filename# get the path the video is saved to
        videos.save(path)
        video = Video(filePath=str(path), videoName=videos.filename)
        session.add(video)
        session.commit()
        return jsonify({"message": "successfull", "video Url": video.filePath})
    except Exception as e:
        return jsonify({"error": f"An error occured processing this video: {e}"})

@app.route('/all')
def all_videos():
    '''Returns the path of all videos'''
    videos = session.query(Video).all()
    vid = [{'name': video.videoName, 'path': video.filePath} for video in videos]
    return jsonify(vid)

if __name__ == "__main__":
    app.run(debug=True)
