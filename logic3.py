# =========================
# Profile Page Logic
# =========================

from logic1 import current_user

# الأفلام المفضلة لكل مستخدم (مؤقتاً)
favorite_movies = {
    "admin": ["John Wick", "Joker"],
    "raghad": ["Frozen", "Coco"]
}
def get_profile_data():
    """
    يرجع بيانات المستخدم الحالي:
    - الاسم
    - الأفلام المفضلة
    """

    user = current_user

    if not user:
        return {
            "status": False,
            "message": "No user logged in"
        }

    return {
        "status": True,
        "username": user,
        "favorites": favorite_movies.get(user, [])
    }
def add_favorite_movie(movie_name):
    """إضافة فيلم لقائمة المفضلة"""

    user = current_user

    if not user:
        return False

    if user not in favorite_movies:
        favorite_movies[user] = []

    if movie_name not in favorite_movies[user]:
        favorite_movies[user].append(movie_name)

    return True
def logout():
    """تسجيل خروج المستخدم"""

    global current_user
    current_user = None

    return "LOGOUT_SUCCESS"
def back_to_home():
    """زر الرجوع للهوم"""

    return "HOME_PAGE"