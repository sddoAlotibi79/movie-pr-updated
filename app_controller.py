from movies_data import movies, movie_details
from movie_details_logic import get_movie_details


# =========================
# تسجيل الدخول (ربط سريع)
# =========================

users = {
    "admin": "1234",
    "raghad": "0000"
}

current_user = None


def login(username, password):
    global current_user

    if username in users and users[username] == password:
        current_user = username
        return True

    return False


def logout():
    global current_user
    current_user = None
    return True


def get_user():
    return current_user


# =========================
# الفئات
# =========================

def get_categories():
    return ["Action", "Comedy", "Drama", "Sci-Fi", "Family", "Mystery"]


# =========================
# جلب أفلام حسب الفئة
# =========================

def get_movies_by_category(category):
    return [m for m in movies if m["category"] == category]


# =========================
# البحث عن فيلم
# =========================

def search_movies(keyword):
    return [m for m in movies if keyword.lower() in m["title"].lower()]


# =========================
# اختيار فيلم + تفاصيله
# =========================

def open_movie(title):
    return get_movie_details(title)


# =========================
# فتح فئة كاملة (واجهة جاهزة)
# =========================

def open_category(category):
    return get_movies_by_category(category)