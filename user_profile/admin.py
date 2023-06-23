from django.contrib import admin

from user_profile import models


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'age', 'city', 'state')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user', 'birthday', 'cpf', 'address',
                     'neighborhood', 'city', 'state')
    ordering = ('-id',)
    list_filter = ('id',)
    list_editable = ('age', 'city', 'state')
