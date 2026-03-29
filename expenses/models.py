from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CURRENCY_CHOICES = [
    ('INR', '₹ Indian Rupee'),
    ('USD', '$ US Dollar'),
    ('EUR', '€ Euro'),
    ('GBP', '£ British Pound'),
]

CATEGORY_CHOICES = [
    ('Food', 'Food & Dining'),
    ('Transport', 'Transport'),
    ('Shopping', 'Shopping'),
    ('Entertainment', 'Entertainment'),
    ('Utilities', 'Utilities'),
    ('Healthcare', 'Healthcare'),
    ('Groceries', 'Groceries'),
    ('Other', 'Other'),
]


class UserProfile(models.Model):
    """Extended User Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        ordering = ['-created_at']


class Expense(models.Model):
    """Expense model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['user', '-date']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.description} - {self.amount} {self.user.profile.currency}"

    @classmethod
    def get_today_expenses(cls, user):
        """Get today's expenses for a user"""
        from django.utils import timezone
        from datetime import datetime
        today = timezone.now().date()
        return cls.objects.filter(user=user, date=today)

    @classmethod
    def get_week_expenses(cls, user):
        """Get this week's expenses for a user"""
        from django.utils import timezone
        from datetime import timedelta
        today = timezone.now().date()
        start_week = today - timedelta(days=today.weekday())
        return cls.objects.filter(user=user, date__gte=start_week)

    @classmethod
    def get_month_expenses(cls, user):
        """Get this month's expenses for a user"""
        from django.utils import timezone
        today = timezone.now().date()
        start_month = today.replace(day=1)
        return cls.objects.filter(user=user, date__gte=start_month)

    @classmethod
    def get_category_breakdown(cls, user, time_period='month'):
        """Get category-wise breakdown of expenses"""
        from django.db.models import Sum
        from datetime import timedelta
        from django.utils import timezone
        
        today = timezone.now().date()
        
        if time_period == 'today':
            expenses = cls.get_today_expenses(user)
        elif time_period == 'week':
            expenses = cls.get_week_expenses(user)
        else:  # month
            expenses = cls.get_month_expenses(user)
        
        breakdown = expenses.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        return breakdown

    @classmethod
    def get_frequent_items(cls, user, limit=5):
        """Get most frequent expense descriptions"""
        from django.db.models import Count
        return cls.objects.filter(user=user).values('description').annotate(
            count=Count('id')
        ).order_by('-count')[:limit]
