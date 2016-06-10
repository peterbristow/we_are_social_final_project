from django import forms

from .models import ContactRequest


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['contact_name', 'contact_email', 'message']
