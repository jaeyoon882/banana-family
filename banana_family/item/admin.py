from django.contrib import admin
from .models import Category, Item

# Register your models here.

#Category databse table shows up in admin interface
admin.site.register(Category)
admin.site.register(Item)