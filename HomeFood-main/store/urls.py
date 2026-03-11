from django.urls import path
from . import views
from .views import login_view, signup_view, logout_view

urlpatterns = [
    
        path('', views.home, name='home'),
        path('store/', views.store, name="store"),
        path('cart/', views.cart, name="cart"),
        path('checkout/', views.checkout, name="checkout"),
        path('update_item/', views.updateItem, name="update_item"),
        path('process_order/', views.processOrder, name="process_order"),
        path("login/", login_view, name="login"),
        path("signup/", signup_view, name="signup"),
        path("logout/", logout_view, name="logout"),
        path('confirm_payment/<int:order_id>/', views.confirm_payment_view, name='confirm_payment'),

]