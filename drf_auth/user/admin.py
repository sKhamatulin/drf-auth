from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',
                    'first_name', 'last_name',
                    'contactId', 'is_staff')
    list_filter = ('is_staff', 'is_active')


admin.site.register(CustomUser, CustomUserAdmin)