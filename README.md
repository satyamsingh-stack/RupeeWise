# 💰 RupeeWise - Django Edition

**Track every rupee. Understand your spending. Master your money.**

RupeeWise is a beautiful, fast web application for tracking micro daily expenses. Built with Django + SQLite3 for a lightweight, easy-to-deploy solution.

## ✨ Features

### ⚡ Core Functionality
- **User Authentication** - Secure signup and login with Django auth
- **Expense Tracking** - Add, edit, delete expenses with categories
- **Smart Analytics** - View spending trends, category breakdown, insights
- **Daily Dashboard** - See today's, this week's, and this month's spending at a glance
- **Advanced Filtering** - Filter by category and date range
- **Favorite Items** - Track frequently used expense items
- **Multi-Currency Support** - Choose your default currency (INR, USD, EUR, GBP)

### 🎨 Beautiful UI
- Modern, minimal design with Bootstrap 5
- Responsive mobile-friendly interface
- Interactive charts and analytics
- Smooth animations and transitions
- Dark-mode ready

### 🔐 Security
- Django built-in authentication
- CSRF protection
- Secure session handling
- Password hashing with bcrypt

---

## 🛠️ Tech Stack

- **Framework**: Django 4.2
- **Database**: SQLite3 (included with Django)
- **Frontend**: HTML5 + Bootstrap 5 + Chart.js
- **Server**: Gunicorn (production)
- **Language**: Python 3.8+

---

## 📋 Project Structure

```
rupeewise/
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── db.sqlite3                 # SQLite database (auto-created)
├── rupeewise/                 # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI config for servers
│   └── __init__.py
├── expenses/                 # Main app
│   ├── models.py             # Database models (Expense, UserProfile)
│   ├── views.py              # View logic
│   ├── forms.py              # Django forms
│   ├── urls.py               # App URLs
│   ├── admin.py              # Admin interface
│   ├── apps.py
│   └── __init__.py
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   └── expenses/
│       ├── login.html
│       ├── signup.html
│       ├── home.html
│       ├── add_expense.html
│       ├── edit_expense.html
│       ├── delete_expense.html
│       ├── expense_list.html
│       ├── analytics.html
│       └── profile.html
├── static/                   # Static files (CSS, JS, images)
└── media/                    # User uploads
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd rupeewise
pip install -r requirements.txt
```

### 2. Apply Database Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Then enter your email and password.

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

### 5. Access Admin Panel

Go to `http://localhost:8000/admin/` and login with your superuser credentials.

---

## 📱 Usage

### For Regular Users

1. **Sign Up** - Create a new account with email and password
2. **Add Expenses** - Click "Add Expense" to log spending
3. **View Dashboard** - See today's, week's, and month's totals
4. **Analytics** - Check spending trends and category breakdown
5. **Manage Profile** - Update preferences and view statistics

### For Admin Users

1. Login to `http://localhost:8000/admin/`
2. Manage users and expenses
3. View analytics for all users
4. Manage site configuration

---

## 🔧 Configuration

### Settings File (`rupeewise/settings.py`)

Key settings you might want to customize:

```python
# Change time zone
TIME_ZONE = 'Asia/Kolkata'  # Change to your timezone

# Debug mode (set to False in production)
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['*']  # Add your domain in production

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

---

## 📦 Database Models

### User Profile
- One-to-one relationship with Django User
- Stores default currency preference
- Timestamps for creation and updates

### Expense
- ForeignKey to User (linked to each user's profile)
- Fields: amount, category, description, date
- Indexes on date and user for fast queries
- Methods for analytics (daily, weekly, monthly totals)

---

## 🌟 API-like Views

Even though this is a web app, views are structured for easy data retrieval:

- `/` - Home/Dashboard
- `/add/` - Add new expense
- `/expense/<id>/edit/` - Edit expense
- `/expense/<id>/delete/` - Delete expense
- `/expenses/` - List all expenses
- `/analytics/` - Spending analytics
- `/profile/` - User profile and settings
- `/signup/` - User registration
- `/login/` - User login
- `/logout/` - User logout

---

## 🔍 Admin Interface

Access admin at `/admin/`:

- View and manage Expense records
- View and manage User Profiles
- Filter by category, date, user
- Search by description
- Bulk actions support

---

## 🚢 Deployment

### Deploy to Heroku

```bash
# Install Heroku CLI
# Then:
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev

# Set production settings
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key

git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy to PythonAnywhere

1. Upload your project
2. Create a virtual environment
3. Install dependencies
4. Configure web app settings
5. Reload web app

### Deploy to Railway

```bash
railway connect
railway up
```

---

## 📊 Data Export

All expense data is stored in SQLite3. To export:

```bash
# Backup database
cp db.sqlite3 db.sqlite3.backup

# Export as JSON
python manage.py dumpdata expenses > expenses_data.json

# Export as CSV (manual query needed)
# Or use Django admin export feature
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001  # Use different port
```

### Database Issues
```bash
# Reset database (WARNING: Deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

---

## 📝 Common Commands

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Make migrations
python manage.py makemigrations

# Run tests
python manage.py test

# Shell access
python manage.py shell

# Collect static files
python manage.py collectstatic

# Create app
python manage.py startapp app_name

# Clear database (be careful!)
python manage.py flush
```

---

## 🔐 Security Tips

1. **Never** commit `db.sqlite3` to version control
2. **Never** commit `settings.py` with real `SECRET_KEY`
3. Set `DEBUG = False` in production
4. Use environment variables for sensitive data
5. Set `ALLOWED_HOSTS` to your domain in production
6. Use HTTPS in production
7. Regularly backup your database

---

## 📈 Performance

SQLite3 is perfect for:
- Small to medium applications
- Single-server deployments
- Low to medium traffic
- Development and testing

For scaling, consider PostgreSQL or MySQL.

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

---

## 📄 License

MIT License - feel free to use this project.

---

## 📞 Support

- **Documentation**: See this README
- **Issues**: Report on GitHub
- **Questions**: Contact via email

---

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] REST API for mobile integration
- [ ] Budget alerts
- [ ] Recurring expenses
- [ ] Receipt scanner (OCR)
- [ ] Data export (CSV, PDF)
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Spending goals

---

## 🙏 Acknowledgments

- Django Framework
- Bootstrap 5
- Chart.js for visualizations
- Open source community

---

**Happy tracking! Track every rupee. 💰**

*Version 1.0.0 - March 2026*
