
from .models import *
from django.contrib import admin

class ItemVolumeInline (admin.TabularInline):
    model = ItemVolume
    extra = 0

class ItemFeedbackInline (admin.TabularInline):
    model = ItemFeedback
    extra = 0


class ItemFaqInline(admin.TabularInline):
    model = ItemFaq
    extra = 0


class ItemVideoInline(admin.TabularInline):
    model = ItemVideo
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name', 'article',  'is_active']
    inlines = [ItemVolumeInline, ItemFeedbackInline,ItemFaqInline,ItemVideoInline]
    list_filter = ('is_active',)
    class Meta:
        model = Item

admin.site.register(Item,ItemAdmin)
