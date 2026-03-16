from django.urls import path
from . import views
from .views import login_view, signup_view, logout_view

urlpatterns = [
    
        path('', views.home, name='home'),
        path('store/', views.store, name="store"),
        path('product/<int:product_id>/', views.product_detail, name="product_detail"),
        path('orders/', views.my_orders, name="my_orders"),
        path('orders/<int:order_id>/', views.order_detail, name="order_detail"),
        path('cart/', views.cart, name="cart"),
        path('checkout/', views.checkout, name="checkout"),
        path('update_item/', views.updateItem, name="update_item"),
        path('process_order/', views.processOrder, name="process_order"),
        path("login/", login_view, name="login"),
        path("signup/", signup_view, name="signup"),
        path("logout/", logout_view, name="logout"),
        path('confirm_payment/<int:order_id>/', views.confirm_payment_view, name='confirm_payment'),

]