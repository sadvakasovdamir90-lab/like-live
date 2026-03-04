from TikTokLive import TikTokLiveClient
from TikTokLive.events import LikeEvent
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Өз никнейміңді жаз
TIKTOK_USERNAME = "@dam1r_sadu" 

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    # Лайк басқан адамның аты мен саны
    data = {
        'username': event.user.nickname,
        'amount': event.like_count,
        'total': event.total_likes
    }
    print(f"Liker: {data['username']} sends {data['amount']} likes")
    socketio.emit('new_like', data)

@app.route('/')
def index():
    return render_template('widget.html')

def run_tiktok():
    try:
        client.run()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    threading.Thread(target=run_tiktok, daemon=True).start()
    socketio.run(app, port=5000)
