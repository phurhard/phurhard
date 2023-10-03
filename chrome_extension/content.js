console.log("I have been injected")

var recorder = null
function onAccessApproved(stream){
    recorder  = new MediaRecorder(stream);

    recorder.start();
    recorder.ondataavailable = function(event){
        console.log("Event.data has been sent to recordedBlob")


        let recordedBlob = event.data;
        console.log(recordedBlob)
        fetch('http://127.0.0.1:5000/',{
            // method: 'POST',
            // body: recordedBlob
        }).then(res => {
            if (res.ok){
                console.log(res)
            } else{
                console.error('error')
            }
        }).catch(error => {
            console.error('Fetch error:', error)
        })
        // let url = URL.createObjectURL(recordedBlob);


        // let a = document.createElement("a");

        // a.style.display = "none";
        // a.href = url;
        // a.download = "screen-recording.webm"

        // document.body.appendChild(a);
        // a.click();

        // document.body.removeChild(a);

        // URL.revokeObjectURL(url);

    }

    recorder.onstop = function(){
        console.log("Recording has been stopped")
        stream.getTracks().forEach(function(track){
            if(track.readyState === "live"){
                track.stop()
            }
        })
    }

    
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse)=>{
    if(message.action === "request_recording"){
        console.log("Requesting recording");
        fetch("http://127.0.0.1:5000/start")
            .then((res, body) => {
                console.log(res);
                console.log(body);
                // video_id = res.video.id
            })

        sendResponse(`processed: ${message.action}`);

        navigator.mediaDevices.getDisplayMedia({
            audio:true,
            video: {
                width:9999999999,
                height: 999999999
            }
        }).then((stream)=>{
            
            onAccessApproved(stream)
        })

    }

    if(message.action === "stop_recording"){
        console.log("Recording stopped")
        sendResponse(`processed: ${message.action}`);
        if(!recorder) return console.log("no recorder")

        recorder.stop();
    }
})
