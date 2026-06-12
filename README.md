🛒 Ecommerce Django
A full-featured Django-based ecommerce web application with product listings, shopping cart, user authentication, and order management.

🌐 Live Demo: https://Alekya26.pythonanywhere.com

✨ Features
🏠 Home page with featured products
🛍️ Product listing and product detail pages
🛒 Shopping cart (add, remove, update items)
💳 Checkout flow
🔐 User registration and login
📦 Order history and order detail pages
🔧 Django admin panel for managing products and orders

🛠️ Tech Stack
Backend: Python, Django
Database: SQLite
Frontend: HTML, CSS (Django Templates)
Deployment: PythonAnywhere

🚀 Getting Started (Run Locally)
1. Clone the repository
bashgit clone https://github.com/alekyamerugumalla-lab/ecommerce_django.git
cd ecommerce_django

2. Create and activate a virtual environment
bash# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate

3. Install dependencies
bashpip install -r requirements.txt

4. Run database migrations
bashcd ecommerce
python manage.py migrate

5. Start the development server
bashpython manage.py runserver

6. Open in browser
http://127.0.0.1:8000

📁 Project Structure
ecommerce_django/
├── ecommerce/
│   ├── ecommerce/          # Django settings, urls, wsgi
│   ├── store/              # Main app (models, views, urls)
│   │   ├── templates/      # HTML templates
│   │   │   └── store/
│   │   │       ├── home.html
│   │   │       ├── product_detail.html
│   │   │       ├── cart.html
│   │   │       ├── checkout.html
│   │   │       ├── login.html
│   │   │       ├── register.html
│   │   │       ├── orders.html
│   │   │       └── order_detail.html
│   ├── manage.py
│   └── db.sqlite3
├── requirements.txt
└── Procfile


👩‍💻 Author
Alekya Merugumalla


GitHub: @alekyamerugumalla-lab
