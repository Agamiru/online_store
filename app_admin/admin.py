from django.contrib import admin
from .models import User

admin.site.site_header = "Sabi Gear Admin"

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')

    def full_name(self, obj):
        return obj.get_full_name()

    def get_queryset(self, request):
        queryset = super(UserAdmin, self).get_queryset(request)
        queryset = queryset.order_by('first_name')
        return queryset


    full_name.short_description = "Full Name:"


admin.site.register(User, UserAdmin)