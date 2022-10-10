from django.contrib.auth.models import User
from django.test import TestCase
from purbeurre_website.models import Category, Product, Favourite


class TestModels(TestCase):

    def setUp(self):

        self.user = User.objects.create(username="Arnaud")
        self.category1 = Category.objects.create(
            category_id=1,
            category_name="Fruits",
            category_url="https://fr.openfoodfacts.org/categorie/fruits?json=1"
        )

        self.product1 = Product.objects.create(
            category_id=Category(self.category1.category_id),
            product_id=1,
            product_name="orange",
            product_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            product_url="https://fr.openfoodfacts…anges-a-dessert-marque-u",
            product_ingredients="orange",
            product_nutriscore="a"
        )

        self.substitute1 = Favourite.objects.create(
            user_id=self.user,
            substitute_id=1,
            substitute_name="orange",
            substitute_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            substitute_nutriscore="a"
        )

    def test_category_inserted_in_database(self):
        self.assertEqual(self.category1.category_name, "Fruits")

    def test_product_inserted_in_database(self):
        self.assertEqual(self.product1.product_name, "orange")

    def test_substitute1_inserted_in_database(self):
        self.assertEqual(self.substitute1.substitute_name, "orange")
