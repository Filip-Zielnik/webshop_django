from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from django_countries.widgets import CountrySelectWidget

from .models import Address, Comment, Profile


class FormCleanMixin(ModelForm):
    """ Checks if the user is at least 18 years old. """
    def clean(self):
        super(FormCleanMixin, self).clean()
        birth_date = self.cleaned_data.get('birth_date')
        user_age = (date.today() - birth_date).days / 365
        if user_age < 18:
            self._errors['birth_date'] = self.error_class(
                ['Musisz mieć co najmniej 18 lat żeby się zarejestrować!']
            )
        return self.cleaned_data


class LoginForm(forms.Form):
    """ Login form. """
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    """ Registration form, based on build-in django user model. """
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Imię', required=False)
    last_name = forms.CharField(label='Nazwisko', required=False)
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')


class ProfileForm(FormCleanMixin):
    """ Registration form, extends build-in django user model (Profile model). """
    birth_date = forms.DateField(
        label='Data urodzin',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
    )

    class Meta:
        model = Profile
        fields = ('birth_date',)


class UpdateUserForm(forms.ModelForm):
    """ Updates user's data from build-in django user model. """
    username = forms.CharField(label='Nazwa użytkownika')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {'username': 'Nazwa użytkownika',
                  'first_name': 'Imię',
                  'last_name': 'Nazwisko',
                  'email': 'Email',
                  }


class UpdateProfileForm(FormCleanMixin):
    """ Updates user's data from EXTENDED user model (Profile model). """
    class Meta:
        model = Profile
        fields = ('birth_date',)
        labels = {'birth_date': 'Data urodzin'}
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'})}


class ChangePasswordForm(forms.ModelForm):
    """ Form to change password. """
    password = forms.CharField(widget=forms.PasswordInput, label='Nowe hasło')

    class Meta:
        model = User
        fields = ('password',)


class AddAddressForm(forms.ModelForm):
    """ Form to add and modifie address. """
    class Meta:
        model = Address
        fields = ('name', 'country', 'city', 'address', 'zip_code')
        labels = {
            'name': 'Nazwa',
            'country': 'Kraj',
            'city': 'Miasto',
            'address': 'Adres',
            'zip_code': 'Kod pocztowy',

        }
        widgets = {'country': CountrySelectWidget()}


class AddCommentForm(forms.ModelForm):
    """ Comment form. """
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': ''}
