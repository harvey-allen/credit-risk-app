import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel

from helpers.base_model import BaseModel


class Title(models.TextChoices):
    MR = "Mr", _("Mr")
    MRS = "Mrs", _("Mrs")
    MS = "Ms", _("Ms")
    DR = "Dr", _("Dr")
    PROF = "Prof", _("Prof")
    OTHER = "Other", _("Other")


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class User(SafeDeleteModel, AbstractUser, BaseModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)

    title = models.CharField(
        max_length=10,
        choices=Title.choices,
        null=True,
        blank=True,
    )

    phone_number = models.CharField(max_length=11)

    objects = UserManager()

    def __str__(self):
        return self.email
