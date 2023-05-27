from django import forms
from .models import Newsletter

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['first_name', 'email']

    def __init__(self, *args, **kwargs):
        super(NewsletterSubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'