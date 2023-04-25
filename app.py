from flask import Flask, session, g
import config
from extends import mongo, mail
from models import *
from module.qa import qa_bp
from module.authority import au_bp
from functions import header_getter,collection_creator, password_getter
import requests

app = Flask(__name__)

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
    else:
        setattr(g, "user", None)


@app.context_processor
def context():
    return {"user": g.user}


if __name__ == '__main__':

    #stage 1 with port 5000, stage 2 with port 5066
    app.run(port = 5066)

    #create 3 collections
    headers = header_getter()
    collection_creator("User",headers)
    collection_creator("Email",headers)
    collection_creator("Publish",headers)
    collection_creator("Order", headers)

    #set order index
    indexUrl = "http://127.0.0.1:5000/" + ".create_index/" + "Order/3/" + "create_time"
    requests.post(indexUrl, headers=headers)




