from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Rescue,RescueMarks,Agency,RescuesInClass,Location
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Rescue)
admin.site.register(RescueMarks)
admin.site.register(Agency)
admin.site.register(RescuesInClass)
admin.site.register(Location)
