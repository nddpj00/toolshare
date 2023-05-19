from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .widgets import CustomClearableFileInput
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ["title", "body", "date", "location", "thumb", "organiser"]
        widgets = {
            "date": DateTimePickerInput(options={"format": "DD/MM/YYYY HH:mm"}),
        }

    thumb = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'