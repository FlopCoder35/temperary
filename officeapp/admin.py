from django.contrib import admin
from .models import Member,Role,Department
# Register your models here.
admin.site.register(Member)
admin.site.register(Role)
admin.site.register(Department)