# How to use
This API has 5 endpoints

- /api: This endpoint is a status checker, to comfirm the server is running

- /api/all: This endpoints is used to get all the info of all the recordings in the database.
    each video object has the following attributes
    {"id": "This is the ID of the video object, its used for all other operations in the db",
    "filePath": "This is the path where the video is saved on the file storage, it is a path string calling this string calls the recording itself.",
    "videoName": "This is the name of the video on the database, it's set automatically to the time when the request ti record was made",
    "transcript": "This contains the transcript of the video, it is set to an empty string if the transceiption is not yet ready",
    }

- /api/start: This endpoint sends a request to the server, telling it to be ready for transmission of data. The server responds by returning credentials of a new video file, these credentails includes {id, videoName, filePath, transcript}. these information are used for subsequent requests.

- /api/upload/<vidID>: This endpoint accepts blob data sent in streams and writes it to the video file specified by the filePath. This filePath is gotten by querying the database based on the vidID sent in the request.
When all streams have been successful, it returms a message ```Blob data received and saved```

- /api/done_recording/<vidID>: This endpoint confirms that streams has stopped, amd proceeds to transcribe the data stored in the video file.
it returns the video object with its `id`, `filePath`, `videoName`, `transcript` if successfull, or an error message `Unable to transcribe video` if there is a server error
