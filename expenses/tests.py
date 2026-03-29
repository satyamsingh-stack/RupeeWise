from django.test import TestCase
from django.contrib.auth.models import User
from .models import Expense, UserProfile, CATEGORY_CHOICES, CURRENCY_CHOICES
from datetime import datetime, timedelta
from decimal import Decimal


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_creation(self):
        """Test that a profile is created with a user"""
        profile = UserProfile.objects.create(user=self.user, currency='INR')
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.currency, 'INR')
    
    def test_profile_string_representation(self):
        """Test profile __str__ method"""
        profile = UserProfile.objects.create(user=self.user, currency='INR')
        self.assertEqual(str(profile), "testuser's Profile")
    
    def test_currency_choices(self):
        """Test that all currency options are valid"""
        valid_currencies = ['INR', 'USD', 'EUR', 'GBP']
        profile = UserProfile.objects.create(user=self.user, currency='INR')
        for currency in valid_currencies:
            profile.currency = currency
            profile.save()
            self.assertEqual(profile.currency, currency)


class ExpenseModelTest(TestCase):
    """Test cases for Expense model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(user=self.user, currency='INR')
    
    def test_expense_creation(self):
        """Test creating an expense"""
        expense = Expense.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            category='Food',
            description='Chai',
            date=datetime.now().date()
        )
        self.assertEqual(expense.user, self.user)
        self.assertEqual(expense.amount, Decimal('50.00'))
        self.assertEqual(expense.category, 'Food')
    
    def test_expense_string_representation(self):
        """Test expense __str__ method"""
        expense = Expense.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            category='Food',
            description='Chai',
            date=datetime.now().date()
        )
        expected = f"Chai - 50.00 INR"
        self.assertEqual(str(expense), expected)
    
    def test_get_today_expenses(self):
        """Test get_today_expenses class method"""
        today = datetime.now().date()
        Expense.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            category='Food',
            description='Chai',
            date=today
        )
        Expense.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            category='Transport',
            description='Bus',
            date=today - timedelta(days=1)
        )
        today_expenses = Expense.get_today_expenses(self.user)
        self.assertEqual(today_expenses.count(), 1)
        self.assertEqual(today_expenses[0].description, 'Chai')
    
    def test_get_category_breakdown(self):
        """Test category breakdown calculation"""
        today = datetime.now().date()
        Expense.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            category='Food',
            description='Chai',
            date=today
        )
        Expense.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            category='Food',
            description='Lunch',
            date=today
        )
        Expense.objects.create(
            user=self.user,
            amount=Decimal('20.00'),
            category='Transport',
            description='Bus',
            date=today
        )
        breakdown = Expense.get_category_breakdown(self.user, time_period='month')
        self.assertEqual(len(breakdown), 2)
        self.assertEqual(breakdown[0]['category'], 'Food')
        self.assertEqual(breakdown[0]['total'], Decimal('150.00'))


class ViewsTest(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(user=self.user, currency='INR')
    
    def test_login_page_loads(self):
        """Test that login page loads"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/login.html')
    
    def test_signup_page_loads(self):
        """Test that signup page loads"""
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/signup.html')
    
    def test_home_requires_login(self):
        """Test that home page requires login"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_home_page_loads_when_authenticated(self):
        """Test that home page loads when user is logged in"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/home.html')
    
    def test_add_expense_page_loads(self):
        """Test that add expense page loads"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/add_expense.html')
