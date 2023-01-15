from django.urls import path

from .views import ConverterView, FilesList, FileDelete, FileCreate

urlpatterns = [
    path('list/', FilesList.as_view(), name='files_list'),
    path('main/<uuid:pk>/delete/', FileDelete.as_view(), name='file_delete'),
    path('main/create/', FileCreate.as_view(), name='file_create'),
    path('', ConverterView.as_view(), name='converter'),
]
