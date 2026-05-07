import random
from urllib.parse import quote
from movies_data import movies


class MovieAssistantChatbot:
    def __init__(self):
        self.movies = movies
        self.last_genre = None
        self.last_movie = None
        self.last_source = None
        self.awaiting_mood = False

        self.greetings = ["hi", "hello", "hey", "heyyy", "hello there", "hey there"]

        self.genre_aliases = {
            "Action": ["action", "fight", "adventure", "exciting"],
            "Comedy": ["comedy", "funny", "laugh"],
            "Drama": ["drama", "emotional", "deep", "serious"],
            "Sci-Fi": ["sci-fi", "sci fi", "science fiction", "scifi", "space", "future"],
            "Mystery": ["mystery", "thriller", "suspense", "detective", "dark"],
            "Family": ["family", "kids", "warm", "light", "sweet", "cozy"]
        }

        self.mood_map = {
            "Action": ["excited", "adrenaline", "fast", "intense"],
            "Comedy": ["happy", "fun", "funny", "laugh", "cheerful", "bored"],
            "Drama": ["sad", "emotional", "deep", "heartbroken", "serious"],
            "Sci-Fi": ["curious", "mind-blowing", "mind blowing", "future", "space", "science"],
            "Mystery": ["mysterious", "dark", "suspense", "thriller", "detective"],
            "Family": ["cozy", "soft", "warm", "cute", "relaxed", "family time"]
        }

        self.genre_emojis = {
            "Action": "🔥",
            "Comedy": "😂",
            "Drama": "🎭",
            "Sci-Fi": "🚀",
            "Mystery": "🕵️",
            "Family": "✨"
        }
    def decorate_text(self, text, intent=None, genre=None):
        if intent == "greeting":
            return f"{text} 🎬✨"
        if intent == "recommendation":
            return f"{text} {self.genre_emojis.get(genre, '🎬')}🍿"
        if intent == "top_rated":
            return f"{text} ⭐🏆"
        if intent == "poster":
            return f"{text} 🖼️✨"
        if intent == "exists":
            return f"{text} 🎞️✅"
        if intent == "favorites":
            return f"{text} ❤️🍿"
        if intent == "goodbye":
            return f"{text} 👋🍿"
        return text
        

    def build_response(
        self,
        text,
        suggestions=None,
        movie=None,
        intent=None,
        show_button=False,
        show_poster=False
    ):
        suggestions = suggestions or []
        if show_button:
           suggestions = [s for s in suggestions if s.lower() != "open movie page"]

        if movie:
            self.last_movie = movie
            self.last_genre = movie["category"]

        return {
            "reply": self.decorate_text(
                text,
                intent=intent,
                genre=movie["category"] if movie else None
            ),
            "suggestions": suggestions,
            "movie_title": movie["title"] if movie else None,
            "poster_url": movie["image"] if movie and show_poster else None,
            "button_label": "Open movie page" if movie and show_button else None,
            "button_url": f"/movie/{quote(movie['title'])}" if movie and show_button else None
        }

    def get_movie_by_title(self, title):
        for movie in self.movies:
            if movie["title"].strip().lower() == title.strip().lower():
                return movie
        return None

    def get_movies_by_genre(self, genre):
        return [movie for movie in self.movies if movie["category"].lower() == genre.lower()]

    def get_favorite_movie_objects(self, favorites):
        favorite_movies = []

        for title in favorites:
            movie = self.get_movie_by_title(title)
            if movie:
                favorite_movies.append(movie)

        return favorite_movies

    def favorite_titles_text(self, favorites):
        if not favorites:
            return "no favorites yet"

        if len(favorites) <= 3:
            return ", ".join(favorites)

        shown = ", ".join(favorites[:3])
        remaining = len(favorites) - 3
        return f"{shown} and {remaining} more"

    def find_movie_object(self, message):
        lower_message = message.lower()
        sorted_movies = sorted(self.movies, key=lambda m: len(m["title"]), reverse=True)

        for movie in sorted_movies:
            if movie["title"].lower() in lower_message:
                return movie
        return None

    def detect_genre(self, message):
        lower_message = message.lower()

        for genre, aliases in self.genre_aliases.items():
            for alias in aliases:
                if alias in lower_message:
                    return genre
        return None

    def detect_mood_genre(self, message):
        lower_message = message.lower()

        for genre, words in self.mood_map.items():
            for word in words:
                if word in lower_message:
                    return genre
        return None

    def recommend_movie(self, genre, exclude_title=None):
        genre_movies = self.get_movies_by_genre(genre)

        if exclude_title:
            genre_movies = [m for m in genre_movies if m["title"] != exclude_title]

        if not genre_movies:
            return None

        movie = random.choice(genre_movies)
        self.last_movie = movie
        self.last_genre = movie["category"]
        self.last_source = "genre"
        return movie

    def recommend_by_favorites(self, favorites, exclude_title=None):
        favorite_movies = self.get_favorite_movie_objects(favorites)

        if not favorite_movies:
            return None, [], None

        genre_count = {}
        for movie in favorite_movies:
            genre = movie["category"]
            genre_count[genre] = genre_count.get(genre, 0) + 1

        primary_genre = max(genre_count, key=genre_count.get)

        candidates = [
            movie for movie in self.get_movies_by_genre(primary_genre)
            if movie["title"] not in favorites
        ]

        if exclude_title:
            candidates = [movie for movie in candidates if movie["title"] != exclude_title]

        if not candidates:
            candidates = [
                movie for movie in self.movies
                if movie["title"] not in favorites and movie["title"] != exclude_title
            ]

        if not candidates:
            return None, favorite_movies, primary_genre

        movie = random.choice(candidates)
        self.last_movie = movie
        self.last_genre = movie["category"]
        self.last_source = "favorites"

        return movie, favorite_movies, primary_genre

    def get_top_rated_movie(self, genre=None):
        candidates = self.movies if genre is None else self.get_movies_by_genre(genre)

        if not candidates:
            return None

        movie = max(candidates, key=lambda m: float(m["rating"]))
        self.last_movie = movie
        self.last_genre = movie["category"]
        self.last_source = "top_rated"
        return movie

    def movie_details_text(self, movie):
        return (
            f"{movie['title']}\n"
            f"Category: {movie['category']}\n"
            f"Story: {movie['story']}\n"
            f"Rating: {movie['rating']}/10"
        )

    def welcome_message(self):
        return self.build_response(
            "Hi! I’m your Movie Assistant. I can help you find movies by mood, genre, favorites, or details.",
            [
                "recommend by mood",
                "recommend by favorites",
                "do you have Interstellar?"
            ],
            intent="greeting"
        )

    def help_message(self):
        return self.build_response(
            "I can recommend movies, tell you details, show posters, check if a movie exists, and recommend based on your favorites.",
            [
                "recommend by favorites",
                "show me the poster of Interstellar",
                "do you have John Wick?"
            ]
        )

    def fallback_message(self):
        return self.build_response(
            "I didn’t fully understand that. Try asking by mood, genre, favorites, movie title, or poster request.",
            [
                "recommend by favorites",
                "recommend mystery",
                "do you have Interstellar?"
            ]
        )

    def reply(self, user_message, favorites=None):
        favorites = favorites or []
        favorites = [title.strip() for title in favorites if title]

        message = user_message.strip()
        lower_message = message.lower()

        if not message:
            return self.build_response(
                "Please type something so I can help you.",
                ["recommend by favorites", "surprise me", "recommend drama"]
            )

        if self.awaiting_mood:
            mood_genre = self.detect_mood_genre(lower_message)

            if mood_genre:
                movie = self.recommend_movie(mood_genre)
                self.awaiting_mood = False

                if movie:
                    return self.build_response(
                        f"Based on your mood, I recommend '{movie['title']}' from the {movie['category']} category.",
                        ["another one", "tell me about this movie", "best in this genre"],
                        movie=movie,
                        intent="recommendation",
                        show_button=True
                    )

            return self.build_response(
                "Tell me your mood using words like happy, sad, exciting, mysterious, cozy, or emotional.",
                ["I feel sad", "I feel excited", "I want something mysterious"]
            )

        if any(greeting == lower_message for greeting in self.greetings):
            return self.welcome_message()

        if "help" in lower_message:
            return self.help_message()

        if (
            "what are my favorites" in lower_message
            or "show my favorites" in lower_message
            or "my favorite movies" in lower_message
        ):
            if favorites:
                return self.build_response(
                    f"Your favorite movies are: {', '.join(favorites)}.",
                    ["recommend by favorites", "another one", "show me the poster of Interstellar"],
                    intent="favorites"
                )

            return self.build_response(
                "You do not have favorite movies yet.",
                ["recommend by mood", "surprise me", "recommend comedy"],
                intent="favorites"
            )

        if (
            "recommend by favorites" in lower_message
            or "based on my favorites" in lower_message
            or "recommend me by favorites" in lower_message
        ):
            if favorites:
                movie, favorite_movies, primary_genre = self.recommend_by_favorites(favorites)

                if movie:
                    return self.build_response(
                        f"Based on your favorites ({self.favorite_titles_text(favorites)}), I recommend '{movie['title']}' for you. Your favorites mostly point to {primary_genre}.",
                        [
                            "another one",
                            "tell me about this movie",
                            "show me my favorites"
                        ],
                        movie=movie,
                        intent="favorites",
                        show_button=True
                    )

            return self.build_response(
                "You do not have favorite movies saved yet, so I cannot recommend by favorites right now.",
                ["show my favorites", "recommend by mood", "surprise me"],
                intent="favorites"
            )

        if "recommend by mood" in lower_message or "my mood" in lower_message or "depending on my mood" in lower_message:
            self.awaiting_mood = True
            return self.build_response(
                "What is your mood today?",
                ["I feel sad", "I feel happy", "I feel excited"]
            )

        if any(phrase in lower_message for phrase in [
            "show me the poster of this movie",
            "show poster of this movie",
            "show me a poster of this movie",
            "show a poster of this movie",
            "poster of this movie"
        ]):
            if self.last_movie:
                return self.build_response(
                    f"Here is the poster of {self.last_movie['title']}.",
                    ["another one", "tell me about this movie"],
                    movie=self.last_movie,
                    intent="poster",
                    show_poster=True,
                    show_button=True
                )

            return self.build_response(
                "I need a movie first before I can show its poster.",
                ["surprise me", "recommend by mood", "do you have Interstellar?"]
            )

        if any(phrase in lower_message for phrase in [
            "show me the poster of",
            "show poster of",
            "show me a poster of",
            "show a poster of",
            "poster of"
        ]):
            movie = self.find_movie_object(lower_message)

            if movie:
                return self.build_response(
                    f"Here is the poster of {movie['title']}.",
                    ["tell me about this movie", "another one"],
                    movie=movie,
                    intent="poster",
                    show_poster=True,
                    show_button=True
                )

            return self.build_response(
                "I couldn’t find that movie poster in our library.",
                ["do you have Interstellar?", "recommend sci-fi", "recommend by favorites"]
            )
        if "open movie page" in lower_message:
            if self.last_movie:
                return self.build_response(
                    f"You can open the page for {self.last_movie['title']}.",
                    ["tell me about this movie", "show me the poster of this movie", "another one"],
                    movie=self.last_movie,
                    show_button=True
                )

        if "do you have" in lower_message or "is there" in lower_message or "in the library" in lower_message:
            movie = self.find_movie_object(lower_message)

            if movie:
                return self.build_response(
                    f"Yes, we have {movie['title']} in our library.",
                    ["open movie page", "show me the poster of this movie", "tell me about this movie"],
                    movie=movie,
                    intent="exists",
                    show_button=True
                )

            return self.build_response(
                "I couldn’t find that movie in our current library.",
                ["recommend action", "recommend comedy", "recommend by favorites"]
            )

        if "surprise me" in lower_message or "pick for me" in lower_message or "anything is fine" in lower_message:
            movie = random.choice(self.movies)
            self.last_movie = movie
            self.last_genre = movie["category"]
            self.last_source = "surprise"

            return self.build_response(
                f"My surprise pick for you is '{movie['title']}'.",
                ["tell me about this movie", "show me the poster of this movie", "another one"],
                movie=movie,
                intent="recommendation",
                show_button=True
            )

        if "another one" in lower_message or "something similar" in lower_message or lower_message == "another":
            if self.last_source == "favorites" and favorites:
                exclude_title = self.last_movie["title"] if self.last_movie else None
                movie, favorite_movies, primary_genre = self.recommend_by_favorites(
                    favorites,
                    exclude_title=exclude_title
                )

                if movie:
                    return self.build_response(
                        f"Here is another recommendation based on your favorites: '{movie['title']}'.",
                        ["tell me about this movie", "show me the poster of this movie", "show my favorites"],
                        movie=movie,
                        intent="favorites",
                        show_button=True
                    )

            if self.last_genre:
                exclude_title = self.last_movie["title"] if self.last_movie else None
                movie = self.recommend_movie(self.last_genre, exclude_title=exclude_title)

                if movie:
                    return self.build_response(
                        f"Here is another {movie['category']} movie for you: '{movie['title']}'.",
                        ["tell me about this movie", "show me the poster of this movie", "best in this genre"],
                        movie=movie,
                        intent="recommendation",
                        show_button=True
                    )

            return self.build_response(
                "I need to recommend a movie first before I can give you another one.",
                ["recommend by favorites", "recommend by mood", "surprise me"]
            )

        if "tell me about this movie" in lower_message or "tell me about it" in lower_message:
            if self.last_movie:
                return self.build_response(
                    self.movie_details_text(self.last_movie),
                    ["show me the poster of this movie", "open movie page", "another one"],
                    movie=self.last_movie,
                    show_button=True
                )

            return self.build_response(
                "I need to recommend or find a movie first before I can tell you about it.",
                ["surprise me", "recommend comedy", "do you have Interstellar?"]
            )

        if "best in this genre" in lower_message:
            if self.last_genre:
                movie = self.get_top_rated_movie(self.last_genre)

                if movie:
                    return self.build_response(
                        f"The top-rated {movie['category']} movie in our library is '{movie['title']}' with a rating of {movie['rating']}.",
                        ["tell me about this movie", "show me the poster of this movie", "open movie page"],
                        movie=movie,
                        intent="top_rated",
                        show_button=True
                    )

            return self.build_response(
                "I need a genre first before I can show the best movie in it.",
                ["recommend action", "recommend mystery", "recommend by favorites"]
            )

        if "best" in lower_message or "top rated" in lower_message or "highest rated" in lower_message:
            genre = self.detect_genre(lower_message)

            if genre:
                movie = self.get_top_rated_movie(genre)

                if movie:
                    return self.build_response(
                        f"The top-rated {movie['category']} movie in our library is '{movie['title']}' with a rating of {movie['rating']}.",
                        ["tell me about this movie", "show me the poster of this movie", "open movie page"],
                        movie=movie,
                        intent="top_rated",
                        show_button=True
                    )

            movie = self.get_top_rated_movie()

            if movie:
                return self.build_response(
                    f"The highest-rated movie in our library is '{movie['title']}' with a rating of {movie['rating']}.",
                    ["tell me about this movie", "show me the poster of this movie", "open movie page"],
                    movie=movie,
                    intent="top_rated",
                    show_button=True
                )

        movie = self.find_movie_object(lower_message)
        if movie and (
            "tell me about" in lower_message
            or "what is" in lower_message
            or "facts about" in lower_message
            or lower_message == movie["title"].lower()
        ):
            self.last_movie = movie
            self.last_genre = movie["category"]

            return self.build_response(
                self.movie_details_text(movie),
                ["show me the poster of this movie", "open movie page", "another one"],
                movie=movie,
                show_button=True
            )

        direct_mood_genre = self.detect_mood_genre(lower_message)
        if direct_mood_genre and (
            "feel" in lower_message
            or "mood" in lower_message
            or "want something" in lower_message
            or "i want" in lower_message
        ):
            movie = self.recommend_movie(direct_mood_genre)

            if movie:
                return self.build_response(
                    f"Based on your mood, I recommend '{movie['title']}' from the {movie['category']} category.",
                    ["another one", "tell me about this movie", "show me the poster of this movie"],
                    movie=movie,
                    intent="recommendation",
                    show_button=True
                )

        genre = self.detect_genre(lower_message)
        if genre:
            movie = self.recommend_movie(genre)

            if movie:
                return self.build_response(
                    f"I recommend '{movie['title']}' from the {movie['category']} category.",
                    ["another one", "tell me about this movie", "best in this genre"],
                    movie=movie,
                    intent="recommendation",
                    show_button=True
                )

        if "bye" in lower_message or "goodbye" in lower_message:
            return self.build_response(
                "Goodbye! Come back when you want another movie recommendation.",
                ["recommend by favorites", "recommend by mood", "surprise me"],
                intent="goodbye"
            )

        return self.fallback_message()


assistant = MovieAssistantChatbot()


def movie_assistant(user_message, favorites=None):
    return assistant.reply(user_message, favorites)