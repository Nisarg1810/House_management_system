from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional user-specific fields here if needed
    # For example, preferred currency, notification settings, etc.

    def __str__(self):
        return self.user.username


class BudgetItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ITEM_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    item_type = models.CharField(max_length=7, choices=ITEM_TYPES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100, blank=True, null=True)  # e.g., Salary, Groceries

    def __str__(self):
        return f"{self.get_item_type_display()}: {self.description} - {self.amount}"


class InventoryItem(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Household', 'Household'),
        ('Personal Care', 'Personal Care'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., kg, pcs, litre")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    description = models.TextField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Quantity cannot be negative')
        if self.expiry_date and self.expiry_date < timezone.now().date():
            # Optional: warn about expired items
            pass
    
    def __str__(self):
        return f"{self.item_name} ({self.quantity} {self.unit or ''})"
    
    class Meta:
        ordering = ['-date_updated']
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Utilities', 'Utilities'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Healthcare', 'Healthcare'),
        ('Shopping', 'Shopping'),
        ('Repairs', 'Repairs'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - ${self.amount} on {self.date}"
    
    class Meta:
        ordering = ['-date', '-date_created']


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_reminder = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    class Meta:
        ordering = ['date', 'time']


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Budget for {self.month}/{self.year} - ${self.total_budget}"

    class Meta:
        db_table = 'manager_app_budget'
        unique_together = ['user', 'month', 'year']
        ordering = ['-year', '-month']