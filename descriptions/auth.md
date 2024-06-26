* install
```
pip install djangorestframework-simplejwt
```

* settings.py
```

INSTALLED_APPS = [
    ...
    "rest_framework_simplejwt",
    ...
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        # 모든 view에 Auth 체크가 적용된다.
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # JWT를 통한 인증을 위해 추가
        ...
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        ...
    ],
}


# 커스텀 유저 모델 사용, "어플리케이션명.모델명"
AUTH_USER_MODEL = "user.User"  

# simple jwt 옵션 제공
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "email",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.MyTokenObtainPairSerializer",
}
```

* models.py
```
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username=None, email=None, password=None, **extra_fields
    ):
        superuser = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        superuser.auth = 1

        # 아래 핃드는 사라졌기 때문에 필요가 없어졌다.
        # superuser.is_staff = True
        # superuser.is_superuser = True
        # superuser.is_active = True

        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser):
    """
    AbstractUser: Use this option if you are happy with the existing fields on the user model and just want to remove the username field.
    AbstractBaseUser: Use this option if you want to start from scratch by creating your own, completely new user model.

    PermissionsMixin 을 함께 상속하면 Django의 기본그룹, 허가권 관리 등을 사용할 수 있습니다.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)
    auth = models.IntegerField(default=0)

    USERNAME_FIELD = "email"  # 사용자 로그인 필드로 user_id가 아니라 email을 기본값으로 지정
    REQUIRED_FIELDS = ["username"]

    """
        기존에 django에서 만들어주는 auth_user에 없는 필드들이 있기 때문에
        사용자를 저장하려면 내 user model에 맞도록 manager를 재 정의 해줘야 한다.
    """
    objects = CustomUserManager()

    """
        'User' object has no attribute 'is_staff'
        'User' object has no attribute 'has_perm'
        'User' object has no attribute 'has_module_perms'
        아래 함수를 넣어야 위 오류가 해결된다.
        
        이럴거면 그냥 is_staff, is_admin, is_superuser 를 넣는게 낫지 않나?
    """

    @property
    def is_staff(self):
        return self.auth

    def has_perm(self, perm, obj=None):
        # return self.is_superuser
        return self.auth

    def has_module_perms(self, app_label):
        # return self.is_superuser
        return self.auth

    class Meta:
        """
        managed=False
            If False, no database table creation, modification, or deletion operations will be performed for this model.
            This is useful if the model represents an existing table or a database view that has been created by some other means.
        """

        db_table = "user"

```