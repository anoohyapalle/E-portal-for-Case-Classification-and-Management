from django.db import models
from django.contrib.auth.models import User

class CaseType(models.Model):
    id = models.AutoField(primary_key=True)
    case =  models.CharField(max_length=100)
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.lawyer.username}'