from flask import Blueprint, render_template, request, jsonify, redirect, session
from extends import mail
from flask_mail import Message
import random
from models import Email, User

au_bp = Blueprint("authority", __name__, url_prefix="/authority")

@au_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password =  request.form.get("password")
        user = User.objects(email=email).first()
        if user:
           if user.password == password:
               session["user_email"] = user.email
               return redirect("/")
           else:
               return redirect("/authority/login")
        else:
            return redirect("/authority/login")

@au_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")

@au_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        email = request.form.get("email")
        if not (User.objects(email=email).first()):
            password = request.form.get("password")
            password_confirm = request.form.get("password_confirm")
            if password_confirm == password:
                user = request.form.get("user")
                user = User(user=user,password=password,email=email)
                code = request.form.get("code")
                email_in_db = Email.objects(email=email,code=code).first()
                if email_in_db:
                    user.save()
                    email_in_db.delete()
                else:
                    return redirect("/authority/register")

                return redirect("/authority/login")
            else:
                return redirect("/authority/register")
        else:
            return redirect("/authority/register")



@au_bp.route("/validation_code")
def code():
    email = request.args.get("email")
    digits = "0123456789"
    ascii_lower = "abcdefghijklmnopqrstuvwxyz"
    ascii_upper = ascii_lower.upper()
    code = []
    for i in range(6):
        number = random.randint(0, 25)
        if number % 3 == 0:
            code.append(digits[number % 10])
        elif number % 3 == 1:
            code.append(ascii_lower[number])
        else:
            code.append(ascii_upper[number])
    code = "".join(code)
    message = Message(subject="DSCI551 forum validation code", recipients=[email],
                      body=f"your validation code is {code}")
    mail.send(message)
    email = Email(email=email, code=code)
    email.save()
    return jsonify({"code": 200, "message": "", "date": None})
