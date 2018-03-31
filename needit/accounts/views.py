from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from accounts.forms import (
    RegistrationForm, 
    EditProfileForm,
)
from home.forms import (
    UploadSoundForm,
    UploadPictureForm,
)

from home.models import (
    Friend,
    Sound,
    Picture,
    MySound,
    MyPicture,
)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)

def view_profile(request, pk=None):
    if pk:
        if int(pk)==request.user.id:
            return redirect('accounts:view_profile')
        user = User.objects.get(pk=pk)
        try:
            friend = Friend.objects.get(current_user=request.user)
            if user in friend.users.all():
                is_he_your_friend = True
        except:
            is_he_your_friend = None
    else:
        user = request.user
        is_he_your_friend = None
    args = {
        'myself_id': request.user.id,
        'user': user,
        'is_he_your_friend': is_he_your_friend
    }
    return render(request, 'accounts/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/account/profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return redirect('/account/change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}

        return render(request, 'accounts/change_password.html', args)

class FileView(TemplateView):
    template_name = 'accounts/files.html'
    def get(self, request, pk=None):
        if pk and int(pk)==request.user.id:
            return redirect('accounts:files')
        sound_form = UploadSoundForm()
        picture_form = UploadPictureForm()
        try:
            myself = MySound.objects.get(current_user=request.user)
            my_sounds = myself.sounds.all()
        except:
            my_sounds = None
        try:
            myself = MyPicture.objects.get(current_user=request.user)
            my_pictures = myself.pictures.all()
        except:
            my_pictures = None
        if pk:
            curent_user = User.objects.get(pk=pk)
            try:
                some_user = MySound.objects.get(current_user=curent_user)
                user_sounds = some_user.sounds.all()
            except:
                user_sounds = None
            try:
                some_user = MyPicture.objects.get(current_user=curent_user)
                user_pictures = some_user.pictures.all()
            except:
                user_pictures = None
        else:
            user_sounds = my_sounds
            user_pictures = my_pictures
            curent_user = request.user
        args = {
            'sound_form': sound_form,
            'picture_form': picture_form,
            'user_sounds': user_sounds,
            'user_pictures': user_pictures,
            'my_sounds': my_sounds,
            'my_pictures': my_pictures,
            'current_user': curent_user,
            'myself': request.user,
        }
        return render(request, self.template_name, args)

    def post(self, request, pk=None):
        sound_form = UploadSoundForm(request.POST, request.FILES)
        if sound_form.is_valid():
            sound = sound_form.save(commit=False)
            sound.user = request.user
            sound.save()
            sound_form = UploadSoundForm()
            if pk:
                return redirect('accounts:files', pk=pk)
            else:
                return redirect('accounts:files')

        picture_form = UploadPictureForm(request.POST, request.FILES)
        if picture_form.is_valid():
            picture = picture_form.save(commit=False)
            picture.author = request.user
            picture.save()
            picture_form = UploadPictureForm()
            if pk:
                return redirect('accounts:files', pk=pk)
            else: 
                return redirect('accounts:files')

        args = {
            'sound_form': sound_form,
            'picture_form': picture_form,
        }
        return render(request, self.template_name, args)

class SoundView(TemplateView):
    template_name = 'accounts/sounds.html'
    def get(self, request, pk=None):
        if pk and int(pk)==request.user.id:
            return redirect('accounts:sounds')
        sound_form = UploadSoundForm()
        try:
            myself = MySound.objects.get(current_user=request.user)
            my_sounds = myself.sounds.all()
        except:
            my_sounds = None
        if pk:
            curent_user = User.objects.get(pk=pk)
            try:
                some_user = MySound.objects.get(current_user=curent_user)
                user_sounds = some_user.sounds.all()
            except:
                user_sounds = None
        else:
            user_sounds = my_sounds
            curent_user = request.user
        args = {
            'sound_form': sound_form,
            'user_sounds': user_sounds,
            'my_sounds': my_sounds,
            'current_user': curent_user,
            'myself': request.user,
        }
        return render(request, self.template_name, args)

    def post(self, request, pk=None):
        sound_form = UploadSoundForm(request.POST, request.FILES)
        if sound_form.is_valid():
            sound = sound_form.save(commit=False)
            sound.user = request.user
            sound.save()
            sound_form = UploadSoundForm()
            if pk:
                return redirect('accounts:sounds', pk=pk)
            else:
                return redirect('accounts:sounds')

        args = {
            'sound_form': sound_form,
        }
        return render(request, self.template_name, args)

class PictureView(TemplateView):
    template_name = 'accounts/pictures.html'
    def get(self, request, pk=None):
        if pk and int(pk)==request.user.id:
            return redirect('accounts:pictures')
        picture_form = UploadPictureForm()
        try:
            myself = MyPicture.objects.get(current_user=request.user)
            my_pictures = myself.pictures.all()
        except:
            my_pictures = None
        if pk:
            curent_user = User.objects.get(pk=pk)
            try:
                some_user = MyPicture.objects.get(current_user=curent_user)
                user_pictures = some_user.pictures.all()
            except:
                user_pictures = None
        else:
            user_pictures = my_pictures
            curent_user = request.user
        args = {
            'picture_form': picture_form,
            'user_pictures': user_pictures,
            'my_pictures': my_pictures,
            'current_user': curent_user,
            'myself': request.user,
        }
        return render(request, self.template_name, args)

    def post(self, request, pk=None):
        picture_form = UploadPictureForm(request.POST, request.FILES)
        if picture_form.is_valid():
            picture = picture_form.save(commit=False)
            picture.author = request.user
            picture.save()
            picture_form = UploadPictureForm()
            if pk:
                return redirect('accounts:pictures', pk=pk)
            else:
                return redirect('accounts:pictures')
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
    return redirect('accounts:sounds')

def change_pictures(request, operation, pk):
    picture = Picture.objects.get(pk=pk)
    if picture:
        if operation == 'add':
            MyPicture.add_file(request.user, picture)
        elif operation == 'remove':
            MyPicture.lose_file(request.user, picture)
    return redirect('accounts:pictures')
