from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Customer, Product, Order, OrderItem, Rating, Review


class StoreFlowTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Burger", price=10.0, digital=False, description="Tasty")
        self.user = User.objects.create_user(username="9999999999", password="pass12345", email="a@b.com")
        Customer.objects.get_or_create(user=self.user)

    def test_login_and_view_store(self):
        ok = self.client.login(username="9999999999", password="pass12345")
        self.assertTrue(ok)
        resp = self.client.get(reverse("store"))
        self.assertEqual(resp.status_code, 200)

    def test_update_item_requires_auth(self):
        resp = self.client.post(
            reverse("update_item"),
            data='{"productId": %d, "action": "add"}' % self.product.id,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 302)  # redirected to login

    def test_add_to_cart_and_create_orderitem(self):
        self.client.login(username="9999999999", password="pass12345")
        resp = self.client.post(
            reverse("update_item"),
            data='{"productId": %d, "action": "add"}' % self.product.id,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        customer = Customer.objects.get(user=self.user)
        order = Order.objects.get(customer=customer, complete=False)
        self.assertEqual(order.orderitem_set.count(), 1)

    def test_rate_and_review_product(self):
        self.client.login(username="9999999999", password="pass12345")
        url = reverse("product_detail", args=[self.product.id])
        resp = self.client.post(url, {"rating": "5", "review_text": "Great"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Rating.objects.filter(user=self.user, product=self.product, rating=5).exists())
        self.assertTrue(Review.objects.filter(user=self.user, product=self.product, review_text="Great").exists())

from django.test import TestCase

# Create your tests here.
