from django.urls import path

from . import views

urlpatterns = [
    path('list-groundwater/', views.list_groundwater, name='list_groundwater'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),

]
