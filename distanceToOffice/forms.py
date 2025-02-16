from django import forms

class Location(forms.Form):
    address = forms.CharField(
        label='Your Address',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'})
    )
