from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, PerevalAdded, Coords, Image


admin.site.register(PerevalAdded)

admin.site.register(Coords)
admin.site.register(Image)


class CustomUserAdmin(UserAdmin):

    list_display = ['email', 'fio', 'phone', 'is_active', 'is_staff']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('fio', 'phone')}),  # Эти поля видны, но readonly
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    readonly_fields = ['fio', 'phone']


    search_fields = ['email', 'fio', 'phone']
    ordering = ['email']

admin.site.register(Users, CustomUserAdmin)


# class CustomUserAdmin(UserAdmin):
#
#     list_display = ['email', 'fio', 'phone', 'is_active', 'is_staff']
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Личная информация', {'fields': ('fio', 'phone')}),
#         ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Важные даты', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'fio', 'phone', 'password1', 'password2', 'is_active', 'is_staff'),
#         }),
#     )
#     search_fields = ['email', 'fio', 'phone']
#     ordering = ['email']
#
#     def save_model(self, request, obj, form, change):
#
#         fio = obj.fio.strip() if obj.fio else ''
#         if fio:
#             parts = fio.split(' ', 1)
#             obj.last_name = parts[0] if parts else ''
#             obj.first_name = parts[1] if len(parts) > 1 else ''
#         super().save_model(request, obj, form, change)
#
#
# admin.site.register(Users, CustomUserAdmin)
