from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *


class GetBanners(generics.ListAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()

class GetStaticData(generics.RetrieveAPIView):
    serializer_class = StaticSerializer
    def get_object(self):
        return TextData.objects.get(id=1)


class GetAllBlogCats(generics.ListAPIView):
    serializer_class = BlogCategoryShortSerializer
    queryset = BlogCategory.objects.all()

class GetBlogCat(generics.RetrieveAPIView):
    serializer_class = BlogCategoryFullSerializer

    def get_object(self):
        blog_cat = BlogCategory.objects.filter(title_slug=self.request.query_params.get('title_slug'))
        if blog_cat:
            return blog_cat[0]
        else:
            return None

class GetBlogItem(generics.RetrieveAPIView):
    serializer_class = BlogItemSerializer

    def get_object(self):
        blog_item = BlogItem.objects.filter(title_slug=self.request.query_params.get('item_slug'))
        if blog_item:
            return blog_item[0]
        else:
            return None

class CForm(APIView):
    def post(self,request):
        print(request.data)
        form = ContactForm.objects.create(
            subject=request.data['subject'],
            text=request.data['text'],
        )
        if request.FILES.getlist('file'):
            form.file = request.FILES.getlist('file')[0]
            form.save()
        return Response(status=200)


