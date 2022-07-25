from django.db import models
from pytils.translit import slugify
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField

def makeThumb(image):
    fill_color = '#fff'
    base_image = Image.open(image)
    blob = BytesIO()
    if base_image.mode in ('RGBA', 'LA'):
        background = Image.new(base_image.mode[:-1], base_image.size, fill_color)
        background.paste(base_image, base_image.split()[-1])
        base_image = background

    width, height = base_image.size
    transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.thumbnail((415, 440), Image.ANTIALIAS)
    transparent.save(blob, 'png', quality=100, optimize=True)
    return blob



class Item(models.Model):
    name = models.CharField('Название', max_length=100, blank=False, null=True)
    name_slug = models.CharField('Название', max_length=100, blank=True, null=True, editable=False)
    article = models.CharField('Артикул', max_length=20, blank=False, null=True)
    description_short = models.TextField('Короткое описание', blank=True, null=True)
    description = RichTextUploadingField('Описание товара', blank=True, null=True)
    info = RichTextUploadingField('Информация о товаре', blank=True, null=True)
    purpose = RichTextUploadingField('Назначение', blank=True, null=True)
    image = models.ImageField('Большое изображение', upload_to='item/full', blank=True, null=True)
    image_thumb = models.ImageField('Маленькое изображение', upload_to='item/thumb', blank=True, null=True)

    is_active = models.BooleanField('Активен ?',default=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        self.image_thumb.save(f'{self.name_slug}.jpg', File(makeThumb(self.image)), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.image:
            return mark_safe(f'<img src="{self.image_thumb.url}" width="235" height="160" />')
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Картинка'


class ItemVolume(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE,blank=True,null=True,related_name='volumes')
    label = models.CharField('Название, например 10 мл', max_length=20,blank=False,null=True)
    volume = models.IntegerField('Объем', default=0)
    price = models.IntegerField('Цена', default=0)
    left = models.IntegerField('Остаток', default=0)
    weight = models.DecimalField('Вес в кг', decimal_places=2, max_digits=4, blank=False, default=0)
    width = models.DecimalField('Ширина в см', decimal_places=2, max_digits=4, blank=False, default=0)
    height = models.DecimalField('Высота в см', decimal_places=2, max_digits=4, blank=False, default=0)
    length = models.DecimalField('Длина в см', decimal_places=2, max_digits=4, blank=False, default=0)
    def __str__(self):
        return f'Объем'

class ItemFeedback(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE,blank=True,null=True,related_name='feedbacks')
    fio = models.TextField('Отзыв от', default=0)
    text = models.TextField('Текст', default=0)

    def __str__(self):
        return f'Отзыв'

class ItemVideo(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE,blank=True,null=True,related_name='videos')
    name = models.TextField('Название', default=0)
    link = models.TextField('Код видео на youtube', default=0)

    def __str__(self):
        return f'Видео'

class ItemFaq(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE,blank=True,null=True,related_name='faqs')
    question = models.TextField('Вопрос', default=0)
    answer = models.TextField('Ответ', default=0)

    def __str__(self):
        return f'Вопрос-ответ'