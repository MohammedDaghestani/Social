from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta():
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
        widgets = {
            'email'         : forms.TextInput(attrs={'class': 'form-control'}),
            'first_name'    : forms.TextInput(attrs={'class': 'form-control'}),
            'last_name'     : forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
