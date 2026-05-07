# users
users = {
    "admin": "1234",
    "raghad": "0000"
}

current_user = None

def login_user(username, password):
    global current_user

    if username in users:
        if users[username] == password:
            current_user = username
            return True
        else:
            return False
    else:
        return False


# movies
movies = [
    {"title": "Mad Max", "category": "Action", "rating": 8},
    {"title": "John Wick", "category": "Action", "rating": 7},
    {"title": "Frozen", "category": "Family", "rating": 7},
    {"title": "Joker", "category": "Drama", "rating": 9}
]

def get_movies(category):
    result = []

    for m in movies:
        if m["category"] == category:
            result.append(m)

    return result