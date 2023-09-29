document.addEventListener("DOMContentLoaded", ()=>{
    // GET SELECTORS OF THE UTO
    const startVideoBtn = document.querySelector("button#start_video")
    const stopVideoBtn = document.querySelector("button#stop_video")

    //adding event listeners
    startVideoBtn.addEventListener("click", ()=>{
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
            chrome.tabs.sendMessage(tabs[0].id, {action: "request_recording"}, function(response){
                if(!chrome.runtime.lastError){
                    console.log(response)
                } else{
                    console.log(chrome.runtime.lastError, "error line 13")
                }
            })
        })
    })

    stopVideoBtn.addEventListener("click", ()=>{
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
            chrome.tabs.sendMessage(tabs[0].id, {action: "stop_recording"}, function(response){
                if(!chrome.runtime.lastError){
                    console.log(response)
                } else{
                    console.log(chrome.runtime.lastError, "error line 26")
                }
            })
        })
    })
})