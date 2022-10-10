"""Internal imports"""
from operator import itemgetter
import random
import requests
import unidecode
from requests import get
from purbeurre_website.models import Category, Product


class ProductImporter:
    """
    Import category of products from the API OpenFoodFacts(OFF) and insert it in the database.
    """

    def __init__(self):

        self.product_database = Product.objects.all()
        self.product_data = {}
        self.product_url_list = []
        self.products_list = []
        self.substitute_data = {}
        self.substitute_proposed_list = []

    @staticmethod
    def load_category_url():
        """
        Loads category URLS from the category table.
        """
        category_database = Category.objects.all()
        category_url_list = []
        for category in category_database:
            category_url_json = category.category_url + "&json=1"
            category_url_list.append(category_url_json)
        return category_url_list

    def extract_products(self, category_url_list, nb_product):
        for url in category_url_list:
            request = get(url)
            product_page_json = request.json()
            number = 0
            while number < nb_product:
                self.product_data = {"categories": "",
                                     "product_name": "",
                                     "nutriscore": "",
                                     "product_image": "",
                                     "url": "",
                                     "ingredients": ""
                                     }
                try:
                    product_category = product_page_json["products"][number]["categories_old"]
                    self.product_data["categories"] = product_category

                    product_image = product_page_json["products"][number]["image_url"]
                    self.product_data["product_image"] = product_image

                    product_name = product_page_json["products"][number]["product_name_fr"]
                    self.product_data["product_name"] = product_name

                    nutriscore = product_page_json["products"][number]["nutrition_grade_fr"]
                    self.product_data["nutriscore"] = nutriscore

                    url = product_page_json["products"][number]["url"]
                    self.product_data["url"] = url

                    ingredients = product_page_json["products"][number]["ingredients_text_fr"]
                    self.product_data["ingredients"] = ingredients

                    self.products_list.append(self.product_data)
                    number += 1

                except KeyError:
                    number += 1
        return self.products_list

    def inject_product_in_database(self, products_list, category_table):

        num_id = 1
        for product in products_list:
            for category in category_table:
                if category.category_name in product["categories"]:
                    category_id = Category(category.category_id)
                    product_data = Product(
                        category_id=category_id,
                        product_id=num_id,
                        product_name=product["product_name"],
                        product_nutriscore=product["nutriscore"],
                        product_image=product["product_image"],
                        product_ingredients=product["ingredients"],
                        product_url=product["url"]
                    )
                    product_data.save()
                    num_id = num_id + 1
        return self.product_database

    @staticmethod
    def check_product_in_database(searched_product_name, product_database):
        products_list = []
        for product in product_database:
            for word in searched_product_name.split():
                if word.capitalize() in product.product_name.split():
                    product_selected = Product.objects.filter(product_name__contains=word.capitalize())
                    products_list.append(product_selected)
        return products_list[0]

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
                    "nutriscore": product.product_nutriscore,
                    "product_image": product.product_image,
                    "ingredients": product.product_ingredients,
                    "url": product.product_url
                }
                self.substitute_proposed_list.append(self.substitute_data)

        substitute_proposed_list_sorted = sorted(self.substitute_proposed_list, key=itemgetter('nutriscore'))
        return substitute_proposed_list_sorted
