from django.test import TestCase
from django.urls import reverse, resolve


class TestUrls(TestCase):

    def test_login_user_url(self):
        path = reverse('login_user')
        assert path == '/login_user/'
        assert resolve(path).view_name == "login_user"

    def test_home_url(self):
        path = reverse('home')
        assert path == '/'
        assert resolve(path).view_name == "home"

    def test_create_account_url(self):
        path = reverse('create_account')
        assert path == '/create_account/'
        assert resolve(path).view_name == "create_account"

    def test_logout_user_url(self):
        path = reverse('logout_user')
        assert path == '/logout_user/'
        assert resolve(path).view_name == "logout_user"

    def test_user_account_url(self):
        path = reverse('user_account')
        assert path == '/user_account/'
        assert resolve(path).view_name == "user_account"

    def test_propose_substitute_url(self):
        path = reverse('propose_substitute')
        assert path == '/propose_substitute/'
        assert resolve(path).view_name == "propose_substitute"

    def test_product_data_url(self):
        path = reverse('product_data')
        assert path == '/product_data/'
        assert resolve(path).view_name == "product_data"

    def test_display_favourite_url(self):
        path = reverse('display_favourite')
        assert path == '/display_favourite/'
        assert resolve(path).view_name == "display_favourite"

    def test_add_favourite_url(self):
        path = reverse('add_favourite')
        assert path == '/add_favourite/'
        assert resolve(path).view_name == "add_favourite"

    def test_delete_product_url(self):
        path = reverse('delete_product')
        assert path == '/delete_product/'
        assert resolve(path).view_name == "delete_product"
