from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from .models import Product, CartItem

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})

def add_to_cart_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def update_cart_view(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    if request.method == 'POST':
        cart_item.quantity = request.POST['quantity']
        cart_item.save()
    return redirect('cart')

def remove_from_cart_view(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def admin_view(request):
    if not request.user.is_staff:
        return redirect('login')
    products = Product.objects.all()
    cart_items = CartItem.objects.all()
    return render(request, 'admin.html', {'products': products, 'cart_items': cart_items})

def add_product_view(request):
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price'],
            image=request.FILES.get('image', None)
        )
        return redirect('admin')
    return render(request, 'add_product.html')

def remove_product_view(request, product_id):
    if not request.user.is_staff:
        return redirect('login')
    product = Product.objects.get(pk=product_id)
    product.delete()
    return redirect('admin')

def update_product_view(request, product_id):
    if not request.user.is_staff:
        return redirect('login')
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        if request.FILES.get('image', None):
            product.image = request.FILES['image']
        product.save()
        return redirect('admin')
    return render(request, 'update_product.html', {'product': product})

def delete_cart_items_view(request):
    CartItem.objects.filter(user=request.user).delete()
    return redirect('
