from crypt import methods
from flask import Flask, render_template, session, request, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
from decouple import config
from boggle import Boggle


app = Flask(__name__)
app.config["SECRET_KEY"] = config("SECRET_KEY")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/", methods=["GET", "POST"])
def show_homepage():
    if request.method == "GET":
        return render_template("home.html")
    else:
        row = int(request.form["row"])
        boggle_game = Boggle(row)
        board = boggle_game.make_board()
        session["row"] = row
        session["board"] = board
        if not session.get("highest_score"):
            session["highest_score"] = 0
        return render_template("board.html")


@app.route("/check")
def check_word():
    guess = request.args["word"]
    result = Boggle(session["row"]).check_valid_word(session["board"], guess)
    info = jsonify({"result": result})
    return info


@app.route("/score", methods=["POST"])
def get_score():
    score = request.form["score"]
    if int(score) > int(session["highest_score"]):
        session["highest_score"] = int(score)
    return redirect("/")
