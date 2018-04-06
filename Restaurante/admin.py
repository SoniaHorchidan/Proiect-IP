from django.contrib import admin

# Register your models here.
from Restaurante.models import Restaurant, Keyword, UserProfile
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Keyword)
admin.site.register(UserProfile)
