from flask import Flask, render_template, request, redirect, session, jsonify
from movies_data import movies
from chatbot import movie_assistant

app = Flask(__name__)
app.secret_key = "movie_chat_secret_key"


@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" or password == "":
            error = "Fill all fields"

        elif len(password) < 8:
            error = "Password must be at least 8 characters"

        else:
            session["username"] = username
            session["password"] = password

            if "favorites" not in session:
                session["favorites"] = []

            return redirect("/home")

    return render_template("login.html", error=error)


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/categories")
def categories():
    return render_template("categories.html", error="")


@app.route("/search", methods=["GET"])
def search_movie():
    search_name = request.args.get("search", "").strip()

    for movie in movies:
        if movie["title"].lower() == search_name.lower():
            return redirect("/movie/" + movie["title"])

    return render_template(
        "categories.html",
        error="Movie not found"
    )


@app.route("/category/<category_name>")
def category_page(category_name):

    category_movies = []

    for movie in movies:
        if movie["category"].lower() == category_name.lower():
            category_movies.append(movie.copy())

    max_views = max([movie["views"] for movie in category_movies], default=1)

    for movie in category_movies:
        movie["bar_height"] = int((movie["views"] / max_views) * 90)

    return render_template(
        "category_page.html",
        category_name=category_name,
        movies=category_movies,
        favorites=session.get("favorites", [])
    )


@app.route("/movie/<path:movie_title>")
def movie_page(movie_title):

    selected_movie = None

    for movie in movies:
        if movie["title"].strip().lower() == movie_title.strip().lower():
            selected_movie = movie.copy()
            break

    if selected_movie is None:
        return "Movie not found"

    return render_template(
        "movieDetails.html",
        movie=selected_movie
    )


@app.route("/toggle_favorite", methods=["POST"])
def toggle_favorite():

    movie_title = request.form.get("movie_title")
    category_name = request.form.get("category_name")

    favorites = session.get("favorites", [])

    if movie_title in favorites:
        favorites.remove(movie_title)
    else:
        favorites.append(movie_title)

    session["favorites"] = favorites
    session.modified = True

    return redirect("/category/" + category_name)


@app.route("/profile")
def profile():

    return render_template(
        "profile.html",
        username=session.get("username", "Guest"),
        password=session.get("password", ""),
        favorites=session.get("favorites", [])
    )


@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")


@app.route("/chatbot_reply", methods=["POST"])
def chatbot_reply():

    data = request.get_json(silent=True) or {}

    user_message = data.get("message", "").strip()

    session_favorites = session.get("favorites", [])

    bot_data = movie_assistant(
        user_message,
        session_favorites
    )

    return jsonify(bot_data)


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


print("STARTING FLASK APP...")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)