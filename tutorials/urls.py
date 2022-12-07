from django.urls import re_path
from tutorials import views 
 
urlpatterns = [ 
    re_path(r'^tutorials$', views.tutorial_list),
    re_path(r'^analisis$', views.analisis_list),
]