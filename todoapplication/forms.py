from django import forms
from django.contrib.auth.models import User 
from todoapplication.models import Todo
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegistrationForm(UserCreationForm ):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password1','password2']
        # widgets={
        #     'password':forms.PasswordInput(attrs={'class':'form-control'})
        # }
class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['task_name']
        widgets={
            'task_name':forms.TextInput(attrs={'class':'form-control'})
        }
class TodoEditForm(forms.ModelForm):
    class Meta:
        model=Todo
        exclude=('user',)

