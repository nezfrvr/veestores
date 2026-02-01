from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from orders.models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    return render(request, "order_history.html", {"orders": orders})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if request.method == 'POST' and cart:
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            quantity = cart.get(str(product.id), 0)
            if quantity > 0:
                Order.objects.create(user=request.user, product=product, quantity=quantity)
        request.session['cart'] = {}
        return render(request, "checkout.html", {"success": True})
    total = 0
    for pid, qty in cart.items():
        try:
            product = Product.objects.get(id=pid)
            total += product.price * qty
        except Product.DoesNotExist:
            continue
    return render(request, "checkout.html", {"total": total})

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
    return render(request, "cart.html", {"cart_items": cart_items, "total": total})

@login_required
def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('/cart/')

def store_home(request):
    products = list(Product.objects.all())
    # Group products into chunks of 5 for the carousel
    product_groups = [products[i:i+5] for i in range(0, len(products), 5)]
    return render(request, "store.html", {"product_groups": product_groups, "products": products})

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('/')
