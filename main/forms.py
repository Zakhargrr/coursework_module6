from django import forms

from main.models import Mailing, MailingMessage


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
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingMessageForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


