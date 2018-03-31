from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts-images', blank=True)
    sound = models.FileField(upload_to='musics', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post

class Sound(models.Model):
    author = models.CharField(max_length=100)
    sound_name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='sound-images', blank=True)
    sound = models.FileField(upload_to='sounds', blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sound_name

class Picture(models.Model):
    author = models.ForeignKey(User, related_name='picture_creater', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='pictures', blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Картинка'

class MySound(models.Model):
    sounds = models.ManyToManyField(Sound)
    current_user = models.ForeignKey(User, related_name='sound_haver', null=True, on_delete=models.CASCADE)

    @classmethod
    def add_file(cls, current_user, new_sound):
        haver, created = cls.objects.get_or_create(
            current_user=current_user,
        )
        haver.sounds.add(new_sound)

    @classmethod
    def lose_file(cls, current_user, new_sound):
        haver, created = cls.objects.get_or_create(
            current_user=current_user,
        )
        haver.sounds.remove(new_sound)

    def __str__(self):
        return self.current_user.username

class MyPicture(models.Model):
    pictures = models.ManyToManyField(Picture)
    current_user = models.ForeignKey(User, related_name='picture_haver', null=True, on_delete=models.CASCADE)

    @classmethod
    def add_file(cls, current_user, new_picture):
        haver, created = cls.objects.get_or_create(
            current_user=current_user,
        )
        haver.pictures.add(new_picture)

    @classmethod
    def lose_file(cls, current_user, new_picture):
        haver, created = cls.objects.get_or_create(
            current_user=current_user,

        )
        haver.pictures.remove(new_picture)

    def __str__(self):
        return self.current_user.username

class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

    def __str__(self):
        return self.current_user.username

class AllMsg(models.Model):
    text = models.TextField()
    sender_user = models.ForeignKey(User, related_name='sender_u', on_delete=models.CASCADE)
    recipient_user = models.ForeignKey(User, related_name='recipient_u', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
