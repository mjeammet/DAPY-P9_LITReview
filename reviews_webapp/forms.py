from django import forms
from django.core.exceptions import ValidationError

from authentication.models import User

class SubscriptionForm(forms.Form):
    username = forms.CharField(max_length=30, initial='Nom d\'utilisateur', required=False)
    # username = forms.IntegerField()

    def is_existing_user(self):
        queryset = User.objects.filter(username = self.username)
        if len(queryset) != 1:
            raise ValidationError("Utilisateur introuvable")
        else:
            return True