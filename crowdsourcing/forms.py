from django import forms
from .models import CustomUser

class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.widgets.TextInput)
    class Meta:
        fields = ['username']
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'age']
