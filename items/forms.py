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




# class ItemForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Field('category', css_class='border-black rounded-0'),
#             Field('name', css_class='border-black rounded-0'),
#             Field('description', css_class='border-black rounded-0'),
#             Field('manufacturer', css_class='border-black rounded-0'),
#             Field('price', css_class='border-black rounded-0'),
#             Field('image_url', css_class='border-black rounded-0'),
#             Field('image', css_class='border-black rounded-0'),
#             Field('availableDate', css_class='border-black rounded-0'),
#             Field('stock', css_class='border-black rounded-0'),
#         )

#     class Meta:
#         model = Item
#         fields = '__all__'
#         widgets = {
#             "availableDate": DatePickerInput(options={"format": "DD/MM/YYYY"}),
#         }
    
#     image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)
