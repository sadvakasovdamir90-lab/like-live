from TikTokLive import TikTokLiveClient
from TikTokLive.events import LikeEvent
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Пайдаланушылардың лайктарын сақтайтын сөздік
user_likes = {}

TIKTOK_USERNAME = "@сенің_нигің" 

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

@client.on("like")
async def on_like(event: LikeEvent):
    user = event.user.nickname
    count = event.like_count # Бір басқандағы лайк саны
    
    if user not in user_likes:
        user_likes[user] = 0
    user_likes[user] += count

    # Топ 10 адамды сұрыптау
    top_10 = sorted(user_likes.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Виджетке жіберу
    socketio.emit('update_leaderboard', top_10)

@app.route('/')
def index():
    return render_template('widget.html')

def run_tiktok():
    client.run()

if __name__ == '__main__':
    threading.Thread(target=run_tiktok, daemon=True).start()
    socketio.run(app, port=5000)