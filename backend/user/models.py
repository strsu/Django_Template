import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
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

    class Meta:
        """
        managed=False
            If False, no database table creation, modification, or deletion operations will be performed for this model.
            This is useful if the model represents an existing table or a database view that has been created by some other means.
        """

        db_table = "user"
