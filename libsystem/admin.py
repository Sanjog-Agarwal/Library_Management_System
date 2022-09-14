from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Ebook)
# admin.site.register(User_role)
admin.site.register(User)
admin.site.register(HardCopy)