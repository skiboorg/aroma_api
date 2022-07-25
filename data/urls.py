from django.urls import path,include
from . import views

urlpatterns = [
    path('banners', views.GetBanners.as_view()),
    path('static', views.GetStaticData.as_view()),
    path('c_form', views.CForm.as_view()),
    path('blog_categories', views.GetAllBlogCats.as_view()),
    path('blog_category', views.GetBlogCat.as_view()),
    path('blog_item', views.GetBlogItem.as_view()),






]
