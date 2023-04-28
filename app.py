from flask import Flask, session, g
import config
from extends import mongo, mail
from models import *
from module.qa import qa_bp
from module.authority import au_bp
from functions import header_getter,collection_creator, password_getter
from flask_socketio import SocketIO
import socketio as sio
import threading
import eventlet
import requests

eventlet.monkey_patch()
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

def on_event_received(data):
    print(f"Received event: {data}")
    if data['operationType'] == "update":
        print(data)
        update = data['updateDescription']['updatedFields']
        question = {"id":list(update.keys())[0].split('.')[0], "content":list(update.values())[0]}
        socketio.emit('question content', question)

def run_client_socketIO():
    client_socketIO = sio.Client()

    @client_socketIO.event
    def connect():
        print("Connected to Flask App 1")

    @client_socketIO.on('change_detected')
    def on_my_event(data):
        on_event_received(data)

    client_socketIO.connect('http://localhost:5000')
    client_socketIO.wait()

app.config.from_object(config)

mongo.init_app(app)
mail.init_app(app)

app.register_blueprint(au_bp)
app.register_blueprint(qa_bp)


@app.before_request
def before():
    user_email = session.get("user_email")
    if user_email:
       # user = User.objects(email=user_email).first()
        setattr(g, "user", user_email)
        print("g.user look up ---------------------------")
        print(g.user)
    else:
        setattr(g, "user", None)


@app.context_processor
def context():
    return {"user": g.user}


if __name__ == '__main__':

    #stage 1 with port 5000, stage 2 with port 5066
    # app.run(port = 5066)
    client_socketIO_thread = threading.Thread(target=run_client_socketIO, daemon=True)
    client_socketIO_thread.start()

    #create 3 collections
    headers = header_getter()
    collection_creator("User",headers)
    collection_creator("Email",headers)
    collection_creator("Publish",headers)
    collection_creator("Order", headers)

    #set order index
    indexUrl = "http://127.0.0.1:5000/" + ".create_index/" + "Order/3/" + "create_time"
    requests.post(indexUrl, headers=headers)

    #create listener
    postUrl = "http://127.0.0.1:5000/.create_listener/Order"
    requests.post(postUrl, headers=headers)

    socketio.run(app, port=5066, debug=True)

    



