from django import forms
from . models import StreamPost

class StreamPostForm(forms.ModelForm):
    class Meta:
        model = StreamPost
        fields =['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'stream-title',
                'required': True,
                'placeholder': 'Title...'
                }),
            'description': forms.TextInput(attrs={
                'id': 'stream-description',
                'required': True,
                'placeholder': "Describe what you'll be streaming..."
                })
        }
