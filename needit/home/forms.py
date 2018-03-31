from django import forms
from home.models import (
	Post,
	Sound,
	Picture,
)

class HomeForm(forms.ModelForm):
	post = forms.CharField(widget=forms.TextInput(
									attrs={
													'class': 'form-control',
													'placeholder': 'Write a post...'
									}
				))

	class Meta:
		model = Post
		fields = ('post',)

class UploadSoundForm(forms.ModelForm):
	sound_name = forms.CharField(widget=forms.TextInput(
									attrs={
													'class': 'form-control',
													'placeholder': 'Введите название песни...'
									}
				))

	author = forms.CharField(widget=forms.TextInput(
									attrs={
													'class': 'form-control',
													'placeholder': 'Введите имя исполнителя...'
									}
	))

	class Meta:
		model = Sound
		fields = (
			'sound_name',
			'author',
			'sound',
			'picture',
		)

class UploadPictureForm(forms.ModelForm):
	
	class Meta:
		model = Picture
		fields = ('picture',)