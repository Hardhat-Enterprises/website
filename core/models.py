from django.db import models

class BlacklistedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    is_blacklisted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address
