"""
Run with: python manage.py shell < seed_data.py
Or: python manage.py runscript seed_data  (if django-extensions installed)
"""
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Category, Product

CATEGORIES = [
    {'name': 'Electronics', 'slug': 'electronics'},
    {'name': 'Clothing', 'slug': 'clothing'},
    {'name': 'Books', 'slug': 'books'},
    {'name': 'Home', 'slug': 'home'},
]

PRODUCTS = [
    {'name': 'Wireless Headphones', 'slug': 'wireless-headphones', 'cat': 'electronics', 'price': 2499, 'emoji': '🎧',
     'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80',
     'desc': 'Premium over-ear headphones with active noise cancellation and 30-hour battery life.'},
    {'name': 'Smart Watch', 'slug': 'smart-watch', 'cat': 'electronics', 'price': 3999, 'emoji': '⌚',
     'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&q=80',
     'desc': 'Health & fitness tracker with heart rate, SpO2, GPS, sleep monitoring and 7-day battery life.'},
    {'name': 'Bluetooth Speaker', 'slug': 'bluetooth-speaker', 'cat': 'electronics', 'price': 1499, 'emoji': '🔊',
     'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&q=80',
     'desc': 'Portable waterproof speaker with 360° sound, 12-hour battery, and built-in mic for calls.'},
    {'name': 'Running Shoes', 'slug': 'running-shoes', 'cat': 'clothing', 'price': 1899, 'emoji': '👟',
     'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80',
     'desc': 'Lightweight mesh runners with responsive cushioning, perfect for daily training and long runs.'},
    {'name': 'Linen Shirt', 'slug': 'linen-shirt', 'cat': 'clothing', 'price': 799, 'emoji': '👔',
     'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&q=80',
     'desc': 'Breathable 100% linen shirt, perfect for warm weather. Available in multiple colours.'},
    {'name': 'Python Crash Course', 'slug': 'python-crash-course', 'cat': 'books', 'price': 499, 'emoji': '📗',
     'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&q=80',
     'desc': 'Best-selling beginner programming book covering Python 3 fundamentals with hands-on projects.'},
    {'name': 'The Lean Startup', 'slug': 'the-lean-startup', 'cat': 'books', 'price': 399, 'emoji': '📘',
     'image_url': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&q=80',
     'desc': "Eric Ries' essential guide on building startups using validated learning and rapid iteration."},
    {'name': 'Desk Lamp', 'slug': 'desk-lamp', 'cat': 'home', 'price': 649, 'emoji': '🪔',
     'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&q=80',
     'desc': 'Minimalist LED desk lamp with 3 colour temperatures and USB-C charging port.'},
    {'name': 'Ceramic Mug', 'slug': 'ceramic-mug', 'cat': 'home', 'price': 299, 'emoji': '☕',
     'image_url': 'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400&q=80',
     'desc': 'Handmade 350ml ceramic mug. Microwave and dishwasher safe.'},
]

print("Seeding categories...")
cats = {}
for c in CATEGORIES:
    obj, _ = Category.objects.get_or_create(slug=c['slug'], defaults={'name': c['name']})
    cats[c['slug']] = obj
    print(f"  ✅ {obj.name}")

print("Seeding products...")
for p in PRODUCTS:
    obj, created = Product.objects.get_or_create(slug=p['slug'], defaults={
        'name': p['name'],
        'category': cats[p['cat']],
        'price': p['price'],
        'emoji': p['emoji'],
        'image_url': p['image_url'],
        'description': p['desc'],
        'stock': 50,
    })
    if not created:
        obj.image_url = p['image_url']
        obj.save()
    print(f"  {'✅' if created else '⏭️ '} {obj.name}")

print("\nDone! Seeded", Category.objects.count(), "categories and", Product.objects.count(), "products.")
