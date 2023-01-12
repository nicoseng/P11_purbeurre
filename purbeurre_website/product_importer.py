"""Internal imports"""
from operator import itemgetter
import random
import requests
import unidecode
from requests import get
from purbeurre_website.models import Category, Product


class ProductImporter:
    """
    Import products from the API OpenFoodFacts(OFF) and insert it in the database.
    """

    def __init__(self):
        self.substitute_data = {}
        self.substitute_proposed_list = []

    @staticmethod
    def extract_products(category_table, nb_product):
        products_list = []
        # We fetch the url of each category in category table
        for category in category_table:
            params = {
                "categorie": category.category_name,
                "json": "true",
                "page_size": nb_product,  # number of products we want
            }
            request = requests.get(category.category_url, params=params)
            products_data_json = request.json()
            counter = 0
            while counter < nb_product:
                try:
                    product_data = {
                        "categories": products_data_json["products"][counter]["categories"],
                        "name": products_data_json["products"][counter]["product_name"],
                        "nutriscore": products_data_json["products"][counter]["nutrition_grades"],
                        "image": products_data_json["products"][counter]["image_front_small_url"],
                        "ingredients": products_data_json["products"][counter]["ingredients_text"],
                        "url": products_data_json["products"][counter]["url"]
                    }
                    products_list.append(product_data)
                    counter += 1
                except KeyError:
                    counter += 1
        return products_list

    @staticmethod
    def inject_product_in_database(products_list, category_table):
        product_table = Product.objects.all()
        num_id = 1
        for product in products_list:
            for category in category_table:
                if category.category_name in product["categories"]:
                    category_id = Category(category.category_id)
                    product_data = Product(
                        category_id=category_id,
                        product_id=num_id,
                        product_name=product["name"],
                        product_nutriscore=product["nutriscore"],
                        product_image=product["image"],
                        product_ingredients=product["ingredients"],
                        product_url=product["url"]
                    )
                    product_data.save()
                    num_id = num_id + 1
        return product_table

    @staticmethod
    def check_product_in_database(searched_product_name, product_database):
        products_list = []
        for product in product_database:
            for word in searched_product_name.split():
                if word.capitalize() in product.product_name.split():
                    product_selected = Product.objects.filter(product_name__contains=word.capitalize())
                    products_list.append(product_selected)
        return products_list

    @staticmethod
    def retrieve_product_data(products_list):
        random_product_selected = random.choice(products_list)
        return random_product_selected

    def propose_substitute(self, product_selected_data, product_list):
        product_selected_nutriscore = product_selected_data.product_nutriscore
        available_nutriscore_list = ["a", "b", "c", "d", "e"]
        selected_nutriscore_index = \
            available_nutriscore_list.index(product_selected_nutriscore)
        best_nutriscore_list = \
            available_nutriscore_list[0:selected_nutriscore_index]

        for product in product_list:
            if product.product_nutriscore in best_nutriscore_list or product.product_nutriscore == "a":
                self.substitute_data = {
                    "product_name": product.product_name,
                    "product_nutriscore": product.product_nutriscore,
                    "product_image": product.product_image,
                    "ingredients": product.product_ingredients,
                    "url": product.product_url
                }
                self.substitute_proposed_list.append(self.substitute_data)

        substitute_proposed_list_sorted = sorted(self.substitute_proposed_list, key=itemgetter('product_nutriscore'))
        return substitute_proposed_list_sorted
