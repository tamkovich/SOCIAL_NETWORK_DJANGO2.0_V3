from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfileManager(models.Manager):
	def get_queryset(self):
		return super(UserProfileManager, self).get_queryset().all()

class UserProfille(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=100, default='')
	city = models.CharField(max_length=100, default='')
	website = models.URLField(default='')
	phone = models.IntegerField(default=0)
	image = models.ImageField(upload_to='profile_image', blank=True)
	sex = models.CharField(max_length=1, default='M')

	def __str__(self):
		return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfille.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
