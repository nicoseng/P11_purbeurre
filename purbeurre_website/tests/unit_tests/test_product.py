from django.contrib.auth.models import User
from django.test import TestCase

from purbeurre_website.models import Product, Category
from purbeurre_website.product_importer import ProductImporter


class TestProduct(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            id=1,
            username="Lucie",
            email="lucie@gmail.com"
        )

        self.category = Category.objects.create(
            category_id=1,
            category_name="Fruits",
            category_url="https://fr.openfoodfacts.org/categorie/fruits?json=1"
        )
        # self.product = Product.objects.create(
        #     category_id=Category(self.category.category_id),
        #     product_id=1,
        #     product_name="orange",
        #     product_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
        #     product_url="https://fr.openfoodfacts…anges-a-dessert-marque-u",
        #     product_ingredients="orange",
        #     product_nutriscore="a"
        # )

    def test_load_category_url(self):
        product_imp = ProductImporter()
        category_url_list = product_imp.load_category_url()
        expected_value = ["https://fr.openfoodfacts.org/categorie/fruits?json=1"]
        assert category_url_list == expected_value

    def test_extract_products(self):
        products_list_url = ["https://fr.openfoodfacts.org/cgi/search.pl?json=1&action=process&search_simple=1"
                             "&search_terms=haribo&page=0"]
        nb_product = 1
        product_imp = ProductImporter()
        products_list = product_imp.extract_products(products_list_url, nb_product)
        expected_value = [
            {'categories': 'Snacks, Snacks sucrés, Confiseries, Bonbons, Guimauves', 'product_name': 'Chamallows',
             'nutriscore': 'd',
             'product_image': 'https://images.openfoodfacts.org/images/products/310/322/004/6159/front_fr.50.400.jpg',
             'url': 'https://fr.openfoodfacts.org/produit/3103220046159/chamallows-haribo',
             'ingredients': 'glucose syrup, sugar, water, humectant: sorbitol syrup, gelatin, dextrose, starch, fruit concentrates and plants: red beet, safflower, flavour'}]
        assert products_list == expected_value

    def test_inject_product_in_database(self):
        products_list = [
            {'categories': 'Snacks, Snacks sucrés, Confiseries, Bonbons, Guimauves',
             'product_name': 'Chamallows',
             'nutriscore': 'd',
             'product_image': 'https://images.openfoodfacts.org/images/products/310/322/004/6159/front_fr.50.200.jpg',
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
        product_imp = ProductImporter()
        product_database = product_imp.inject_product_in_database(products_list, category_table)

        expected_value = Product.objects.all()
        assert len(product_database) == len(expected_value)

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

        product_imp = ProductImporter()
        products_list = Product.objects.all()
        product_selected_data = product_imp.retrieve_product_data(products_list)
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

        product_imp = ProductImporter()
        product_list = Product.objects.all()
        product_selected_data = product_list.get(product_id="18")
        product_list = Product.objects.all()
        substitute_proposed_list_sorted = product_imp.propose_substitute(product_selected_data, product_list)
        expected_value = [{'product_name': 'Croco Baby - Haribo - 165g', 'product_nutriscore': 'b', 'product_image': 'https://images.openfoodfacts.org/images/products/310/322/004/5626/front_fr.29.400.jpg', 'ingredients': 'glucose syrup, solubl fiber - but, sugar, gelatin, dextrose, acidifier: citric acid, aroma, fruit and plant concee: safflower, spirulina, apple, invert sugar sirep dyes: vegetable carotenes, lutein, anthocyanins, coat agents: say white and yellow bee, carnauba wax', 'url': 'https://fr.openfoodfacts.org/produit/3103220045626/croco-baby-haribo'}]
        assert substitute_proposed_list_sorted == expected_value
