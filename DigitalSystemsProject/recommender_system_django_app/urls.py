from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="Homepage"),
    path('login/', views.login_function, name='Login'),
    path('logout/', views.logout_function, name='Logout'),
    path('register/', views.register_function, name='Register'),
    path('recommendComic/', views.recommender_system_function, name='Recommend_Comic'),
    path('comicsList/', views.comics_list_function, name='Comic_List'),
    path('comicsList/individualComic/<comicID>', views.individual_comic_function, name='Individual_Comic'),
    path('allcomics/', views.all_comics_function, name="Comics_List"),
    path('allcomics/updatecomic/<comicID>', views.update_comic_function, name="Update_Comic"),
    path('allcomics/deletecomic/<comicID>', views.delete_comic_function, name="Delete_Comic")
]