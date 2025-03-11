from flask import Flask, render_template, jsonify
from supabase import create_client, Client
from flask_cors import CORS  
app = Flask(__name__)

CORS(app)

@app.route('/')
def hello():
    return 'Hello, world'


SUPABASE_URL = "https://jmhbbmjqaercspxtxfrd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImptaGJibWpxYWVyY3NweHR4ZnJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEyNDE3NzYsImV4cCI6MjA1NjgxNzc3Nn0.2psBAdjTc98V-eaTqW7Ol7T1_wqGMvvcrBuivZ1uNn0"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def clean_chord(chord):
    """
    Membersihkan teks chord dengan mengganti \r\n dengan <br> atau spasi.
    """
    if chord:

        chord = chord.replace("\r\n", "<br>")

    return chord


@app.route('/kategori')
def index():
    
    kategori_response = supabase.table("kategori").select("*").execute()
    kategori = kategori_response.data

    return jsonify({
        "kategori": kategori,
    })

@app.route('/kategori/<int:kategori_id>')
def get_artists_by_kategori(kategori_id):
    artists_response = supabase.table("artists").select("*").eq("kategori_id", kategori_id).execute()
    artists = artists_response.data
    return jsonify({
        "artists": artists,
    })


@app.route('/kategori/<int:kategori_id>/artist/<int:artist_id>')
def get_songs_by_artist(kategori_id, artist_id):
    
    songs_response = supabase.table("songs").select("*").eq("artist_id", artist_id).execute()
    songs = songs_response.data

   
    return jsonify({
        "songs": songs,
    })


@app.route('/chord/<int:song_id>')
def get_song_chord(song_id):
    song_response = supabase.table("songs").select("title, chord").eq("id", song_id).execute()
    
    if song_response.data:
        judul_lagu = song_response.data[0]["title"]
        chord = song_response.data[0]["chord"]
        chord = clean_chord(chord)
        return jsonify({
            "judul_lagu": judul_lagu,
            "chord": chord
        })
    else:
        return jsonify({
            "error": "Lagu tidak ditemukan"
        }), 404

# Export Flask app untuk Vercel
def handler(request):
    return app(request)