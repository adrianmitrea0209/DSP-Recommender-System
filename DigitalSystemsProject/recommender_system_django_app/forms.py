from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Registration form new users
class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']