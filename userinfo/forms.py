from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["key", "hash_password","phone"]
        widgets = {
            "hash_password": TextInput(attrs={"size": 80,"type":"password"}),
            "key": Textarea(attrs={"cols": 80, "row": 10}),

        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["key"].widget.attrs['rows'] = 2


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        # del self.fields["username"]

    class Meta:
        model = User
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin"s
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        # del self.fields["username"]

    class Meta:
        model = User
        fields = ("username", "email")
