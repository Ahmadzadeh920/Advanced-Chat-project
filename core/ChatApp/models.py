from django.db import models
from django.urls import reverse
from accounts.models import Profile , CustomUser


# Create your models here.

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128 , unique=True)

    def __str__(self):
        return self.group_name
    
    def get_absolute_api_url(self):
        return reverse("ChatApp:api-v1:group-messages-retrieve", kwargs={"pk": self.id})
    

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup , related_name="chat_message" , on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.name} :{self.body}'
    
    class Meta:
        ordering = ['-created']
