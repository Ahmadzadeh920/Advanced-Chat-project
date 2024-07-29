from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(blank=False)
    password = models.CharField()

    def __str__(self):
        return self.email
    
class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField()
    desc = models.TextField()
    def __str__(self):
        return self.title



class Profile(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField()
    last_name = models.CharField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='roles')


    def __str__(self):
        return f'{self.user.username} Profile'


