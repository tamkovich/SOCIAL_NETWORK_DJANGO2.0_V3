from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
  content = models.CharField(max_length=500, blank=True)
  # sender_user = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
  # recipient_user = models.ForeignKey(User, related_name='recipient', on_delete=models.CASCADE)
  id_user = models.IntegerField(default=0)
  room_name = models.CharField(max_length=500, default='dialog-1-5')
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  image = models.ImageField(upload_to='posts-images', blank=True)
  sound = models.FileField(upload_to='musics', blank=True)

  def __str__(self):
      return self.room_name