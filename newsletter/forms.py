from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import PrependedText, StrictButton
from newsletter.models import Newsletter

class NewsletterSubscriptionForm(forms.ModelForm):
    agree_terms = forms.BooleanField(label='I agree to the data terms', required=True)

    class Meta:
        model = Newsletter
        fields = ['first_name', 'email', 'agree_terms']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(NewsletterSubscriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'd-none'
        self.helper.layout = Layout(
            PrependedText('first_name', '<i class="fa fa-user"></i>', placeholder='First Name'),
            PrependedText('email', '<i class="fa fa-envelope"></i>', placeholder='Email'),
            'agree_terms',
            StrictButton('Submit', type='submit', css_class='btn-primary')
        )