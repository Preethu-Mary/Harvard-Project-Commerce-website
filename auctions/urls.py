from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createNewListing, name="createNewListing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categoryPage, name="categoryPage"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("additem/<int:id>", views.additem, name="additem"),
    path("removeitem/<int:id>", views.removeitem, name="removeitem"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment"),
    path("addbid/<int:id>", views.addbid, name="addbid"),
    path("closelisting/<int:id>", views.closelisting, name="closelisting")
]
