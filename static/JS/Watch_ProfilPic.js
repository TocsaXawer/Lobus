function loadImageWithDataParam(dataParam) {
    var xhr = new XMLHttpRequest();
    var url = `/show_image/${dataParam}`; // Az URL-t az aktuális szerver elérési útjára állítsd be
  
    xhr.open('GET', url, true);
    xhr.responseType = 'blob';
  
    xhr.onload = function() {
      if (this.status === 200) {
        var blob = this.response;
        var url = URL.createObjectURL(blob);
  
        // Blob megjelenítése egy <img> elemként
        var image = document.getElementById('image');
        image.src = url;
      }
    };
  
    xhr.send();
  }