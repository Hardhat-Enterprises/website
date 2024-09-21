from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_platform_leader= models.BooleanField('Is Platform Leader', default=False)
    is_platform_senior_developer = models.BooleanField('Is Platform Senior Developer', default=False)
    is_platform_general_developer = models.BooleanField('Is Platform General Developer', default=False)
    is_external_user = models.BooleanField('Is External User', default=False)