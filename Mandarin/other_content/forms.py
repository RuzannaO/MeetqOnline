
from django import forms
from .models import ContactUsMassage


class ContactUsMassageForm(forms.ModelForm):
    class Meta:
        model = ContactUsMassage
        fields = ['full_name', 'email', 'phone_number', 'massage_text']