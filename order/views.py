from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class Pay(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pay')


class SaveOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('CloseOrder')


class Detail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detail')
