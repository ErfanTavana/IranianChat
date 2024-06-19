from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'پروفایل'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'bio', 'birth_date', 'responsibility', 'phone_number')
    search_fields = ('user__username', 'first_name', 'last_name', 'responsibility')
    list_filter = ('birth_date',)
    fieldsets = (
        (None, {
            'fields': ('user', 'profile_picture', 'first_name', 'last_name', 'bio', 'birth_date', 'responsibility', 'phone_number')
        }),
    )
