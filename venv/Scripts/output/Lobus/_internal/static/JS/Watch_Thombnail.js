function downloadAndDisplayImage(url, imgId) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'blob';

    xhr.onload = function() {
        if (this.status === 200) {
            var blob = this.response;
            var url = URL.createObjectURL(blob);
            displayImage(url, imgId);
        }
    };

    xhr.send();
}

function displayImage(imageUrl, imgId) {
    var thumbnail = document.getElementById(imgId);
    thumbnail.src = imageUrl;
}

function downloadAndDisplayImagewithSearch(url, imgId) {
    fetch(url)  // Használj fetch-et az egyszerűség kedvéért
        .then(response => response.blob())
        .then(blob => {
            const imageUrl = URL.createObjectURL(blob);
            displayImage(imageUrl, imgId);
        })
        .catch(error => {
            console.error('Hiba a kép letöltésekor:', error);
        });
}