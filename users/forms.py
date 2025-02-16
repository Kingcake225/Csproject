from django import forms
from django.contrib.auth.models import User # Imports user model
from django.contrib.auth.forms import UserCreationForm # Imports built in user creation form

class UserRegisterForm(UserCreationForm): # Creates a new form 'UserRegisterForm' which inherits from the prebuilt 'UserCreationForm'
    # Adds addition fields to the 'UserCreationForm'
    email = forms.EmailField(required=True) #required=True - user must include an email

    class Meta: # This class gives a nested name space for configurations and keeps them in one place
        model = User # What model will be affected by this form
        fields = ['username', 'email', 'password1', 'password2'] # What fields do we want in form and in what order