from typing import Any

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from user_profile import forms, models


class BaseProfile(View):
    template_name = 'user_profile/create.html'

    def setup(self, *args: Any, **kwargs: Any) -> None:
        super().setup(*args, **kwargs)

        if self.request.user.is_authenticated:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None,
                                           user=self.request.user,
                                           instance=self.request.user),
                'profileform': forms.ProfileForm(data=self.request.POST or None)
            }

            self.render = render(self.request, self.template_name, self.context)
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None)
            }

            self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render


class Create(BaseProfile):
    def post(self, *args, **kwargs):
        return self.render


class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('update')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('logout')
