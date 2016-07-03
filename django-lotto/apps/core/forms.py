from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from registration.forms import RegistrationForm
User = get_user_model()

class RegistrationFormExtra(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` to add in extra fields from the user model
    """

    class Meta(UserCreationForm.Meta):
        fields = [
            'first_name',
            'last_name',
            User.USERNAME_FIELD,
            'email',
            'password1',
            'password2'
        ]
        required_css_class = 'required'
