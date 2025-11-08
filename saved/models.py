from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    role = models.CharField(max_length=10, default='admin')
    fname = models.CharField(max_length=60)
 
class saved(models.Model):
    fname = models.CharField(max_length=60)
    mname = models.CharField(max_length=60)
    lname = models.CharField(max_length=60)
    profile_picture = models.FileField(upload_to='profile_pics/')
    phone_no = models.CharField(max_length=13)  
    location = models.CharField(max_length=200) 
    registered_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.full_name
    @property
    def full_name(self):
        return " ".join(part for part in [self.fname, self.mname, self.lname] if part)
    

class news(models.Model):
    new = models.TextField()
    title = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.new
    
