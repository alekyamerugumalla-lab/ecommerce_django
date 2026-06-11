import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, Order, OrderItem


def home(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = Product.objects.filter(category__slug=category_slug, is_active=True)
    else:
        products = Product.objects.filter(is_active=True)
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'active_category': category_slug,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
    })


@login_required
def cart(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart_obj})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    qty = int(request.POST.get('quantity', 1))
    item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product)
    if not created:
        item.quantity += qty
    else:
        item.quantity = qty
    item.save()
    messages.success(request, f'{product.emoji} {product.name} added to cart!')
    next_url = request.POST.get('next', '/')
    return redirect(next_url)


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    qty = int(request.POST.get('quantity', 1))
    if qty < 1:
        item.delete()
    else:
        item.quantity = qty
        item.save()
    return redirect('cart')


@login_required
def checkout(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    if not cart_obj.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    return render(request, 'store/checkout.html', {
        'cart': cart_obj,
        'user': request.user,
    })


@login_required
def place_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    if not cart_obj.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    full_name = request.POST.get('full_name', '').strip()
    address = request.POST.get('address', '').strip()
    phone = request.POST.get('phone', '').strip()

    if not all([full_name, address, phone]):
        messages.error(request, 'Please fill in all shipping details.')
        return redirect('checkout')

    subtotal = cart_obj.get_total()
    shipping = cart_obj.get_shipping()
    total = subtotal + shipping

    order = Order.objects.create(
        user=request.user,
        order_number='ORD' + uuid.uuid4().hex[:8].upper(),
        full_name=full_name,
        address=address,
        phone=phone,
        subtotal=subtotal,
        shipping=shipping,
        total=total,
        status='confirmed',
    )

    for item in cart_obj.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            product_emoji=item.product.emoji,
            price=item.product.price,
            quantity=item.quantity,
        )

    cart_obj.items.all().delete()
    messages.success(request, f'🎉 Order {order.order_number} placed successfully!')
    return redirect('order_detail', order_number=order.order_number)


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': user_orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        if not all([name, email, password]):
            messages.error(request, 'Please fill in all fields.')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            username = email.split('@')[0] + '_' + uuid.uuid4().hex[:4]
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = name.split()[0]
            user.last_name = ' '.join(name.split()[1:])
            user.save()
            login(request, user)
            messages.success(request, f'Welcome, {name}!')
            return redirect('home')
    return render(request, 'store/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        try:
            username = User.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
        except User.DoesNotExist:
            user = None
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')
