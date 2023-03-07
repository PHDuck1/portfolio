from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.FilesList.as_view(), name='files_list'),
    path('main/<uuid:pk>/delete/', views.FileDelete.as_view(), name='file_delete'),
    path('main/create/', views.PDFFileCreateView.as_view(), name='file_create'),
    path('', views.ConverterView.as_view(), name='converter'),
]
