from typing import Any, Dict

from django import forms
from django.contrib.auth.models import User

from user_profile import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ('user',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirm Password'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password', 'password2')

    def clean(self) -> Dict[str, Any]:
        data = self.data
        cleaned_data = self.cleaned_data

        validation_error_msgs = {}

        user_data = cleaned_data.get('username')
        password_data = cleaned_data.get('password')
        password2_data = cleaned_data.get('password2')
        email_data = cleaned_data.get('email')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'User already exists.'
        error_msg_email_exists = 'Email Already exists.'
        error_msg_password_match = 'Passwords do not match.'
        error_msg_password_short = 'Minimun 6 characters.'

        if self.user:
            if user_db:
                if user_data != user_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short

                if len(password2_data) < 6:
                    validation_error_msgs['password2'] = error_msg_password_short
        else:
            ...

        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs, code='invalid'))

        return super().clean()
