from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
import os
import uuid
from flask_cors import CORS
from transcribe_openAI import run_transcription
from datetime import datetime
import subprocess

engine = create_engine('sqlite:///videos.db')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

Base = declarative_base()

a = Path.cwd()
if (a / 'xtensiovideos').is_dir():
    print('passing')
    pass

else:
    # if the directory does not exist, create it
    os.makedirs(a / 'xtensiovideos')
    print('created')


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

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# create a file to save the chunks 

uploadfolder = Path.cwd() / 'xtensiovideos'

@app.route('/')
def status():
    '''Status of the app'''
    return jsonify({"message": "Up and running"})

@app.route('/start')
def request_recording():
    '''This is the first step
        creates a blank mp4 file in storage
        assigns a name to it which is the current time
        assigns a uuid to it
        returns the uuid to the client for further streaming
        the transcript at this time is None

    '''
    vidID = str(uuid.uuid4())
    filename = f'{datetime.now().strftime("%d_%m_%yT%H_%M_%S")}.mp4'
    filepath = str(uploadfolder / filename)
    new_video = Video(id=vidID, videoName=filename, filePath=filepath, transcript='')
    session.add(new_video)
    session.commit()

    return jsonify({"Message": "This is the video details", "video": new_video.to_json()})


@app.route('/upload', methods=["POST"])
def start_recording():
    '''This is the second part
        Receives chunks of blob data from client
        Writes this data to the file that was created in part one above
        The filepath is gotten by using the videoID sent in the part one above
        Once all data has been written, returns a success message
    '''
    # video = session.query(Video).filter_by(id=vidID).first()
    # filepath = video.filePath
    vidID = str(uuid.uuid4())
    filename = f'{datetime.now().strftime("%d_%m_%yT%H_%M_%S")}.mp4'
    filepath = str(uploadfolder / filename)
    new_video = Video(id=vidID, videoName=filename, filePath=filepath, transcript='')
    session.add(new_video)
    session.commit()
    '''
    creates the videi path and then saves data to the path
    '''
    with open(str(filepath), 'ab') as videoFile:
         while True:
             chunks = request.stream.read(4096)
             if len(chunks) == 0:
                 break
             videoFile.write(chunks)
             # return jsonify({"message": "No data sent to server"}), 400
        # videoFile.write(chunks)
    return jsonify({"Message": "Blob data received and saved", "video": new_video.to_json()}), 200


@app.route('/done_recording/<vidID>')
def stop_recording(vidID):
    '''This is the third step
        Processes the video already gotten
        The file path is gotten which already contains the blob datas.
        Sub prpcess is used to transcribe it and the transcription is saved
        to video.transcript
    '''

    video = session.query(Video).filter_by(id=vidID).first()
    videoFile = video.filePath

    # use subprocess to convert the video file to audio
    transcript = subprocess(run_transcription(videoFile))
    
    # error handlers
    if len(transcript) == 0:
        return jsonify("Unable to transcribe video"), 500
    video.transcript = transcript
    # return the full video
    return jsonify({"Video": video.to_json()})

@app.route('/all')
def all_videos():
    '''Returns the path of all videos'''
    videos = session.query(Video).all()
    vid = [{'videos': video.to_json()} for video in videos]
    return jsonify(vid)


"""
@app.route('/upload', methods=["POST"])
def vid_upload():
    # Saves uploaded video to disk n returns it's path
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
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
