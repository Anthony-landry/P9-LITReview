from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms

from blog.models import Ticket


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        fields = ('username', 'email', 'password1', 'password2')
        error_messages = {
            'username': {
                'blank': _("Veuillez renseigner un nom d'utilisateur."),
                'max_length': _("Ce nom d'utilisateur est trop long."),
            },
        }

        labels = {
            "first_name": "Prénom",
            "last_name": "Nom"
        }

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['username'].required = True
        self.fields['email'].label = "Adresse e-mail"
        self.fields['email'].required = True
        self.fields['password1'].label = "Mot de passe"
        self.fields['password1'].required = True
        self.fields['password2'].label = "Confirmation du mot de passe"
        self.fields['password2'].required = True


class UserLoginForm(AuthenticationForm):
    # username= forms.CharField(max_length=100,
    #                        widget= forms.TextInput
    #                        (attrs={'placeholder':'Enter your first name'}))
    # email= forms.CharField(max_length=100,
    #                        widget= forms.EmailInput
    #                        (attrs={'placeholder':'Enter your email'}))
    class Meta:
        model = User
        fields = '__all__'
        error_messages = {
            'username': {
                'blank': _("Veuillez renseigner un nom d'utilisateur."),
                'max_length': _("Ce nom d'utilisateur est trop long."),
            },
            'password': {
                'blank': _("Veuillez renseigner un mot de passe."),
                'max_length': _("Ce mot de passe est trop long."),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password'].label = "Mot de passe"


class UpdateTicketForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "d-flex flex-shrink-1",
                                                          "style": "margin-bottom: 2rem;display:\
                                                           flex;width: 62.5em;padding: 10px;"}),
                            label="Titre")

    description = forms.CharField(
        widget=forms.TextInput(attrs={"class": "border-primary focus-ring form-control-lg d-flex flex-shrink-1",
                                      "style": "display: flex;position: relative;padding-right: \
                                      0px;margin-bottom: 4px;margin-right: 6px;width: 50em;height: 20em;"}),
        label="Description")

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
