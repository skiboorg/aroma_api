from rest_framework import serializers
from .models import *


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class StaticSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextData
        fields = '__all__'


class BlogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogItem
        fields = '__all__'



class BlogCategoryShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = '__all__'


class BlogCategoryFullSerializer(serializers.ModelSerializer):
    items = BlogItemSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = BlogCategory
        fields = '__all__'





