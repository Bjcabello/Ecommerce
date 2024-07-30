from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order, OrderProduct, Category
from .forms import UserRegisterForm, PaymentForm
from django.core.paginator import Paginator

def homepage(request):
    images = ['image1.jpg', 'image2.jpg', 'image3.jpg']
    return render(request, 'shop/homepage.html', {'images': images})

def product_list(request):
    search_query = request.GET.get('search')
    category_id = request.GET.get('category')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    else:
        products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'shop/product_list.html', {'products': page_obj, 'categories': categories, 'selected_category': category_id})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    return render(request, 'shop/product_detail.html', {'product': product, 'categories': categories})

@login_required
def cart_detail(request):
    order = Order.objects.filter(user=request.user, is_active=True).first()
    if not order:
        order = Order.objects.create(user=request.user, is_active=True)
    order_products = OrderProduct.objects.filter(order=order)
    order_total = sum(item.product.price * item.quantity for item in order_products)
    order.total = order_total
    order.save()
    context = {
        'order': order,
        'order_products': order_products,
        'order_total': order_total,
    }
    return render(request, 'shop/cart_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, is_active=True)
    order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)
    if not created:
        order_product.quantity += 1
    else:
        order_product.quantity = 1
    order_product.save()
    
    order_total = sum(item.product.price * item.quantity for item in OrderProduct.objects.filter(order=order))
    order.total = order_total
    order.save()
    
    messages.success(request, f"{product.name} se ha añadido al carrito.")
    return redirect('product_list')


@login_required
def checkout(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            if payment_method == 'bank':
                account_number = form.cleaned_data['account_number']
            elif payment_method == 'credit_card':
                credit_card_number = form.cleaned_data['credit_card_number']
                credit_card_expiry = form.cleaned_data['credit_card_expiry']
                credit_card_cvv = form.cleaned_data['credit_card_cvv']
            elif payment_method == 'paypal':
                paypal_email = form.cleaned_data['paypal_email']
            order = Order.objects.get(user=request.user, is_active=True)
            order.is_active = False
            order.save()
            new_order = Order.objects.create(user=request.user, is_active=True)
            messages.success(request, "Compra realizada con éxito.")
            return redirect('order_history')
    else:
        form = PaymentForm()
    return render(request, 'shop/checkout.html', {'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    order_details = []
    for order in orders:
        order_total = 0
        products = []
        order_products = OrderProduct.objects.filter(order=order)
        for order_product in order_products:
            product_total = order_product.product.price * order_product.quantity
            order_total += product_total
            products.append({
                'product': order_product.product,
                'quantity': order_product.quantity,
                'product_total': product_total,
                'order_product_id': order_product.id
            })
        order_details.append({
            'order': order,
            'products': products,
            'order_total': order_total
        })
    context = {
        'order_details': order_details
    }
    return render(request, 'shop/order_history.html', context)

@login_required
def cancel_order(request, order_product_id):
    order_product = get_object_or_404(OrderProduct, id=order_product_id, order__user=request.user)
    order_product.delete()
    messages.success(request, f"{order_product.product.name} ha sido cancelado.")
    return redirect('order_history')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso. ¡Bienvenido!")
            return redirect('homepage')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'registration/logout.html')
    return redirect('homepage')
