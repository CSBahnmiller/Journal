from django.contrib import admin
from .models import UserContent, User, Comments

# Register your models here.
#admin.site.register(User)

class UserContentAdmin(admin.ModelAdmin):
  readonly_fields = ('id',)


admin.site.register(UserContent, UserContentAdmin)
admin.site.register(Comments)