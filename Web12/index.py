from flask import Flask, render_template, request, url_for, redirect, abort
import random

app = Flask(__name__)

movies_db = {
    1: {"title": "Інтерстеллар", "desc": "Подорож крізь час і простір."},
    2: {"title": "Початок", "desc": "Світ усвідомлених сновидінь."},
    3: {"title": "Дюна", "desc": "Боротьба за планету Арракіс."}
}

participants_list = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/countries")
def countries():
    places = ["Париж", "Кіото", "Барселона", "Балі", "Рим"]
    return render_template("countries.html", places=places)

@app.route("/movies")
def movies():
    return render_template("movies.html", movies=movies_db)

@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    movie = movies_db.get(movie_id)
    if not movie: abort(404)
    return render_template("movie_detail.html", movie=movie)

@app.route("/random")
def random_movie():
    movie_id = random.choice(list(movies_db.keys()))
    return redirect(url_for('movie_detail', movie_id=movie_id))

@app.route("/event_register", methods=["GET", "POST"])
def event_register():
    if request.method == "POST":
        name, email, time = request.form.get("name"), request.form.get("email"), request.form.get("time")
        if name and email and time:
            participants_list.append({"name": name, "email": email, "time": time})
            return redirect(url_for('participants'))
    return render_template("event_register.html")

@app.route("/participants")
def participants():
    return render_template("participants.html", participants=participants_list)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    message_sent = request.method == "POST"
    return render_template("contact.html", message_sent=message_sent)

if __name__ == "__main__":
    app.run(debug=True)
