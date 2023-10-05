from django import forms
from django.contrib.admin import widgets

from main.models import Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('message', 'datetime_start', 'datetime_finish', 'clients', 'schedule')
        widgets = {
            'datetime_start': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
            'datetime_finish': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['datetime_start'].widget = widgets.AdminSplitDateTime(forms.SelectDateWidget())
        # self.fields['datetime_finish'].widget = forms.SelectDateWidget()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
