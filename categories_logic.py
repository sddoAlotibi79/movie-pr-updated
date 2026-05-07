from movies_data import movies
import matplotlib.pyplot as plt


# =========================
# الفئات
# =========================

def get_categories():
    return ["Action", "Comedy", "Drama", "Sci-Fi", "Family", "Mystery"]


# =========================
# جلب أفلام حسب الفئة (الدالة الأساسية)
# =========================

def get_movies_by_category(category):
    return [m for m in movies if m["category"] == category]


# =========================
# بيانات المشاهدات لكل الفئات
# =========================

views_data = {
    "Action": {
        "Mad Max: Fury Road": 1200,
        "John Wick": 2500,
        "Avengers: Endgame": 5000,
        "Fast & Furious 7": 1800,
        "Black Panther": 3000
    },

    "Comedy": {
        "The Hangover": 2100,
        "Superbad": 1800,
        "The Internship": 950,
        "School of Rock": 1300,
        "The Devil Wears Prada": 1600
    },

    "Drama": {
        "The Shawshank Redemption": 5000,
        "The Godfather": 4500,
        "Forrest Gump": 4000,
        "A Beautiful Mind": 3000,
        "The Pursuit of Happyness": 3500
    },

    "Sci-Fi": {
        "Interstellar": 4800,
        "Gravity": 2200,
        "Arrival": 2500,
        "The Martian": 2700,
        "Edge of Tomorrow": 3100
    },

    "Family": {
        "Frozen": 3000,
        "Moana": 2800,
        "Coco": 4200,
        "The Lion King": 5000,
        "Zootopia": 3900
    },

    "Mystery": {
        "Shutter Island": 2600,
        "Se7en": 4100,
        "Prisoners": 3300,
        "Black Swan": 2900,
        "Knives Out": 3600
    }
}


# =========================
# أعلى فيلم في أي فئة
# =========================

def get_top_movie(category):
    category_views = views_data.get(category, {})

    if not category_views:
        return None, 0

    top_movie = max(category_views, key=category_views.get)
    return top_movie, category_views[top_movie]


# =========================
# رسم Bar Plot لأي فئة
# =========================

def plot_category(category):
    category_views = views_data.get(category, {})

    titles = list(category_views.keys())
    views = list(category_views.values())

    plt.figure(figsize=(10, 5))
    plt.bar(titles, views)

    plt.title(f"{category} Movies Views")
    plt.xlabel("Movies")
    plt.ylabel("Views")

    plt.xticks(rotation=30)

    for i, value in enumerate(views):
        plt.text(i, value + 50, str(value), ha='center')

    plt.tight_layout()
    plt.show()