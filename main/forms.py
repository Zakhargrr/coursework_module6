from django import forms

from clients.models import Client
from main.models import Mailing, MailingMessage


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(owner=owner)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    class Meta:
        model = Mailing
        fields = ('message', 'datetime_start', 'datetime_finish', 'clients', 'schedule')
        widgets = {
            'datetime_start': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
            'datetime_finish': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'})
        }


class MailingMessageForm(StyleFormMixin, forms.ModelForm):



    class Meta:
        model = MailingMessage
        fields = ('title', 'body')
