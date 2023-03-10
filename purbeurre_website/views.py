import ast
import random
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.conf import settings

from .models import Category, Product
from .product_importer import ProductImporter
from .category_importer import CategoryImporter
from .forms import CreateUser, UpdateUserForm, ChangePasswordForm
from .substitute_in_favourite import SubstituteInFavourite
from .delete_product import ProductEliminator


def home(request):
    user = request.user
    if user is None:
        logout(request)
        messages.success(request, 'Etat : Non connecté')

    return render(request, 'home.html')


def create_account(request):
    create_account_form = CreateUser()
    if request.method == "POST":
        create_account_form = CreateUser(request.POST)
        if create_account_form.is_valid():
            create_account_form.save()
            username = create_account_form.cleaned_data.get('username')
            messages.success(request, 'Compte crée avec succès pour ' + username + ' !')
            return redirect('login_user')
    context = {'create_account_form': create_account_form}
    return render(request, 'create_account.html', context)


def update_user(request):
    actual_user_data = User.objects.get(username=request.user)
    if request.method == "POST":
        update_user_form = UpdateUserForm(request.POST, instance=actual_user_data)
        new_username = update_user_form["new_username"].value()
        new_email = update_user_form["new_email"].value()
        if update_user_form.is_valid():
            update_user_form.save()
            new_user_data = update_user_form.update_user(
                actual_user_data,
                new_username,
                new_email,
                actual_user_data.password
            )
            messages.success(request, 'Profil bien mis à jour pour ' + new_user_data.username + ' !')
            return redirect('login_user')
    else:
        update_user_form = UpdateUserForm(request.POST)

    context = {'update_user_form': update_user_form}
    return render(request, 'update_user.html', context)


def change_password(request):
    user = request.user
    change_password_form = ChangePasswordForm(user, request.POST)
    if request.method == 'POST':
        if change_password_form.is_valid():
            change_password_form.save()
            messages.success(request, "Mot de passe bien modifié !")
            return redirect('login_user')
        else:
            messages.error(request, mark_safe("Erreur : Mot de passe différents !<br/>Veuillez recommencer votre saisie"))
            change_password_form = ChangePasswordForm(user, request.POST)

    context = {'change_password_form': change_password_form}
    return render(request, 'change_password.html', context)


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = User.objects.get(email=email).username
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Bienvenue sur le site de Pur Beurre ' + user.username + ' !')
            return redirect('home')
        else:
            messages.error(request, "Email et/ou mot de passe inconnus")
    return render(request, 'login_user.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Etat : Non connecté')
    return render(request, 'home.html')


@login_required(login_url='login_user')
def user_account(request):
    current_user = request.user
    user_id = current_user.id
    context = {"user_id": user_id}
    return render(request, 'user_account.html', context)


def propose_substitute(request):

    if request.method == "POST":
        product_database = Product.objects.all()
        searched_product_name = request.POST.get('searched_product_name')
        product_imported = ProductImporter()
        products_list = product_imported.check_product_in_database(searched_product_name, product_database)
        product_selected_data = product_imported.retrieve_product_data(products_list[0])
        if len(products_list) == 0:
            messages.info(request, "Il n'y a pas de produit correspondant à votre recherche.")
            return redirect('home')

        # We fetch the products of this category
        substitute_list = Product.objects.filter(category_id=product_selected_data.category_id.category_id)
        product_imported = ProductImporter()
        substitute_list = product_imported.propose_substitute(product_selected_data, substitute_list)
        # We filter the products of the list to have a substitute list
        context = {
            "product_selected_data": product_selected_data,
            "substitute_list": substitute_list,
        }
        return render(request, 'propose_substitute.html', context)


@login_required(login_url='login_user')
def add_favourite(request):
    # We fetch the id of the user
    current_user = request.user
    user_id = current_user.id

    if request.method == "POST":
        substitute_selected_data = request.POST.get('substitute_selected_data')
        substitute_selected_data = ast.literal_eval(substitute_selected_data)

        favourite_database = SubstituteInFavourite()
        favourite_database = favourite_database.inject_substitute_in_favourite(substitute_selected_data, user_id)
        messages.info(request, "Voici vos favoris")
        context = {"favourite_database": favourite_database}
        return render(request, 'display_favourite.html', context)


def delete_product(request):
    if request.method == "POST":
        substitute_selected_id = request.POST.get('substitute_selected_id')
        substitute_deleted = ProductEliminator()
        favourite_database = substitute_deleted.delete_substitute(substitute_selected_id)

        if len(favourite_database) == 0:
            messages.info(request, "Favoris vide")
        else:
            messages.info(request, "Voici vos favoris")

        context = {"favourite_database": favourite_database}
        return render(request, 'display_favourite.html', context)


@login_required(login_url='login_user')
def display_favourite(request):
    current_user = request.user
    user_id = current_user.id
    favourite_database = SubstituteInFavourite()
    favourite_database = favourite_database.retrieve_favourite_database(user_id)

    if len(favourite_database) == 0:
        messages.info(request, "Favoris vide")
    else:
        messages.info(request, "Voici vos favoris")

    context = {"favourite_database": favourite_database}
    return render(request, 'display_favourite.html', context)


def product_data(request):
    if request.method == "POST":
        product_selected_id = int(request.POST.get("product_selected_id"))
        product_selected_data = Product.objects.get(product_id=product_selected_id)
        product_importer = ProductImporter()
        comment_table = product_importer.retrieve_comment_table(product_selected_id)
        context = {'product_selected_data': product_selected_data,
                   'comment_table': comment_table
                   }
        return render(request, 'product_data.html', context)


@login_required(login_url='login_user')
def submit_mail(request):
    current_user = request.user
    if request.method == "POST":
        message = request.POST["message"]
        send_mail(
            'Message',
            message,
            current_user.email,
            ['sengmanynicolas21@gmail.com'],
            fail_silently=False,
        )
        messages.success(request, "Message bien envoyé ! ")

    return render(request, 'home.html')
