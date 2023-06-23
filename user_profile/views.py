from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class Create(View):
    def get(self, *args, **kwargs):
        return HttpResponse('create')


class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('update')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('logout')
