from purbeurre_website.models import Favourite


class ProductEliminator:
    """Eliminates products datas in Favourite database"""

    @staticmethod
    def delete_substitute(substitute_selected_id):
        favourite_database = Favourite.objects.all()
        substitute_selected_data = Favourite.objects.get(substitute_id=substitute_selected_id)
        substitute_selected_data.delete()

        favourite_database.update()
        return favourite_database
