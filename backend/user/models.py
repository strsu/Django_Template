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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        """
        managed=False
            If False, no database table creation, modification, or deletion operations will be performed for this model.
            This is useful if the model represents an existing table or a database view that has been created by some other means.
        """

        db_table = "user"
