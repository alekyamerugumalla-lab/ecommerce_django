# ShopDemo — Django E-commerce Store

A simple e-commerce web application built with Django (Python) and SQLite.

## Features
- Product listings with category filter
- Product detail page with quantity selector
- Shopping cart (add, update, remove items)
- User registration and login
- Checkout with shipping details
- Order history and order detail pages
- Django admin panel to manage products, orders, users

## Requirements
- Python 3.10+
- pip

## Setup & Run

### 1. Install dependencies
```bash
pip install django pillow
```

### 2. Run database migrations
```bash
python manage.py migrate
```

### 3. Seed sample products
```bash
python seed_data.py
```

### 4. Create an admin user (optional)
```bash
python manage.py createsuperuser
```
Or use the pre-created one:
- Username: `admin`
- Password: `admin123`

### 5. Start the development server
```bash
python manage.py runserver
```

### 6. Open in browser
- Store: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Project Structure
```
ecommerce/
├── manage.py
├── seed_data.py          # Run once to populate products
├── db.sqlite3            # Auto-created after migrate
├── ecommerce/            # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── store/                # Main app
    ├── models.py         # Category, Product, Cart, Order, etc.
    ├── views.py          # All page views
    ├── urls.py           # URL routing
    ├── admin.py          # Admin panel config
    ├── context_processors.py
    └── templates/store/  # HTML templates
        ├── base.html
        ├── home.html
        ├── product_detail.html
        ├── cart.html
        ├── checkout.html
        ├── orders.html
        ├── order_detail.html
        ├── login.html
        └── register.html
```

## Database Models
| Model | Description |
|-------|-------------|
| Category | Product categories (Electronics, Books, etc.) |
| Product | Products with name, price, emoji, stock |
| Cart | One cart per logged-in user |
| CartItem | Individual items in a cart |
| Order | Placed orders with shipping info |
| OrderItem | Snapshot of each product in an order |
