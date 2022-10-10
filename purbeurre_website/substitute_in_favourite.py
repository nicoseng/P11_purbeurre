from django.contrib.auth.models import User


from purbeurre_website.models import Favourite


class SubstituteInFavourite:
    """To inject products datas in favourite database """

    @staticmethod
    def inject_substitute_in_favourite(substitute_selected_data, user_id):

        favourite_database = Favourite.objects.all()
        current_user = User.objects.get(id=user_id)

        if Favourite.objects.filter(substitute_name=substitute_selected_data["product_name"]).exists():
            return favourite_database
        else:
            substitute_selected_data = Favourite(
                user_id=current_user,
                substitute_name=substitute_selected_data["product_name"],
                substitute_image=substitute_selected_data["product_image"],
                substitute_nutriscore=substitute_selected_data["nutriscore"]
            )
            substitute_selected_data.save()
            favourite_database = Favourite.objects.filter(user_id=user_id)
            favourite_database.update()

            return favourite_database

    @staticmethod
    def retrieve_favourite_database(user_id):
        favourite_database = Favourite.objects.all()
        favourite_database = favourite_database.filter(user_id=user_id)
        return favourite_database
