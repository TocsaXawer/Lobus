function openModal() {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("modal").style.display = "block";
}

function closeModal() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("modal").style.display = "none";
}

function add_playlist_open(){
    document.getElementById("exit_playlist").style.display = "block";
    document.getElementById("add_playlist_modul").style.display = "block";
}

function add_playlist_close(){
    document.getElementById("exit_playlist").style.display = "none";
    document.getElementById("add_playlist_modul").style.display = "none";
}




function watch_playlist(name, Leiras, datum, id) {
    console.log(name, Leiras, datum, id);
    document.getElementById("exit_watch_playlist").style.display = "block";
    document.getElementById("watch_playlist").style.display = "block";
    document.getElementById("watch_container").innerHTML = '<h1 class="Title">' + name + '</h1><p class="descript_pl">' + Leiras + '</p><p class="datum">' + datum + '</p><a class="d_p_d" href="/remove_playlist/' + id + '">delete</a><div class="buton_container"><div id="Play_pl" class="play_pl"></div></div><hr><table id="zenes_music">';
    fetch('/music_in_playlist/' + id + '')
        .then(response => response.text())
        .then(data => {
            var songs_d = JSON.parse(data);
            const a = []

            for (let i = 0; i < songs_d.length; i++) {
                (function (i) {
                    fetch('/play/' + songs_d[i])
                        .then(response => response.text())
                        .then(file => {
                            var file_d = JSON.parse(file);
                            document.getElementById("zenes_music").innerHTML += `<tr><td><p>${file_d[0]} ${file_d[1]} <a class="d_p_s_i" href="/remove/${id}/${songs_d[i]}">(Delete)</a></p></td><td class="button_container"><button onclick="play([{id:\'${songs_d[i]}\', name:\'${file_d[0]}\', auth:\'${file_d[1]}\', file:\'${file_d[2]}\'}], 0)"><i class="fa fa-play"></i></button></td><td class="button_container"></td></tr>`;
                            a.push({id:`${songs_d[i]}` ,name:`${file_d[0]}`, auth:`${file_d[1]}`, file:`${file_d[2]}`});
        
                        })
                        .catch(error => {
                            console.log(name, Leiras, datum, id);
                            console.error('hiba:', error);
                        });
                })(i);
            }
            var elem = a;
            document.getElementById("Play_pl").innerHTML = '<button id="playP"><i class="fa fa-play" style="color: #ffffff;"></i></button>';
            document.getElementById("playP").addEventListener('click', function() {
                play(elem, 0);
            });
             // A tömb tartalma helyesen jelenik meg
        })
        .catch(error => {
            console.error('Hiba történt anyádba:', error);
        });

}




function close_playlist(){
    document.getElementById("exit_watch_playlist").style.display = "none";
    document.getElementById("watch_playlist").style.display = "none";
}

function merge(id, play_id){
    alert(`Zene ID:${id}, Playlist_ID:${play_id}`)
}

function parseData(dataString) {
    // Töröljük az idézőjeleket és a datetime.date részeket
    var cleanedData = dataString.replace(/\('([^']+)','([^']+)','([^']+)', datetime.date\(([^,]+), ([^,]+), ([^)]+)\)\)/g, '["$1", "$2", "$3", "$4-$5-$6"]');

    // JSON-parszoljuk az adatot
    var dataList = JSON.parse("[" + cleanedData + "]");

    return dataList;
}

// function watch(data){
//     console.log(data);
// }

let playlist_data = [];

function add_to_playlist(id, playlist_o){
    document.getElementById("exit_song_to_playlist").style.display = "block";
    document.getElementById("add_playlist_to_song_modul").style.display = "block";
    playlist_data.push('' + id + '');
    console.log(typeof playlist_o);
    const playlist = JSON.parse(playlist_o);
    for(var i = 0; i < playlist.length; i++){
        console.log(playlist[i].Name, id);
        document.getElementById("list_item").innerHTML +=  '<tr><td><a href="/music_add_to_pl/' + `${playlist[i].ID}` + '/' + `${id}` + '">' + playlist[i].Name + '</a><td><tr>';
    }
}




function give_delet_alert(event,elem){
    var notic = document.getElementById("Alert");
    notic.innerHTML='<span class="closebtn" onclick="'+notic+'.parentElement.style.display="none";">&times;</span> <strong>'+`${event}`+'</strong> '+`${elem}`;
}


function add_song_to_playlist_close(){
    document.getElementById("exit_song_to_playlist").style.display = "none";
    document.getElementById("add_playlist_to_song_modul").style.display = "none";
}

function watch(dat){
    console.log(dat)
}

function op_pl(pl){
    document.getElementById("op_pl").style.display = "block";
    document.getElementById("exit_pl").style.display = "block";
    alert(`${pl}`);
}

function cl_pl(){
    document.getElementById("exit_pl").style.display = "none";
    document.getElementById("op_pl").style.display = "none";
}