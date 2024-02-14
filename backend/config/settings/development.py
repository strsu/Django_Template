DEBUG = False

# CORS_ALLOW_ALL_ORIGINS = True # 이건 True해도 WHITELIST 없으면 cors 발생함,,

CORS_ALLOW_CREDENTIALS = True  # 이건 반드시 필요, 없으면 cors 발생
CORS_ORIGIN_WHITELIST = [
    "https://localhost:8082",
    "http://localhost:8082",
    "https://localhost",
    "http://localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "https://localhost",
    "https://192.168.1.243",
    "https://192.168.9.113",
]

ALLOWED_HOSTS = ["*"]
