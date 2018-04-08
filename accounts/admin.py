from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SchoolUser

# Register your models here.

EXTRA_USER_FIELDS = (
        (None, {'fields': ('is_admin', 'is_teacher', 'is_student', 'is_parent',)}),
    )

class SchoolUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = SchoolUser

class SchoolUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = SchoolUser


class SchoolUserAdmin(UserAdmin):
    form = SchoolUserChangeForm
    add_form = SchoolUserCreationForm
    fieldsets = UserAdmin.fieldsets + EXTRA_USER_FIELDS
    add_fieldsets = UserAdmin.add_fieldsets + EXTRA_USER_FIELDS


admin.site.register(SchoolUser, SchoolUserAdmin)