
from django.urls import path


from django.conf.urls.static import static
from . import views


urlpatterns = [
   
    path('', views.movie_list, name='movie_list'),
    path('create/', views.create_movie, name='create_movie'),
    path('edit/<int:id>/', views.edit_movie, name='edit_movie'),
    path('delete/<int:id>/', views.delete_movie, name='delete_movie'),
    path('signup/', views.signup, name='signup'),
]

