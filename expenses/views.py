from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta, datetime
from .models import Expense, UserProfile, User
from .forms import SignUpForm, LoginForm, ExpenseForm, UserProfileForm


def signup(request):
    """User signup view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    
    return render(request, 'expenses/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid credentials.')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email.')
    else:
        form = LoginForm()
    
    return render(request, 'expenses/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required(login_url='login')
def home(request):
    """Home/Dashboard view"""
    user = request.user
    today = timezone.now().date()
    
    # Get expenses for today
    today_expenses = Expense.objects.filter(user=user, date=today).order_by('-created_at')
    today_total = today_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get this week's expenses
    start_week = today - timedelta(days=today.weekday())
    week_expenses = Expense.objects.filter(user=user, date__gte=start_week)
    week_total = week_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get this month's expenses
    start_month = today.replace(day=1)
    month_expenses = Expense.objects.filter(user=user, date__gte=start_month)
    month_total = month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get recent expenses (last 30 days)
    recent_start = today - timedelta(days=30)
    recent_expenses = Expense.objects.filter(user=user, date__gte=recent_start).order_by('-date', '-created_at')[:10]
    
    # Get category breakdown for this month
    category_breakdown = month_expenses.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Get frequent items
    frequent_items = Expense.objects.filter(user=user).values('description').annotate(
        count=Sum('id')
    ).order_by('-count')[:5]
    
    context = {
        'today_total': today_total,
        'today_count': today_expenses.count(),
        'week_total': week_total,
        'month_total': month_total,
        'recent_expenses': recent_expenses,
        'category_breakdown': category_breakdown,
        'frequent_items': frequent_items,
    }
    
    return render(request, 'expenses/home.html', context)


@login_required(login_url='login')
def add_expense(request):
    """Add new expense view"""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, f'Expense of {expense.amount} added successfully!')
            
            # If coming from dashboard, redirect back
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ExpenseForm(initial={'date': timezone.now().date()})
    
    return render(request, 'expenses/add_expense.html', {'form': form})


@login_required(login_url='login')
def edit_expense(request, pk):
    """Edit expense view"""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'expenses/edit_expense.html', {'form': form, 'expense': expense})


@login_required(login_url='login')
def delete_expense(request, pk):
    """Delete expense view"""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        amount = expense.amount
        expense.delete()
        messages.success(request, f'Expense of {amount} deleted successfully!')
        return redirect('home')
    
    return render(request, 'expenses/delete_expense.html', {'expense': expense})


@login_required(login_url='login')
def expense_list(request):
    """View all expenses with filters"""
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('-date', '-created_at')
    
    # Filters
    category = request.GET.get('category')
    date_filter = request.GET.get('date_filter', 'all')
    
    if category:
        expenses = expenses.filter(category=category)
    
    # Date filters
    today = timezone.now().date()
    if date_filter == 'today':
        expenses = expenses.filter(date=today)
    elif date_filter == 'week':
        start_week = today - timedelta(days=today.weekday())
        expenses = expenses.filter(date__gte=start_week)
    elif date_filter == 'month':
        start_month = today.replace(day=1)
        expenses = expenses.filter(date__gte=start_month)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(expenses, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_sum = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    categories = [choice[0] for choice in expenses.model._meta.get_field('category').choices]
    
    context = {
        'page_obj': page_obj,
        'total_sum': total_sum,
        'selected_category': category,
        'selected_date_filter': date_filter,
        'categories': categories,
    }
    
    return render(request, 'expenses/expense_list.html', context)


@login_required(login_url='login')
def analytics(request):
    """Analytics and insights view"""
    user = request.user
    today = timezone.now().date()
    
    # Get time period filter
    period = request.GET.get('period', 'month')
    
    if period == 'today':
        expenses = Expense.objects.filter(user=user, date=today)
        period_label = 'Today'
    elif period == 'week':
        start = today - timedelta(days=today.weekday())
        expenses = Expense.objects.filter(user=user, date__gte=start)
        period_label = 'This Week'
    elif period == 'year':
        start = today.replace(month=1, day=1)
        expenses = Expense.objects.filter(user=user, date__gte=start)
        period_label = 'This Year'
    else:  # month
        start = today.replace(day=1)
        expenses = Expense.objects.filter(user=user, date__gte=start)
        period_label = 'This Month'
    
    # Calculate total
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Category breakdown
    category_breakdown = expenses.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Daily breakdown for charts
    daily_breakdown = expenses.values('date').annotate(
        total=Sum('amount')
    ).order_by('date')
    
    # Top expenses
    top_expenses = expenses.order_by('-amount')[:5]
    
    # Frequent items
    frequent_items = Expense.objects.filter(user=user).values('description').annotate(
        count_sum=Sum('id')
    ).order_by('-count_sum')[:5]
    
    # Calculate average
    expense_count = expenses.count()
    average = total / expense_count if expense_count > 0 else 0
    
    context = {
        'period': period,
        'period_label': period_label,
        'total': total,
        'expense_count': expense_count,
        'average': average,
        'category_breakdown': category_breakdown,
        'daily_breakdown': daily_breakdown,
        'top_expenses': top_expenses,
        'frequent_items': frequent_items,
    }
    
    return render(request, 'expenses/analytics.html', context)


@login_required(login_url='login')
def profile(request):
    """User profile view"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=profile)
    
    # Get user statistics
    expenses = Expense.objects.filter(user=request.user)
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_count = expenses.count()
    
    today = timezone.now().date()
    start_month = today.replace(day=1)
    month_expenses = expenses.filter(date__gte=start_month)
    month_total = month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'profile_form': profile_form,
        'profile': profile,
        'total_expenses': total_expenses,
        'total_count': total_count,
        'month_total': month_total,
        'currency': profile.currency,
    }
    
    return render(request, 'expenses/profile.html', context)
