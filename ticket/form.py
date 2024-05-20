from django import forms
from django.contrib.auth import get_user_model

from ticket.models import Ticket

User = get_user_model()

class TicketCreationForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['ticket_title', 'ticket_description']


class AssignTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignTicketForm, self).__init__(*args, **kwargs)
        self.fields['engineer'].queryset = User.objects.filter(is_engineer=True)
    class Meta:
        model = Ticket
        fields = ['engineer']

