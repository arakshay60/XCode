from django.forms import ModelForm
from django import forms
from Users.models import User
from django.contrib.auth.forms import  UserCreationForm

class RegForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password1','password2']
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError('This email address is already taken.')
        except User.DoesNotExist:
            return email
        

class ProfForm(ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','profile_picture']