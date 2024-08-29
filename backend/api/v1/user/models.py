import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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
        superuser.is_superuser = True

        # 아래 핃드는 사라졌기 때문에 필요가 없어졌다.
        # superuser.is_staff = True
        # superuser.is_active = True

        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """
    AbstractUser: Use this option if you are happy with the existing fields on the user model and just want to remove the username field.
    AbstractBaseUser: Use this option if you want to start from scratch by creating your own, completely new user model.

    PermissionsMixin 을 함께 상속하면 Django의 기본그룹, 허가권 관리 등을 사용할 수 있습니다.
     -> PermissionsMixin이 없으면 get_all_permissions 등 permission 관련 method를 사용할 수 없다.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False
    )  # uuid는 Token에서만 사용! 내부적으론 int를 쓰는게 좋을 것 같다
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=100)
    auth = models.IntegerField(default=0)

    USERNAME_FIELD = (
        "email"  # 사용자 로그인 필드로 user_id가 아니라 email을 기본값으로 지정
    )
    REQUIRED_FIELDS = ["username"]

    """
        PermissionsMixin 필드 리스트
            1. groups - ManyToMany
            2. user_permissions - ManyToMany
            3. is_superuser
    """

    """
        AbstractBaseUser 필드 리스트
            1. password
            2. last_login
    """

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

        이 문제는 PermissionsMixin을 상속받으면 해결된다. 아니면 내부를 직접구현해 줘야해서 권장하지 않는다.
    """

    @property
    def is_staff(self):
        return self.auth

    def __str__(self):
        return self.username

    class Meta:
        """
        managed=False
            If False, no database table creation, modification, or deletion operations will be performed for this model.
            This is useful if the model represents an existing table or a database view that has been created by some other means.
        """

        db_table = "user"
        verbose_name = "사용자"
