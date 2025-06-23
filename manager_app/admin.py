from django.contrib import admin
from .models import InventoryItem, Expense, Event, Budget

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'quantity', 'category', 'user', 'date_updated']
    list_filter = ['category', 'date_added']
    search_fields = ['item_name', 'description']
    ordering = ['-date_updated']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'category', 'date', 'user']
    list_filter = ['category', 'date', 'date_created']
    search_fields = ['title', 'description']
    ordering = ['-date']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'user']
    list_filter = ['date', 'date_created']
    search_fields = ['title', 'description']
    ordering = ['date']

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_budget', 'month', 'year']
    list_filter = ['year', 'month']
    ordering = ['-year', '-month']