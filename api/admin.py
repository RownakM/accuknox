from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'last_login',
        'is_superuser',
        'email',
        'bio',
        'date_of_birth',
        'location',
        'website',
        'created_at',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'date_of_birth',
        'created_at',
    )
    raw_id_fields = ('followers', 'following')
    date_hierarchy = 'created_at'
