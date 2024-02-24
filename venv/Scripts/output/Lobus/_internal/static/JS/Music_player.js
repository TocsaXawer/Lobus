function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainder = seconds % 60;
    const formattedRemainder = remainder < 10 ? `0${Math.floor(remainder)}` : Math.floor(remainder);
    return `${minutes}:${formattedRemainder}`;
}

function displayImage(imageUrl, imgId) {
    var thumbnail = document.getElementById(imgId);
    thumbnail.src = imageUrl;
}


// Hívjuk meg a playRestartOnEnd függvényt az audioPlayer ended eseményére.
// document.getElementById("audioPlayer").addEventListener("ended", playRestartOnEnd);

function play(musicList, selectedIndex) {
    console.log();
    if (selectedIndex < 0 || selectedIndex >= musicList.length) {
        console.error("Érvénytelen index kiválasztva.");
        return;
    }

    var selectedMusic = musicList[selectedIndex];
    var url = selectedMusic.file;
    var audioPlayer = document.getElementById("audioPlayer");
    var playButton = document.getElementById("playButton");
    var name = document.getElementById("music_name_player");
    var by = document.getElementById("music_by_player");
    var timeline = document.getElementById("timeline");
    var playhead = document.getElementById("playhead");
    var currentTime = document.getElementById("currentTime");
    var duration = document.getElementById("duration");
    var next = document.getElementById("next");
    var back = document.getElementById("back");

    if (!audioPlayer) {
        console.error("Az 'audioPlayer' elem nem található a DOM-ban.");
        return;
    }
    audioPlayer.onended = function() {
        selectedIndex++;
        if (selectedIndex >= musicList.length) { 
            selectedIndex = 0; 
        }
        play(musicList, selectedIndex);
      };
    
    back.addEventListener("click", function() {
        selectedIndex--;
        if (selectedIndex < 0){
            selectedIndex = (musicList.length-1);
        }
        play(musicList, selectedIndex);
    });
    next.addEventListener("click", function() {
        // Növeljük a selectedIndex értékét egyre.
        selectedIndex++;
    
        // Ellenőrizzük, hogy a selectedIndex nem lépte-e túl a zenék számát.
        if (selectedIndex >= musicList.length) {
            selectedIndex = 0; // Visszaugrik az első zenére.
        }
    
        // Hívjuk meg a play függvényt a frissített selectedIndex értékkel.
        play(musicList, selectedIndex);
    });

    fetch(url)
        .then(response => response.blob())
        .then(blob => {
            var blobUrl = URL.createObjectURL(blob);
            audioPlayer.src = blobUrl;
            name.textContent = selectedMusic.name;
            by.textContent = selectedMusic.auth;

            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.responseType = 'blob';

            xhr.onload = function() {
                if (this.status === 200) {
                    var blob = this.response;
                    displayImage(`/show_thombnail/${selectedMusic.id}`, 'song_img');
                }
            };

            xhr.send();

            if (audioPlayer.paused) {
                audioPlayer.play();
                playButton.className = "fa fa-pause";
            } else {
                audioPlayer.pause();
                playButton.className = "fa fa-play";
            }

            audioPlayer.addEventListener("timeupdate", function() {
                var playPercent = (audioPlayer.currentTime / audioPlayer.duration) * 100;
                playhead.style.width = playPercent + "%";
                currentTime.textContent = formatTime(audioPlayer.currentTime);
                duration.textContent = formatTime(audioPlayer.duration);
                });
            });

            timeline.addEventListener("click", function(event) {
                var timelineWidth = timeline.offsetWidth;
                var clickX = event.clientX - timeline.getBoundingClientRect().left;
                var newTime = (clickX / timelineWidth) * audioPlayer.duration;
                audioPlayer.currentTime = newTime;
            });
}

document.addEventListener("DOMContentLoaded", function() {
    var audioPlayer = document.getElementById("audioPlayer");
    var playButton = document.getElementById("playButton");
    var timeline = document.getElementById("timeline");
    var currentTime = document.getElementById("currentTime");

    playButton.addEventListener("click", function() {
        if (audioPlayer.src) {
            if (audioPlayer.paused) {
                audioPlayer.play();
                playButton.className = "fa fa-pause";
            } else {
                audioPlayer.pause();
                playButton.className = "fa fa-play";
            }
        }
    });

    timeline.addEventListener("click", function(event) {
        var timelineWidth = timeline.offsetWidth;
        var clickX = event.clientX - timeline.getBoundingClientRect().left;
        var newTime = (clickX / timelineWidth) * audioPlayer.duration;
        audioPlayer.currentTime = newTime;
    });
    
});

function setVolume(volume) {
    var audioPlayer = document.getElementById("audioPlayer");
    if (audioPlayer) {
        if (volume >= 0 && volume <= 1) {
            audioPlayer.volume = volume;
        }
    }
}
