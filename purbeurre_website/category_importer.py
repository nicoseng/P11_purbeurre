"""Internal imports"""
from requests import get
from purbeurre_website.models import Category


class CategoryImporter:
    """
    Import category of products from the API OpenFoodFacts(OFF) and insert it in the database.
    """
    @staticmethod
    def load_category_from_OFF():
        """
        Loads the categories datas from the URL address in OFF.
        """
        categories_url = "https://fr.openfoodfacts.org/categories.json"
        request = get(categories_url)

        # To get the json format
        categories_url_json = request.json()
        return categories_url_json

    @staticmethod
    def extract_category(categories_url_json, nb_category):
        # We extract the number of categories we want
        category_list = []
        for category in categories_url_json["tags"][:nb_category]:
            category_data = {
                "name": category["name"],
                "url": category["url"]
            }
            category_list.append(category_data)
        return category_list

    @staticmethod
    def inject_category_in_database(category_list):
        category_table = Category.objects.all()
        num_id = 1
        nb_of_category = len(category_list)
        while num_id < nb_of_category:
            for category in category_list:
                category_data = Category(
                    category_id=num_id,
                    category_name=category["name"],
                    category_url=category["url"]
                )
                category_data.save()
                num_id = num_id + 1
        return category_table
