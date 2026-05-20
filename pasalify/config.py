from datetime import timedelta

class Config:
    SECRET_KEY                 = "pasalify-secret-2026"
    WTF_CSRF_ENABLED           = True
    SESSION_COOKIE_HTTPONLY    = True
    SESSION_COOKIE_SAMESITE    = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    DEBUG                      = True
