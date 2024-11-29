from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser = True"))
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff = True"))

        return self._create_user(email, password, **extra_fields)


class TimestampMixin(models.Model):
    '''
    Inherit this mixin to have created_at and updated_at fields
    '''

    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class AbstractBaseSet(TimestampMixin):
    '''
    Base model
    '''

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

