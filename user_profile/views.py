from copy import deepcopy
from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from user_profile import forms, models


class BaseProfile(View):
    template_name = 'user_profile/create.html'

    def setup(self, *args: Any, **kwargs: Any) -> None:
        super().setup(*args, **kwargs)

        self.cart = deepcopy(self.request.session.get('cart', {}))

        self.profile = None

        if self.request.user.is_authenticated:

            self.profile = models.UserProfile.objects.filter(
                user=self.request.user).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile)
            }

        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None)
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'user_profile/update.html'

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render


class Create(BaseProfile):
    def post(self, *args, **kwargs):

        if not self.userform.is_valid() or not self.profileform.is_valid():
            messages.error(
                self.request,
                'Register form with errors, please review it.'
            )
            return self.render

        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            user = get_object_or_404(
                User, username=self.request.user.username)  # type: ignore

            if password:
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if not self.profile:
                self.profileform.cleaned_data['user'] = user
                profile = models.UserProfile(**self.profileform.cleaned_data)
                profile.save()
            else:
                profile = self.profileform.save(commit=False)
                profile.user = user
                profile.save()

        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()

        if password:
            auth = authenticate(self.request, username=user, password=password)

            if auth:
                login(self.request, user=user)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(self.request, 'Success: Create or Update register.')

        return redirect('product:cart')


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Invalid: username or password.'
            )
            return redirect('user_profile:create')

        user = authenticate(
            self.request, username=username, password=password
        )

        if not user:
            messages.error(
                self.request,
                'Invalid: username or password.'
            )
            return redirect('user_profile:create')

        login(self.request, user=user)

        messages.success(
            self.request,
            'Success: Logged.'
        )

        return redirect('product:cart')


class Logout(View):
    def get(self, *args, **kwargs):
        cart = deepcopy(self.request.session.get('cart'))

        logout(self.request)

        self.request.session['cart'] = cart
        self.request.session.save()

        return redirect('product:list')
