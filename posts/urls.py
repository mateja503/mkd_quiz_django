from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('results/', views.results_list, name='results_list'),
    path('results/<int:result_id>/', views.result_detail, name='result_detail'),
    path('results/excel/import/<int:result_id>/', views.import_results_from_excel, name='import_results_from_excel'),
    path('results/create/', views.create_result, name='create_result'),  # Add this line

]
