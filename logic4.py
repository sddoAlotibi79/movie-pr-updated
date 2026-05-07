from movies_data import movies, movie_details


# =========================
# الفئات (Categories)
# =========================

def get_categories():
    return ["Action", "Sci-Fi", "Family", "Drama", "Comedy", "Mystery"]


# =========================
# البحث عن فيلم
# =========================

def search_movies(keyword):
    results = []

    for movie in movies:
        if keyword.lower() in movie["title"].lower():
            results.append(movie)

    return results


# =========================
# جلب أفلام حسب الفئة
# =========================

def get_movies_by_category(category):
    results = []

    for movie in movies:
        if movie["category"] == category:
            results.append(movie)

    return results


# =========================
# اختيار فيلم (لصفحة التفاصيل)
# =========================

selected_movie = None


def select_movie(title):
    global selected_movie

    for movie in movies:
        if movie["title"] == title:
            selected_movie = movie
            return movie

    return None


def get_selected_movie():
    return selected_movie


# =========================
# جلب تفاصيل الفيلم
# =========================

def get_movie_details(title):
    return movie_details.get(title, None)