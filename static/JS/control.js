console.log("succes install control.js")
var audioPlayer = document.getElementById("audioPlayer");
var currentTime = document.getElementById("currentTime");
var duration = document.getElementById("duration");
var timelineContainer = document.getElementById("timelineContainer");
var timeline = document.getElementById("timeline");
var playhead = document.getElementById("playhead");

var isPlaying = false;

var playButton = document.getElementById("playButton");
var stopButton = document.getElementById("stopButton");

playButton.addEventListener("click", function() {
    if (!isPlaying) {
        audioPlayer.play();
        isPlaying = true;
    } else {
        audioPlayer.pause();
        isPlaying = false;
    }
});

stopButton.addEventListener("click", function() {
    audioPlayer.pause();
    audioPlayer.currentTime = 0;
    isPlaying = false;
});

audioPlayer.addEventListener("timeupdate", function() {
    var currentTimeValue = formatTime(audioPlayer.currentTime);
    var durationValue = formatTime(audioPlayer.duration);
    currentTime.textContent = currentTimeValue;
    duration.textContent = durationValue;

    var playPercent = (audioPlayer.currentTime / audioPlayer.duration) * 100;
    playhead.style.width = playPercent + "%";
});

timelineContainer.addEventListener("click", function(event) {
    var timelineWidth = timeline.offsetWidth;
    var clickX = event.clientX - timeline.getBoundingClientRect().left;
    var newTime = (clickX / timelineWidth) * audioPlayer.duration;
    audioPlayer.currentTime = newTime;
});

function formatTime(seconds) {
    var minutes = Math.floor(seconds / 60);
    var remainder = Math.floor(seconds % 60);
    if (remainder < 10) {
        remainder = "0" + remainder;
    }
    return minutes + ":" + remainder;
}

