# 🚀 RupeeWise Django - Quick Start Guide

**Get RupeeWise running in 5 minutes!**

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd rupeewise
pip install -r requirements.txt
```

### Step 2: Set Up Database
```bash
python manage.py migrate
```

### Step 3: Create Admin Account
```bash
python manage.py createsuperuser
```
Enter your email and password when prompted.

### Step 4: Start Server
```bash
python manage.py runserver
```

### Step 5: Access Application
- **Main App**: http://localhost:8000
- **Admin**: http://localhost:8000/admin/

✅ **Done!** You now have RupeeWise running!

---

## 📱 First Time Usage

### 1. **Create Your Account**
- Go to http://localhost:8000/signup/
- Enter your name, email, and password
- Click "Sign Up"

### 2. **Add Your First Expense**
- Click "Add Expense" button
- Enter amount, category, description, date
- Click "Add Expense"

### 3. **View Dashboard**
- See today's, week's, and month's statistics
- Check recent expenses
- View category breakdown

### 4. **Explore Analytics**
- Click "Analytics" to see spending trends
- View pie charts and line graphs
- Check top expenses and frequent items

### 5. **Check Settings**
- Click on your username
- Click "Profile"
- Update currency preference
- View account statistics

---

## 🔧 Useful Commands

### Reset Password
```bash
python manage.py changepassword username
```

### View Database Content
```bash
python manage.py dbshell
```

### Clear All Data (WARNING!)
```bash
python manage.py flush
```

### Run Tests
```bash
python manage.py test
```

### Check Django Version
```bash
python manage.py --version
```

---

## 🌐 Access Points

| URL | Purpose | Login Required |
|-----|---------|----------------|
| `/` | Dashboard | ✅ Yes |
| `/signup/` | Register | ❌ No |
| `/login/` | Login | ❌ No |
| `/logout/` | Logout | ✅ Yes |
| `/add/` | Add Expense | ✅ Yes |
| `/expenses/` | View All | ✅ Yes |
| `/analytics/` | Analytics | ✅ Yes |
| `/profile/` | Settings | ✅ Yes |
| `/admin/` | Admin Panel | ✅ Yes (Admin Only) |

---

## 💡 Pro Tips

### 1. **Use Frequent Items**
Add expenses you make regularly, and they'll appear in "Frequent Items" for quick adding.

### 2. **Filter Expenses**
On the "All Expenses" page, filter by category and date range to find specific transactions.

### 3. **Check Analytics**
Use different time periods (Today, Week, Month, Year) to see spending patterns.

### 4. **Export Data**
All data is in `db.sqlite3` - you can backup and export anytime.

### 5. **Admin Panel**
For bulk operations, use `/admin/` to manage expenses directly.

---

## 🐛 Quick Troubleshooting

### Port 8000 in Use
```bash
python manage.py runserver 8001
```

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

### Database Issues
```bash
python manage.py migrate --run-syncdb
```

### Can't Login
```bash
python manage.py changepassword your_username
```

---

## 📊 Example Workflow

### Monday - Add Expenses
1. Add ₹50 Chai (Food)
2. Add ₹30 Bus (Transport)
3. Add ₹100 Groceries (Groceries)

### Wednesday - Check Dashboard
1. See today's total: ₹0 (no expenses today)
2. See week's total: ₹180
3. See category breakdown: Food (₹150), Transport (₹30)

### Friday - View Analytics
1. Click Analytics → This Month
2. See pie chart of categories
3. See daily spending trend
4. Check top 5 expenses

### Weekend - Plan Budget
1. Check total spent so far
2. Set budget for next month
3. Identify high spending categories
4. Plan to reduce spending

---

## 🎯 Features Overview

### Dashboard
- ✅ Quick statistics (today, week, month)
- ✅ Recent expenses list
- ✅ Category breakdown
- ✅ Frequent items
- ✅ Quick "Add Expense" button

### Expense Management
- ✅ Add new expenses
- ✅ Edit existing expenses
- ✅ Delete expenses with confirmation
- ✅ View all expenses with pagination
- ✅ Filter by category and date

### Analytics
- ✅ Pie chart (category breakdown)
- ✅ Line chart (daily trends)
- ✅ Total spending summary
- ✅ Top expenses list
- ✅ Average spending calculation
- ✅ Frequent items list

### Account Management
- ✅ User registration
- ✅ Secure login/logout
- ✅ Profile view
- ✅ Currency preference
- ✅ Account statistics
- ✅ Password management

### Admin Features
- ✅ User management
- ✅ Expense management
- ✅ Advanced filtering
- ✅ Bulk actions
- ✅ Search capabilities
- ✅ Data export

---

## 📚 Documentation

For detailed information, see:
- **Full Docs**: `rupeewise/README.md`
- **Conversion Guide**: `README_DJANGO.md`
- **This Guide**: `QUICKSTART_DJANGO.md`

---

## 🚀 Next Steps

1. ✅ Complete 5-minute setup
2. ✅ Create your account
3. ✅ Add 5-10 expenses
4. ✅ Explore all pages
5. ✅ Check analytics
6. ✅ Customize profile
7. ✅ Bookmark important pages!

---

## 🆘 Need Help?

### View App Logs
```bash
# Server logs show in terminal while running
# Check for any error messages
```

### Common Issues

**Q: Can't login?**
A: Make sure you created a superuser with `python manage.py createsuperuser`

**Q: 404 Page Not Found?**
A: Check the URL - use `/` not `/home/`

**Q: Database locked?**
A: Django uses SQLite which can have locking issues. Restart the server.

**Q: Static files not loading?**
A: In development, Django serves them automatically. In production, run `python manage.py collectstatic`

---

## ✨ Have Fun!

Now you have a fully functional expense tracking application!

Track every rupee. Understand your spending. Master your money. 💰

**Happy tracking!**

---

*Last Updated: March 2026*
*Version: 1.0.0*
