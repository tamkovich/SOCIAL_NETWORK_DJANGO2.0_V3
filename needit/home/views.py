from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.forms import (
	HomeForm,
	UploadSoundForm,
	UploadPictureForm,
)
from django.contrib.auth.models import User
from django.db.models import Q

from django.views.generic import TemplateView

from django.utils.safestring import mark_safe
import json
from home.models import (
	Post,
	Friend,
	Sound,
	Picture,
	MySound,
	MyPicture,
)


# Create your views here.
class HomeView(TemplateView):
	template_name = 'home/home.html'

	def get(self, request):
		form = HomeForm()
		posts = Post.objects.all().order_by('-created')
		users = User.objects.exclude(id=request.user.id)
		try:
			friend = Friend.objects.get(current_user=request.user)
			friends = friend.users.all()
		except:
			friends = None

		your_id = request.user.id

		args = {
			'form': form,
			'posts': posts,
			'users': users,
			'friends': friends,
			'your_id': your_id,
		}
		return render(request, self.template_name, args)

	def post(self, request):
		form = HomeForm(request.POST)
		# print(form.is_valid(), form.errors)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			text = form.cleaned_data['post']
			form = HomeForm()
			return redirect('home:home')

		args = {
			'form': form,
			'text': text,
		}
		return render(request, self.template_name, args)

def change_friends(request, operation, pk):
	friend = User.objects.get(pk=pk)
	if friend:
		if operation == 'add':
			Friend.make_friend(request.user, friend)
			Friend.make_friend(friend, request.user)
		elif operation == 'remove':
			Friend.lose_friend(request.user, friend)
			Friend.lose_friend(friend, request.user)
	return redirect('home:home')

def view_friends(request):
	users = User.objects.exclude(id=request.user.id)
	try:
		friend = Friend.objects.get(current_user=request.user)
		friends = friend.users.all()
	except:
		friends = None
	args = {
		'friends': friends,
		'users': users,
	}
	return render(request, 'home/friends.html', args)

def room(request, room_name):
  return render(request, 'home/room.html', {
      'room_name_json': mark_safe(json.dumps(room_name))
  })

class FileView(TemplateView):
	template_name = 'home/files.html'
	def get(self, request):
		sound_form = UploadSoundForm()
		picture_form = UploadPictureForm()
		try:
			sounds = Sound.objects.all()
		except:
			sounds = None
		try:
			pictures = Picture.objects.all()
		except:
			pictures = None
		try:
			myself = MySound.objects.get(current_user=request.user)
			my_sounds = myself.pictures.all()
		except:
			my_sounds = None
		try:
			myself = MyPicture.objects.get(current_user=request.user)
			my_pictures = myself.pictures.all()
		except:
			my_pictures = None
		args = {
			'sound_form': sound_form,
			'picture_form': picture_form,
			'sounds': sounds,
			'pictures': pictures,
			'my_sounds': my_sounds,
			'my_pictures': my_pictures,
			'current_user': request.user,
		}
		return render(request, self.template_name, args)

	def post(self, request):
		sound_form = UploadSoundForm(request.POST, request.FILES)
		if sound_form.is_valid():
			sound = sound_form.save(commit=False)
			sound.user = request.user
			sound.save()
			sound_form = UploadSoundForm()
			return redirect('home:files')

		picture_form = UploadPictureForm(request.POST, request.FILES)
		if picture_form.is_valid():
			picture = picture_form.save(commit=False)
			picture.author = request.user
			picture.save()
			picture_form = UploadPictureForm()
			return redirect('home:files')

		args = {
			'sound_form': sound_form,
			'picture_form': picture_form,
		}
		return render(request, self.template_name, args)

class SoundView(TemplateView):
	template_name = 'home/sounds.html'
	def get(self, request):
		sound_form = UploadSoundForm()
		try:
			sounds = Sound.objects.all()
		except:
			sounds = None
		try:
			myself = MySound.objects.get(current_user=request.user)
			my_sounds = myself.sounds.all()
		except:
			my_sounds = None
		args = {
			'sound_form': sound_form,
			'sounds': sounds,
			'my_sounds': my_sounds,
			'current_user': request.user,
		}
		return render(request, self.template_name, args)

	def post(self, request):
		sound_form = UploadSoundForm(request.POST, request.FILES)
		if sound_form.is_valid():
			sound = sound_form.save(commit=False)
			sound.user = request.user
			sound.save()
			sound_form = UploadSoundForm()
			return redirect('home:sounds')
			
		args = {
			'sound_form': sound_form,
		}
		return render(request, self.template_name, args)

class PictureView(TemplateView):
	template_name = 'home/pictures.html'
	def get(self, request):
		picture_form = UploadPictureForm()
		try:
			pictures = Picture.objects.all()
		except:
			pictures = None
		try:
			myself = MyPicture.objects.get(current_user=request.user)
			my_pictures = myself.pictures.all()
		except:
			my_pictures = None
		args = {
			'picture_form': picture_form,
			'pictures': pictures,
			'my_pictures': my_pictures,
			'current_user': request.user,
		}
		return render(request, self.template_name, args)

	def post(self, request):
		picture_form = UploadPictureForm(request.POST, request.FILES)
		if picture_form.is_valid():
			picture = picture_form.save(commit=False)
			picture.author = request.user
			picture.save()
			picture_form = UploadPictureForm()
			return redirect('home:pictures')
			
		args = {
			'picture_form': picture_form,
		}
		return render(request, self.template_name, args)

def change_sounds(request, operation, pk):
	sound = Sound.objects.get(pk=pk)
	if sound:
		if operation == 'add':
			MySound.add_file(request.user, sound)
		elif operation == 'remove':
			MySound.lose_file(request.user, sound)
	return redirect('home:sounds')

def change_pictures(request, operation, pk):
	picture = Picture.objects.get(pk=pk)
	if picture:
		if operation == 'add':
			MyPicture.add_file(request.user, picture)
		elif operation == 'remove':
			MyPicture.lose_file(request.user, picture)
	return redirect('home:pictures')