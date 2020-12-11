from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomerAuthForm(AuthenticationForm):
    username = forms.EmailField(required=True , label="Email")

class CustomerCreationForm(UserCreationForm):
    
    first_name = forms.CharField(required=True )
    last_name = forms.CharField(required=True )


    def clean_first_name(self):
        value=self.cleaned_data.get('first_name')
        print(value)
        if len(value) < 4 :
            raise ValidationError("First name must be greater than 4 char ")
        else:
            return value 

    def clean_last_name(self):
        value=self.cleaned_data.get('last_name')
        print(value)
        if len(value) < 4 :
            raise ValidationError("Last name must be greater than 4 char ")
        else:
            return value 



    class Meta:
        model =User 
        fields = ['username','first_name','last_name']

