import pytest
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from purbeurre_website.forms import CreateUser
from purbeurre_website.models import Favourite, Product, Category
from purbeurre_website.product_importer import ProductImporter
from purbeurre_website.substitute_in_favourite import SubstituteInFavourite


class TestViews(TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="Louis",
            email="louis@gmail.com",
            password="lunaires"
        )

    def test_not_authenticated_user(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'home.html')
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user(self):
        self.client.login(username="Louis", password="lunaires")
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.client.logout()

    def test_home_view(self):

        self.client.get('home/')
        path = reverse('home')
        response = self.client.get(path)
        assert response.status_code == 302

    def test_create_account_view(self):
        form = CreateUser(
            {"username": "Jeanne",
             "email": "abc@gmail.com",
             "password1": "lunaires",
             "password2": "lunaires"
             }
        )
        assert form.is_valid()

        if form.is_valid():
            form.save()
            assert form.cleaned_data.get('username') == "Jeanne"
            user = form.save()
            self.assertEqual(user.username, "Jeanne")
            self.client.get(reverse('create_account'), follow=True)
        else:
            self.fail("User not valid")

        credentials = {"username": "Lucien", "email": "abc@gmail.com"}
        User.objects.create_user(**credentials)

        # send create_account data
        self.client.post('/create_account/', credentials, follow=True)
        path = reverse('create_account')
        response = self.client.get(path)
        assert response.status_code == 200

    def test_login_user_view(self):
        credentials = {"username": "jeanne", "password":"lunaires", "email": "abc@gmail.com"}
        User.objects.create_user(**credentials)

        # send login data
        response = self.client.post('/login_user/', credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

        path = reverse('login_user')
        response = self.client.get(path)
        assert response.status_code == 200

    def test_logout_user_view(self):
        path = reverse('logout_user')
        response = self.client.get(path)
        assert response.status_code == 200

    def test_user_account_view(self):

        self.client.login(username="Louis", password="lunaires")
        response = self.client.get(reverse('user_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_account.html')
        self.client.logout()

    def test_propose_substitute_view(self):
        category = Category.objects.create(
            category_id=19,
            category_name="Fruits",
            category_url="https://fr.openfoodfacts.org/categorie/fruits?json=1"
        )
        products_list = Product.objects.create(
            category_id=Category(category.category_id),
            product_id=18,
            product_name="orange",
            product_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            product_url="https://fr.openfoodfacts…anges-a-dessert-marque-u",
            product_ingredients="orange",
            product_nutriscore="a"
        )
        credentials = Product.objects.create(
            category_id=Category(category.category_id),
            product_id=11,
            product_name="Pâte à tartiner Nutella noisettes et cacao - 200g",
            product_image="https://images.openfoodf…463/front_fr.168.400.jpg",
            product_url="https://fr.openfoodfacts…es-et-cacao-200g-ferrero",
            product_ingredients="nutella",
            product_nutriscore="e"
        )
        response = self.client.post('propose_substitute/', credentials, follow=True)
        reverse('propose_substitute')
        assert response.status_code == 404

        prod_imp = ProductImporter()
        searched_prod = prod_imp.propose_substitute(credentials, products_list)
        print(searched_prod)
        expected_value = Product.objects.create(
            category_id=Category(category.category_id),
            product_id=18,
            product_name="orange",
            product_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            product_url="https://fr.openfoodfacts…anges-a-dessert-marque-u",
            product_ingredients="orange",
            product_nutriscore="a"
        )
        assert searched_prod == expected_value

    def test_add_favourite_view(self):

        self.client.login(username="Louis", password="lunaires")
        response = self.client.get(reverse('display_favourite'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'display_favourite.html')
        self.client.logout()

    def test_delete_product_view(self):

        self.client.get('delete_product')
        path = reverse('display_favourite')
        response = self.client.get(path)
        self.assertRedirects(response, "/login_user/?next=" + path, 302)

    def test_display_favourite_view(self):
        user_data = {"id": 10, "username": "Lucien", "email": "abc@gmail.com"}
        user_created = User.objects.create(**user_data)
        test_favourite_database = Favourite.objects.all()
        test_substitute_in_favourite = {
            "product_id": 1,
            "product_name": "orange",
            "product_image": "https://images.openfoodf…/0397/front_fr.4.200.jpg",
            "nutriscore": "a"
        }
        sub_fav = SubstituteInFavourite()
        sub_fav.inject_substitute_in_favourite(test_substitute_in_favourite, user_created.id)
        fav_db = sub_fav.retrieve_favourite_database(user_created.id)
        path = reverse('display_favourite')
        response = self.client.get(path)
        assert response.status_code == 302
        assert len(test_favourite_database) == len(fav_db)

    def test_product_data_view(self):
        credentials = {
            "product_id": 1,
            "product_name": "orange",
            "product_image": "https://images.openfoodf…/0397/front_fr.4.200.jpg",
            "product_url": "https://fr.openfoodfacts…anges-a-dessert-marque-u",
            "product_ingredients": "orange",
            "product_nutriscore": "a"
        }
        Product.objects.create(**credentials)
        # send product data
        response = self.client.post('/product_data/', credentials, follow=True)
        assert response.status_code == 200
