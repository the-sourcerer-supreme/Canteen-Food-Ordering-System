from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Order,Customer
from .models import Product

def home(request):
    return render(request, 'store/home.html')

def login_view(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        password = request.POST["password"]
        user = authenticate(username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            return render(request, "store/login.html", {"error": "Invalid phone number or password"})
    return render(request, "store/login.html")

@login_required
def store(request):
    user = request.user

    # Handle users who don't have a customer profile
    customer, created = Customer.objects.get_or_create(user=user)

    return render(request, 'store/store.html', {'customer': customer})

def store(request):
    products = Product.objects.all()
    for product in products:
        product.avg_rating = product.avg_rating()  # Dynamically set avg_rating
    return render(request, 'store/store.html', {'products': products})


def signup_view(request):
    if request.method == "POST":
        name = request.POST["name"]
        surname = request.POST["surname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            return render(request, "store/signup.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=phone).exists():
            return render(request, "store/signup.html", {"error": "Phone number already registered"})

        user = User.objects.create_user(username=phone, email=email, password=password1, first_name=name, last_name=surname)
        user.save()
        return redirect("login")

    return render(request, "store/signup.html")

def logout_view(request):
    logout(request)
    return redirect("home")


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # Vendor's predefined billing details
        billing_info = {
            "address": "Vendor Address, XYZ Street",
            "city": "Vendor City",
            "state": "Vendor State",
            "zipcode": "123456",
            "country": "Vendor Country"
        }
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}  # Empty order for guests
        billing_info = {}  # No billing info for guests

    context = {'order': order, 'billing_info': billing_info}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def confirm_payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.payment_confirmed = True
    order.save()
    return JsonResponse({'message': 'Payment confirmed'})

def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.payment_confirmed = True
    order.save()
    return redirect('/admin/store/order/')


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)