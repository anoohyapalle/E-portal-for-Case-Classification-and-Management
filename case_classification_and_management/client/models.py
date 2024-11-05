from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.lawyer.username} - {self.client}"    