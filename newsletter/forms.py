from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,  Div
from crispy_forms.bootstrap import PrependedText, StrictButton
from newsletter.models import Newsletter

class NewsletterSubscriptionForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        exclude = ('is_registered_already',)


    def __init__(self, *args, **kwargs):
        super(NewsletterSubscriptionForm, self).__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'email': 'Email',
        }


        # self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False

    
