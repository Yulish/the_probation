from django.contrib import admin

from .models import Users, PerevalAdded, Coords, Image

admin.site.register(Users)
admin.site.register(PerevalAdded)

admin.site.register(Coords)
admin.site.register(Image)

