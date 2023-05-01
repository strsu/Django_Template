"""
    setting.py에 env로 변수를 설정하면
    supervisor에서 env값 인지를 못해서,,
"""

POSTGRES = {
    "POSTGRES_DB": "postgres",
    "POSTGRES_USER": "postgres",
    "POSTGRES_PASSWORD": "postgres",
    "POSTGRES_HOST": "postgres",
    "POSTGRES_PORT": 5432,
}

CORE = {
    "SECRET_KEY": "django-insecure-z^y14w-b*meb*%64-9zjy_dc3qmk)ddn)b$2z)2w_c(8h_c6qn"
}
