from django.urls import path
from main import views


app_name = 'main'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('articles/', views.ArticlesList.as_view(), name='articles_list'),
    path('articles/<int:pk>/', views.ArticleDetail.as_view(), name='article_detail')
]
