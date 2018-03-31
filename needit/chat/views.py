from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm
from django.db.models import Q
from django.utils.safestring import mark_safe
import json

from django.views.generic import TemplateView

# Create your views here.
class ChatView(TemplateView):
	dialog = 'dialog'
	conversation = 'conversation'
	template_name = 'chat/chat.html'

	def get(self, request, room_name):
		chat_type, fpk, lpk = room_name.split('-')
		if request.user.id == int(fpk):
			if chat_type==self.dialog:
				pk = lpk
				our_chat_id = chat_type+'-'
				our_chat_id += fpk+'-'+lpk if lpk>fpk else lpk+'-'+fpk
				form = MessageForm()
				messages = Message.objects.filter(room_name=our_chat_id)
				myself = request.user
				interlocutor = User.objects.get(pk=pk)
				args = {
					'form': form,
					'messages': messages,
					'myself': myself,
					'interlocutor': interlocutor,
					'room_name_json': mark_safe(json.dumps(room_name)),
				}
				return render(request, self.template_name, args)
		raise Http404("Can't find this chat-page")			

	def post(self, request, room_name):
		chat_type, fpk, lpk = room_name.split('-')
		form = MessageForm(request.POST)
		if form.is_valid():
			message = form.save(commit=False)
			message.id_user = request.user.id
			message.room_name = chat_type + '-'
			message.room_name += fpk+'-'+lpk if lpk>fpk else lpk+'-'+fpk
			message.save()
			text = form.cleaned_data['content']
			form = MessageForm()
			return redirect('/chat/'+room_name)

		args = {
			'form': form,
			'text': text,
		}
		return render(request, self.template_name, args)