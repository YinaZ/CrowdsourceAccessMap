from django import forms
from .models import CustomUser

class AuthenticationForm(forms.Form):
    name = forms.CharField(widget=forms.widgets.TextInput)
    class Meta:
        fields = ['name']
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'age']
        # name = forms.CharField(max_length=100)
        # age = forms.IntegerField()
