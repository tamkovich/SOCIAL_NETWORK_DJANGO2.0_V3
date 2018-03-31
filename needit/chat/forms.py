from django import forms
from chat.models import Message

class MessageForm(forms.ModelForm):
	content = forms.CharField(widget=forms.TextInput(
									attrs={
													'class': 'form-control',
													'placeholder': 'Write a message...'
									}
				))

	class Meta:
		model = Message
		fields = ('content',)