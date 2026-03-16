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
from django.db.models import Q
from django.views.decorators.http import require_POST

def _normalize_phone(raw: str) -> str:
    if raw is None:
        return ""
    digits = "".join(ch for ch in raw.strip() if ch.isdigit())
    # Accept formats like "+91 99999 99999" by keeping the last 10 digits.
    if len(digits) > 10:
        digits = digits[-10:]
    return digits

def home(request):
    return render(request, 'store/home.html')

def login_view(request):
    if request.method == "POST":
        phone = _normalize_phone(request.POST.get("phone", ""))
        password = request.POST.get("password", "")
        user = authenticate(username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            return render(request, "store/login.html", {"error": "Invalid phone number or password"})
    return render(request, "store/login.html")

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    query = (request.GET.get("q") or "").strip()

    products = Product.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {'products': products, 'cartItems': cartItems, 'query': query}
    return render(request, 'store/store.html', context)

def product_detail(request, product_id: int):
    data = cartData(request)
    cartItems = data['cartItems']

    product = get_object_or_404(Product, id=product_id)

    user_rating = None
    user_review = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, product=product).first()
        user_review = Review.objects.filter(user=request.user, product=product).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        rating_val = request.POST.get("rating")
        review_text = (request.POST.get("review_text") or "").strip()

        if rating_val:
            try:
                rating_int = int(rating_val)
            except ValueError:
                rating_int = None
            if rating_int in {1, 2, 3, 4, 5}:
                Rating.objects.update_or_create(
                    user=request.user,
                    product=product,
                    defaults={"rating": rating_int},
                )

        if review_text:
            Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={"review_text": review_text},
            )

        return redirect("product_detail", product_id=product.id)

    context = {
        "product": product,
        "cartItems": cartItems,
        "user_rating": user_rating.rating if user_rating else None,
        "user_review": user_review.review_text if user_review else "",
        "reviews": Review.objects.filter(product=product).select_related("user").order_by("-id")[:20],
    }
    return render(request, "store/product_detail.html", context)

@login_required
def my_orders(request):
    customer, _ = Customer.objects.get_or_create(user=request.user)
    orders = (
        Order.objects.filter(customer=customer, complete=True)
        .order_by("-paid_at", "-date_order")
        .prefetch_related("orderitem_set__product")
    )
    data = cartData(request)
    return render(
        request,
        "store/orders.html",
        {"orders": orders, "cartItems": data["cartItems"]},
    )

@login_required
def order_detail(request, order_id: int):
    customer, _ = Customer.objects.get_or_create(user=request.user)
    order = get_object_or_404(Order, id=order_id, customer=customer)
    items = order.orderitem_set.select_related("product").all()
    data = cartData(request)
    return render(
        request,
        "store/order_detail.html",
        {"order": order, "items": items, "cartItems": data["cartItems"]},
    )


def signup_view(request):
    if request.method == "POST":
        name = request.POST["name"]
        surname = request.POST["surname"]
        email = request.POST["email"]
        phone = _normalize_phone(request.POST.get("phone", ""))
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            return render(request, "store/signup.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=phone).exists():
            return render(request, "store/signup.html", {"error": "Phone number already registered"})

        if not phone or len(phone) != 10:
            return render(request, "store/signup.html", {"error": "Enter a valid 10-digit phone number"})

        user = User.objects.create_user(username=phone, email=email, password=password1, first_name=name, last_name=surname)
        user.save()
        Customer.objects.get_or_create(user=user, defaults={"name": name, "email": email})
        return redirect("login")

    return render(request, "store/signup.html")

def logout_view(request):
    logout(request)
    return redirect("home")

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    items = data["items"]
    cartItems = data["cartItems"]

    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
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

    context = {"order": order, "items": items, "cartItems": cartItems, "billing_info": billing_info}
    return render(request, 'store/checkout.html', context)

@login_required
@require_POST
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer, _ = Customer.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=productId)
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

@login_required
@require_POST
def confirm_payment_view(request, order_id):
    customer, _ = Customer.objects.get_or_create(user=request.user)
    order = get_object_or_404(Order, id=order_id, customer=customer)
    order.mark_paid()
    order.save(update_fields=["payment_confirmed", "complete", "status", "paid_at"])
    return JsonResponse({'message': 'Payment confirmed'})

def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.payment_confirmed = True
    order.save()
    return redirect('/admin/store/order/')


def processOrder(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    try:
        total = float(data['form']['total'])
    except (TypeError, ValueError, KeyError):
        return JsonResponse({"status": "error", "message": "Invalid total"}, status=400)
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.transaction_id = transaction_id
        order.mark_paid()
        order.save(update_fields=["transaction_id", "payment_confirmed", "complete", "status", "paid_at"])
    else:
        order.transaction_id = transaction_id
        order.save(update_fields=["transaction_id"])

    if order.shipping == True and order.complete:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse({'status': 'ok', 'order_id': order.id}, safe=False)