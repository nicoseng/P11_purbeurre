"""Internal imports"""
from requests import get
from purbeurre_website.models import Category


class CategoryImporter:
    """
    Import category of products from the API OpenFoodFacts(OFF) and insert it in the database.
    """

    def __init__(self):
        self.category_table = Category.objects.all()

    @staticmethod
    def load_category_from_OFF():
        """
        Loads the categories datas

        from the URL address in OFF.
        """

        categories_url = "https://fr.openfoodfacts.org/categories&json=1"
        request = get(categories_url)

        # To get the json format
        categories_url_json = request.json()

        return categories_url_json

    @staticmethod
    def fetch_category(categories_url_json, nb_category):
        # We fetch the categories
        category_list = []
        for category in categories_url_json["tags"][:nb_category]:
            category_data = {
                "category_name": category["name"],
                "category_url": category["url"]
            }
            category_list.append(category_data)

        return category_list

    def inject_category_in_database(self, category_list):

        num_id = 1
        nb_of_category = len(category_list)
        while num_id < nb_of_category:
            for category in category_list:
                category_data = Category(
                    category_id=num_id,
                    category_name=category["category_name"],
                    category_url=category["category_url"]
                )
                category_data.save()
                num_id = num_id + 1

        return self.category_table

    @staticmethod
    def paginate_category_url(category_list, page):

        """Aims to fetch each category URL link per page"""
        category_url_list = []
        for category in category_list:
            category_url = category["category_url"]

            nb_of_page = range(0, page)
            for number in nb_of_page:

                while page <= len(nb_of_page):
                    category_url_page = "{}&page={}".format(category_url, str(number))
                    category_url_list.append(category_url_page)
                    page += 1
        return category_url_list
