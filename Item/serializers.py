from rest_framework import serializers
from .models import *


class ItemVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVideo
        fields = '__all__'

class ItemFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemFeedback
        fields = '__all__'
class ItemFaqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemFaq
        fields = '__all__'
class ItemVolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVolume
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    volumes = ItemVolumeSerializer(many=True, required=False, read_only=True)
    feedbacks = ItemFeedbackSerializer(many=True, required=False, read_only=True)
    faqs = ItemFaqsSerializer(many=True, required=False, read_only=True)
    videos = ItemVideoSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Item
        fields = '__all__'




