DEBUG = True

"""
# CORS_ALLOW_CREDENTIALS=True 임에도 whitelist는 필요하다!
# CORS_ALLOW_ALL_ORIGINS = True <- 이거 있으면 whitelist 필요 x
CORS_ORIGIN_WHITELIST = [
    "https://localhost:8082",
    "http://localhost:8082",
    "https://localhost",
    "http://localhost",
]
"""

# If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "https://localhost",
    "https://192.168.1.243",
]

ALLOWED_HOSTS = ["*"]
