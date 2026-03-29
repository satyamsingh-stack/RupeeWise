#!/usr/bin/env python
"""
RupeeWise Django Setup Script
This script helps set up the Django project quickly.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and report the result"""
    print(f"\n{'=' * 60}")
    print(f"📦 {description}")
    print(f"{'=' * 60}")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with error code {e.returncode}")
        return False

def main():
    print("""
    
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║            💰 RupeeWise - Django Setup                    ║
    ║                                                            ║
    ║    Track every rupee. Understand your spending.           ║
    ║    Master your money.                                     ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Install dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("\n❌ Failed to install dependencies")
        sys.exit(1)
    
    # Step 2: Apply migrations
    if not run_command(
        f"{sys.executable} manage.py migrate",
        "Applying database migrations"
    ):
        print("\n❌ Failed to apply migrations")
        sys.exit(1)
    
    # Step 3: Collect static files
    if not run_command(
        f"{sys.executable} manage.py collectstatic --noinput",
        "Collecting static files"
    ):
        print("\n⚠ Warning: Failed to collect static files (non-critical)")
    
    print(f"\n{'=' * 60}")
    print("✅ Setup completed successfully!")
    print(f"{'=' * 60}")
    
    print("""
    
    🎉 RupeeWise is ready! Next steps:
    
    1. Create a superuser account:
       python manage.py createsuperuser
    
    2. Run the development server:
       python manage.py runserver
    
    3. Open your browser and go to:
       http://localhost:8000
    
    4. Login with the account you just created
    
    5. Access the admin panel at:
       http://localhost:8000/admin/
    
    ✨ Happy tracking!
    
    """)

if __name__ == '__main__':
    main()
