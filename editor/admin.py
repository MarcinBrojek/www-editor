from django.contrib import admin
from .models import User, Directory, File, FileSection

# Register your models here.

admin.site.register(User)
admin.site.register(Directory)
admin.site.register(File)
admin.site.register(FileSection)
