from flask import Blueprint, request, render_template, g, redirect
from models import Publish
from decorators import login_required
from functions import question_saver,get_question,get_question_from_order

qa_bp = Blueprint("qa", __name__, url_prefix="/")


@qa_bp.route("/")
def index():
    #questions = Publish.objects().order_by("-create_time").all()
    #select from Order table order by create_time
    questions =get_question_from_order()
    return render_template("index.html", questions=questions)


@qa_bp.route("/publish", methods=["GET", "POST"])
@login_required
def publish():
    if request.method == "GET":
        return render_template("publish.html")
    else:
        title = request.form.get("title")
        content = request.form.get("content")
        #question = Publish(title=title, content=content, author=g.user.user)
        author=g.user
        question = question_saver(title,content, author)

        print(question)
        # print(question.to_json())
        # question.save()
        return redirect("/")


@qa_bp.route("/detail/<id>")
def detail(id):
    question = Publish.objects(id=id).first()
    answers = Answer.objects(publish_id=id).order_by("-create_time").all()
    return render_template("detail.html", question=question, answers=answers)


@qa_bp.route("/answer/<id>", methods=["POST"])
@login_required
def publish_answer():
    content = request.form.get("content")
    publish_id = request.form.get("publish_id")
    author = g.user
    answer = Answer(content=content, publish_id=publish_id, author=author)
    answer.save()
    return redirect("/detail/<id>", id=publish_id)


@qa_bp.route("/search")
def search():
    criteria = request.args.get("searchContent")
    print(criteria)
    # questions = Publish.objects(title=criteria).order_by("-create_time").all()
    questions = get_question(criteria)
    return render_template("index.html", questions=questions)
