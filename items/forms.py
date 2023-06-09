from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .widgets import CustomClearableFileInput
from .models import Item, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            "availableDate": DatePickerInput(options={"format": "DD/MM/YYYY"}),
        }
    
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded'
