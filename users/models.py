from django.db import models
from django.contrib.auth.models import User
import random

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randit(100000, 999999))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.user.username}: {self.code}'