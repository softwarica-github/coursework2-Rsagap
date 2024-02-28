from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, join_room, leave_room, send
import random
import string

app = Flask(__name__)
app.secret_key = "your_secret_key"
socketio = SocketIO(app)

def random_username():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

@app.route('/')
def index():
    # Check if the username already exists in the session
    if 'username' not in session:
        session['username'] = random_username()
    return render_template('index.html', username=session['username'])

@socketio.on('message')
def handleMessage(msg):
    username = session.get('username', 'Anonymous')  # Get username from session, default to 'Anonymous'
    message = f"{username}: {msg}"  # Concatenate username and message
    print('Message:', message)
    send(message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
