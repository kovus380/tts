from django import forms


class TestForm(forms.Form):
    text = forms.CharField(max_length=100, label='', widget=forms.TextInput())