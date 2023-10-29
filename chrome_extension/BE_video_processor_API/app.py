from flask import Flask, jsonify, request
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
import os
import uuid
from flask_cors import CORS
from transcribe_openAI import run_transcription
from datetime import datetime
import subprocess
from models import storage
from models.video import Video


# engine = create_engine('sqlite:///videos.db')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Base = declarative_base()

a = Path.cwd()
if (a / 'xtensiovideos').is_dir():
    print('passing')
else:
    # if the directory does not exist, create it
    os.makedirs(a / 'xtensiovideos')
    print('created')


# class Video(Base):
#     __tablename__ = 'videos'

#     id = Column(String, primary_key=True)
#     filePath = Column(String)
#     videoName = Column(String)
#     transcript = Column(String, default=None)

#     def to_json(self):
#         return ({"id": self.id,
#                 "filepath": self.filePath,
#                 "videoName": self.videoName,
#                 "Transcript": self.transcript
#                 })

# Base.metadata.create_all(engine)

# Create a session to interact with the database
# Session = sessionmaker(bind=engine)
# session = Session()

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
    storage.new(new_video)
    storage.save()

    return jsonify({"Message": "This is the video details", "video": new_video.to_json()})


@app.route('/upload/<vidID>', methods=["POST"])
def start_recording(vidID):
    '''This is the second part
        Receives chunks of blob data from client
        Writes this data to the file that was created in part one above
        The filepath is gotten by using the videoID sent in the part one above
        Once all data has been written, returns a success message
    '''
    video = storage.get(vidID)
    filepath = video.filePath
    '''
    creates the video path and then saves data to the path
    '''
    with open(str(filepath), 'ab') as videoFile:
         while True:
             chunks = request.stream.read(4096)
             if len(chunks) == 0:
                 break
             videoFile.write(chunks)
    return jsonify({"Message": "Blob data received and saved", "video": video.to_json()}), 200


@app.route('/done_recording/<vidID>')
def stop_recording(vidID):
    '''This is the third step
        Processes the video already gotten
        The file path is gotten which already contains the blob datas.
        Sub prpcess is used to transcribe it and the transcription is saved
        to video.transcript
    '''

    video = storage.get(vidID)
    videoFile = video.filePath

    # use subprocess to convert the video file to audio
    transcript = run_transcription(videoFile)
    
    # error handlers
    if len(transcript) == 0:
        return jsonify("Unable to transcribe video"), 500
    video.transcript = transcript
    # return the full video details
    return jsonify({"Video": video.to_json()})

@app.route('/all')
def all_videos():
    '''Returns the path of all videos'''
    videos = storage.all()
    for vid in videos:
        print(f'{Path(vid.filePath)}')
        try:
            subprocess.run(vid.filePath)
            
        except Exception as e:
            print(f'Exception raised: {e}')
            storage.delete(vid)
            
    vid = [{'videos': video.to_json()} for video in videos]
    return jsonify(vid)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
