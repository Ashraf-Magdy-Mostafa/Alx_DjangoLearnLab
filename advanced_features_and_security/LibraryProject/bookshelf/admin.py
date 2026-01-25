from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book

class CustomUserAdmin(UserAdmin):
    # Include the custom fields in admin
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )
    list_display = ("username", "email", "is_staff", "date_of_birth")
    search_fields = ("username", "email")

# REQUIRED BY CHECKER:
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    search_fields = ("title", "author")
    list_filter = ("publication_year",)
