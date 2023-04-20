from flask import Flask, session, g
import config
from extends import mongo, mail
from models import *
from module.qa import qa_bp
from module.authority import au_bp

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
        user = User.objects(email=user_email).first()
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def context():
    return {"user": g.user}


if __name__ == '__main__':
    app.run()
