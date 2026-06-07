from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket, Comment


class TicketForm(forms.ModelForm):
    class Meta:
        model  = Ticket
        fields = ['title', 'description', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Short title for the issue'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
                'placeholder': 'Describe the problem in detail'
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }


class TicketUpdateForm(forms.ModelForm):
    """For staff/admin: can also change status and assignment."""
    class Meta:
        model  = Ticket
        fields = ['title', 'description', 'priority', 'status', 'assigned_to']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority':    forms.Select(attrs={'class': 'form-control'}),
            'status':      forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Write a comment...'
            }),
        }
        labels = {'body': 'Add a Comment'}


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'