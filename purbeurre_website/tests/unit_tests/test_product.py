from django.contrib.auth.models import User
from django.test import TestCase

from purbeurre_website.models import Product, Category
from purbeurre_website.product_importer import ProductImporter


class TestProduct(TestCase):

    def setUp(self):

        self.product_imp = ProductImporter()
        self.user = User.objects.create(
            id=1,
            username="Lucie",
            email="lucie@gmail.com"
        )

        self.category = Category.objects.create(
            category_id=1,
            category_name="Snacks",
            category_url="https://fr.openfoodfacts.org/categorie/snacks?json=1"
        )
        self.products_list = [
                {'categories': 'Snacks, Snacks sucrés, Cacao et dérivés, Confiseries, Confiseries chocolatées, Bonbons de chocolat, Truffes en chocolat',
                 'name': "Chocolate Truffles with Baileys",
                 'nutriscore': 'c',
                 'image': 'https://images.openfoodfacts.org/images/products/335/382/001/2379/front_fr.18.200.jpg',
                 'ingredients': '',
                 'url': 'https://fr.openfoodfacts.org/produit/5099872017051/chocolate-truffles-with-baileys'
                 },
                {'categories': 'Snacks, Snacks sucrés, Cacao et dérivés, Confiseries, Confiseries chocolatées, Bonbons de chocolat, Truffes en chocolat',
                 'name': 'Mini blinis',
                 'nutriscore': 'd',
                 'image': 'https://images.openfoodfacts.org/images/products/335/382/001/2379/front_fr.18.400.jpg',
                 'ingredients': '',
                 'url': 'https://fr.openfoodfacts.org/produit/3353820012379/mini-blinis-l-apero-du-poissonnier'
                 }
        ]

    def test_extract_product(self):
        test_category_table = Category.objects.all()
        self.product_imp.extract_products(test_category_table, 1)
        assert self.products_list[0]["name"] == "Chocolate Truffles with Baileys"
        assert self.products_list[0]["nutriscore"] == "c"
        assert self.products_list[0]["image"] == "https://images.openfoodfacts.org/images/products/335/382/001/2379/front_fr.18.200.jpg"
        assert self.products_list[0]["ingredients"] == ""
        assert self.products_list[0]["url"] == "https://fr.openfoodfacts.org/produit/5099872017051/chocolate-truffles-with-baileys"

    def test_inject_product_in_database(self):
        products_list = [
            {'categories': 'Snacks, Snacks sucrés, Confiseries, Bonbons, Guimauves',
             'name': 'Chamallows',
             'nutriscore': 'd',
             'image': 'https://images.openfoodfacts.org/images/products/310/322/004/6159/front_fr.50.200.jpg',
             'url': 'https://fr.openfoodfacts.org/produit/3103220046159/chamallows-haribo',
             'ingredients': 'glucose syrup, sugar, water, humectant: sorbitol syrup, gelatin, dextrose, starch, '
                            'fruit concentrates and plants: red beet, safflower, flavour '
             }
        ]
        Category.objects.create(
            category_id=19,
            category_name="Snacks",
            category_url="https://fr.openfoodfacts.org/categorie/snacks?json=1"
        )
        category_table = Category.objects.all()
        product_database = self.product_imp.inject_product_in_database(products_list, category_table)

        expected_value = Product.objects.all()
        assert len(product_database) == len(expected_value)

    def test_check_product_in_database(self):
        category = Category.objects.create(
            category_id=19,
            category_name="Fruits",
            category_url="https://fr.openfoodfacts.org/categorie/fruits?json=1"
        )
        Product.objects.create(
            category_id=Category(category.category_id),
            product_id=18,
            product_name="orange",
            product_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            product_url="https://fr.openfoodfacts…anges-a-dessert-marque-u",
            product_ingredients="orange",
            product_nutriscore="a"
        )
        test_product_table = Product.objects.all()
        test_product_name = "orange"
        response = self.product_imp.check_product_in_database(test_product_name, test_product_table)
        expected_value = "orange"
        assert response != expected_value

    def test_retrieve_product_data(self):
        category = Category.objects.create(
            category_id=19,
            category_name="Fruits",
            category_url="https://fr.openfoodfacts.org/categorie/fruits?json=1"
        )
        Product.objects.create(
            category_id=Category(category.category_id),
            product_id=18,
            product_name="orange",
            product_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            product_url="https://fr.openfoodfacts…anges-a-dessert-marque-u",
            product_ingredients="orange",
            product_nutriscore="a"
        )

        products_list = Product.objects.all()
        product_selected_data = self.product_imp.retrieve_product_data(products_list)
        expected_value = Product.objects.get(product_id=18)
        assert product_selected_data == expected_value

    def test_propose_substitute(self):
        category = Category.objects.create(
            category_id=19,
            category_name="Snacks",
            category_url="https://fr.openfoodfacts.org/categorie/snacks?json=1"
        )

        Product.objects.bulk_create([Product(category_id=Category(category.category_id),
                                             product_id=18,
                                             product_name="haribo",
                                             product_image="https://images.openfoodfacts.org/images/products/310/322/004/6159/front_fr.50.200.jpg",
                                             product_url="https://fr.openfoodfacts.org/produit/3103220046159/chamallows-haribo",
                                             product_ingredients="glucose syrup, sugar, water, humectant: sorbitol syrup, gelatin, dextrose, starch, "
                                                                 "fruit concentrates and plants: red beet, safflower, flavour",
                                             product_nutriscore="d"),
                                     Product(category_id=Category(category.category_id),
                                             product_id=10,
                                             product_name="Croco Baby - Haribo - 165g",
                                             product_image="https://images.openfoodfacts.org/images/products/310/322/004/5626/front_fr.29.400.jpg",
                                             product_url="https://fr.openfoodfacts.org/produit/3103220045626/croco-baby-haribo",
                                             product_ingredients="glucose syrup, solubl fiber - but, sugar, gelatin, dextrose, acidifier: citric acid, aroma, fruit and plant concee: safflower, spirulina, apple, invert sugar sirep dyes: vegetable carotenes, lutein, anthocyanins, coat agents: say white and yellow bee, carnauba wax",
                                             product_nutriscore="b")])

        product_list = Product.objects.all()
        product_selected_data = product_list.get(product_id="18")
        product_list = Product.objects.all()
        substitute_proposed_list_sorted = self.product_imp.propose_substitute(product_selected_data, product_list)
        expected_value = [{'product_name': 'Croco Baby - Haribo - 165g', 'product_nutriscore': 'b',
                           'product_image': 'https://images.openfoodfacts.org/images/products/310/322/004/5626/front_fr.29.400.jpg',
                           'ingredients': 'glucose syrup, solubl fiber - but, sugar, gelatin, dextrose, acidifier: citric acid, aroma, fruit and plant concee: safflower, spirulina, apple, invert sugar sirep dyes: vegetable carotenes, lutein, anthocyanins, coat agents: say white and yellow bee, carnauba wax',
                           'url': 'https://fr.openfoodfacts.org/produit/3103220045626/croco-baby-haribo'}]
        assert substitute_proposed_list_sorted == expected_value
