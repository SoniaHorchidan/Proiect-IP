from django.contrib import admin

# Register your models here.
from Restaurante.models import Restaurant, Keyword, Profile
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Keyword)
admin.site.register(Profile)
