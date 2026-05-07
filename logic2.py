# =========================
# Home Page Logic (Updated with login integration)
# =========================

# نفس المستخدم اللي يجي من login_user
current_user = None


def sync_user():
    """
    مزامنة المستخدم من login_user
    (تستدعيها بعد تسجيل الدخول)
    """
    global current_user
    try:
        from logic1 import current_user as logged_user
        current_user = logged_user
    except:
        current_user = None


def get_current_user():
    """إرجاع المستخدم الحالي"""
    return current_user

def go_to_profile():
    return "PROFILE_PAGE"


def go_to_categories():
    return "CATEGORIES_PAGE"


def go_to_chat():
    return "CHAT_PAGE"
