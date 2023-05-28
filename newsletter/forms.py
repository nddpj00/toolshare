from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms
from newsletter.models import Newsletter

class NewsletterSubscriptionForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(label='I agree to the data terms', required=True)

    class Meta:
        model = Newsletter
        fields = ['first_name', 'email', 'agree_to_terms']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('first_name'),
            Field('email'),
            Field('agree_to_terms', wrapper_class='checkbox-field')
        )
