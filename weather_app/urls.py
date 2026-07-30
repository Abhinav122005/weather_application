from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('favorite/',views.add_favorite, name='favorite'),
    path("favorite/delete/<int:city_id>/",views.delete_favorite,name="delete_favorite"),
    path("current-location/",views.current_location,name="current_location"),

]