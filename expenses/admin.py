from django.contrib import admin
from .models import Expense, UserProfile

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'description', 'date', 'created_at')
    list_filter = ('category', 'date', 'user')
    search_fields = ('description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'created_at')
    list_filter = ('currency',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
