from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from crispy_forms.bootstrap import PrependedText, StrictButton
from newsletter.models import Newsletter

class NewsletterSubscriptionForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ['first_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(NewsletterSubscriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                PrependedText('first_name', '<i class="fa fa-user"></i>', placeholder='First Name'),
                PrependedText('email', '<i class="fa fa-envelope"></i>', placeholder='Email'),
                StrictButton('Sign up', type='submit', css_class='btn-secondary btn-sm ml-0 mt-2'),
                css_class='d-flex flex-column'
            )
        )
