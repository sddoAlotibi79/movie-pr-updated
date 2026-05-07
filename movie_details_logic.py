from movies_data import movie_details


# =========================
# جلب تفاصيل الفيلم (القصة + التقييم + الفيديو)
# =========================

def get_movie_details(title):
    return movie_details.get(title, None)


# =========================
# استخراج القصة فقط
# =========================

def get_movie_story(title):
    movie = movie_details.get(title)
    if movie:
        return movie["story"]
    return None


# =========================
# استخراج التقييم فقط
# =========================

def get_movie_rating(title):
    movie = movie_details.get(title)
    if movie:
        return movie["rating"]
    return None


# =========================
# استخراج رابط الفيديو فقط
# =========================

def get_movie_video(title):
    movie = movie_details.get(title)
    if movie:
        return movie["video"]
    return None