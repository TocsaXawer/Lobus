from flask import Flask, render_template, url_for, jsonify, request, redirect, session, Response, make_response
from flaskwebgui import FlaskUI
from db_int import db_int
from youtubesearchpython.__future__ import VideosSearch
import requests
from pytube import YouTube
from db_init_music import db_music
from io import BytesIO 
import uuid
import json



app = Flask(__name__)
app.secret_key = 'ndjfbsdőafö8328qwnid21beodbwqőfiq' 

def url_to_binary(url):
    response = requests.get(url)
    binary_data = response.content
    return binary_data

async def search_youtube(query, limit=2):
    videosSearch = VideosSearch(query, limit=limit)
    return await videosSearch.next()

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        user = request.form['usr']
        password = request.form['pass']
        data = server.belepes(usr=user, pas=password)
        if data != "No db":
            session['data'] = data
            return redirect(url_for('control'))
        else:
            return redirect(url_for('no_server'))
    else:
        try:
            return render_template("home.html")
        except Exception as e:
            return f"Error: {str(e)}"  # Hibaüzenet az esetleges hibákra
            
    

@app.route('/Logout')
def logout():
    session.pop('data', None)
    return redirect(url_for('home'))

@app.route('/no_server')
def no_server():
    return render_template('no_server.html')


    
@app.route('/control', methods=['POST', 'GET'])
def control():
    data = session.get('data')
    if data == 'HFP':
        return 'Fuck your self'
    elif data == 'NOF':
        return 'you are not user in server'
    elif data[2] == 'Admin':
        user = server.get_user()
        if request.method == 'GET':
            if 'query' in request.args:
                query = request.args.get('query')
                youtube_results = search_youtube(query)
                database_results = music.search_database(query)
                
                return render_template("control_admin.html", data=data, user=user, youtube_results=youtube_results, database_results=database_results)
        return render_template("control_admin.html", data=data, user=user, len=len(user))
    else:
        musics = music.get_music()
        playlists = music.get_playlist_name(data[3])
        k_p = playlists
        j_playlist = []

        for item in k_p:
            j_playlist.append(item)  # Az új módosítot
        j_playlist = json.dumps(j_playlist)
        return render_template("Main/Page.html", data=data, musics=musics, playlists=playlists, j_playlist=j_playlist)
    
@app.route("/<id>/remove_song", methods=['GET', 'POST'])
def delete_music(id):
    music.remove_by_ID(id)
    return redirect(url_for('control'))
    
@app.route("/<id>/remove", methods=['GET', 'POST'])
def delete(id):
    server.delete_user(id=int(id))
    return redirect(url_for('control'))

@app.route("/edit/<id>", methods=['GET', 'POST'])
def edit(id):
    u_data = server.get_user_by_id(id=id)
    data_line = []
    if request.method == "POST":
        username = request.form['change_username']
        password = request.form['change_pass']
        rang = request.form['change_rank']
        
        if password != "":
            password = server.encrypt_string(password=password)
        
        data_line.append((id, username, password, rang))
        server.checker(data_line=data_line)
        return redirect(url_for('control'))
    else: 
        return render_template('edit.html', id=id, data=u_data)

@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
    data = session.get('data')
    if request.method == 'POST':
        image = request.files['image']
        if image.filename != '':
            image_data = image.read()
            server.update_profil_pic(pic=image_data, id=id)
            if data[2] != 'Admin': 
                return redirect(url_for('Profil'))
            else: 
                return redirect(url_for('edit', id=id))
    else:
        return redirect(url_for('Profil'))


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        id = request.form['add_id']
        usr = request.form['user_add']
        passw = request.form['passw_add']
        rank = request.form['add_rank']
        jelszo = server.encrypt_string(passw)
        server.add_user(id, usr, jelszo, '', rank)
        return redirect(url_for('control'))
    else:
        return redirect(url_for('control'))

@app.route('/add_music', methods=['POST'])
def add_music():
    if request.method == 'POST':

        senditem = []

        id = str(uuid.uuid4())
        senditem.append(id)

        song_name = request.form['Song_Name']
        senditem.append(song_name)

        by = request.form['by']
        senditem.append(by)

        song = request.files['song_data']
        if song and song.filename != '':
            song_data = song.read()
            senditem.append(song_data)
        else:
            senditem.append(None) 

        image = request.files['images']
        if image and image.filename != '':
            image_data = image.read()
            senditem.append(image_data)
        else:
            senditem.append(None)
        music.set_music(senditem)
        return redirect(url_for('control'))
    else:
        return redirect(url_for('control'))
        
@app.route('/add_playlist', methods=['POST'])
def add_playlist():
    user = session.get('data')
    if request.method == 'POST':
        data = []
        playlist = request.form['Playlist_name']
        data.append(playlist)
        descript = request.form['Descript']
        data.append(descript)
        picture = request.files['playlist_img']
        if picture and picture.filename != '':
            picture_data = picture.read()
            data.append(picture_data)
            music.create_playlist(nev=data[0], leiras=data[1], borito_kepe=data[2], tulajdonos_id=user[3])

            return redirect(url_for('control'))
        else:
            music.create_playlist(nev=data[0], leiras=data[1], borito_kepe='none', tulajdonos_id=user[3])
            return redirect(url_for('control'))
        
@app.route('/remove_playlist/<id>')
def remove_playlists(id):
    music.remove_playlist(id=id)
    return redirect(url_for('control'))

@app.route('/show_image/<id>')
def show_image(id):
    image = server.show_image(id=id)
    return Response(image, mimetype='image/jpeg') 

@app.route("/show_thombnail/<id>")
def show_thombnail(id):
    image = music.show_thumbnail(id=id)
    return Response(image, mimetype='image/jpg')

@app.route("/Profil")
def Profil():
    data = session.get('data')
    return render_template('Main/Profil.html', data=data)

@app.route("/music/<id>")
def music_data(id):
    music_blob = music.get_music_data(id=id)
    if music_blob:
        return Response(music_blob, mimetype='audio/mp3')
    else:
        return "Nincs ilyen zene"
    
@app.route('/serc')
def search():
    data = session.get('data')
    return render_template('Main/search.html', data=data)

@app.route('/search', methods=['GET'])
async def do_search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Kérlek adj meg egy keresési kifejezést.'})

    youtube_results = await search_youtube(query)
    database_results = await music.search_database(query)

    response = {'videos': [], 'database_results': []}

    if youtube_results:
        video_list = []
        for video in youtube_results['result']:
            video_info = {
                'from': 'YouTube',
                'title': video['title'],
                'publishedTime': video['publishedTime'],
                'duration': video['duration'],
                'viewCount': video['viewCount']['text'],
                'thumbnails': video['thumbnails'],
                'link': f"http://www.youtube.com/watch?v={video['id']}"
            }
            video_list.append(video_info)

        for i in range(len(database_results)):
            video_info = {
                'id': database_results[i][0],
                'from': 'Local',
                'title': database_results[i][1],
                'auth': database_results[i][2],
                'publishedTime': 'none',
                'duration':'none',
                'viewCount': 'none',
                'thumbnails': 'none',
                'link':'none'
            }
            video_list.append(video_info)

        response['videos'] = video_list

    if database_results:
        response['database_results'] = database_results
    return jsonify(response)


@app.route('/down', methods=['POST'])
def down():
     song = []
     if request.method == "POST":
        try:
            id = str(uuid.uuid4())
            song.append(id)
            url = request.form['url']
            url = YouTube(url)
            song.append(url.title)
            song.append(url.author)
            video = url.streams.filter(only_audio=True).last()
            buffer = BytesIO()
            video.stream_to_buffer(buffer)
            buffer.seek(0)
            song.append(buffer.read())
            img = url_to_binary(url.thumbnail_url)
            song.append(img)
            music.set_music(song)
            return redirect((url_for('control')))
        except:
            return redirect((url_for('control')))

@app.route('/play/<music_id>')
def play_music(music_id):
    music_descript = music.get_music_descript(music_id)
    data =  [music_descript[0], music_descript[1],  f'/music/{music_id}' ]
    return data

@app.route('/music_add_to_pl/<p_id>/<s_id>')
def add_s_2_p(p_id, s_id):
    music.add_song_to_playlist(p_id, s_id)
    return redirect(url_for('control'))

@app.route('/music_in_playlist/<id>')
def music_in_playlist(id):
    musics = music.get_numbers_in_playlist(playlist_id=id)
    return musics

@app.route('/remove/<PID>/<SID>')
def remove_ittem_in_playlist(PID, SID):
    music.remove_song_in_playlist(PID=PID, SID=SID)
    return redirect(url_for('control'))

if __name__ == '__main__':
    db = ['localhost', 'root', 'password', 'mydatabase']
    server = db_int(host='localhost', user='root', password='password', db='mydatabase')
    music = db_music(db)
    #app.run(debug=True, port=8080, host='0.0.0.0')
    FlaskUI(app=app, server="flask").run()