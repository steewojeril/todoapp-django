from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
class Todo(models.Model):
    task_name=models.CharField(max_length=120)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.task_name
    
