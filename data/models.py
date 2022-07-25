from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from pytils.translit import slugify


class Banner(models.Model):
    image = models.ImageField('Баннер', upload_to='banner', blank=True, null=True)
    image_mob = models.ImageField('Баннер мобильный', upload_to='banner', blank=True, null=True)


class ContactForm(models.Model):
    subject = models.CharField('Название', max_length=100, blank=True, null=True)
    text = models.TextField('Текст', blank=True, null=True)
    file = models.ImageField('Баннер', upload_to='form', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BlogCategory(models.Model):
    image = models.ImageField('Картинка категории', upload_to='blog', blank=False, null=True)
    title = models.CharField('Название категории', max_length=100, blank=False, null=True)
    title_slug = models.CharField('Название категории', max_length=100, blank=False, null=True, editable=False)
    text = RichTextUploadingField('Текст превью', blank=False, null=True)
    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категории блога'
        verbose_name_plural = 'Категории блога'

class BlogItem(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, blank=False, null=True, verbose_name='Категория', related_name='items')
    image = models.ImageField('Картинка превью', upload_to='blog', blank=False, null=True)
    image_top = models.ImageField('Картинка в шапке статьи', upload_to='blog', blank=False, null=True)
    title = models.CharField('Название статьи', max_length=100, blank=False, null=True)
    title_slug = models.CharField('Название статьи', max_length=100, blank=False, null=True, editable=False)
    text = RichTextUploadingField('Текст полный', blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class TextData(models.Model):
    payment_info = RichTextUploadingField('Условия оплаты', blank=False, null=True)
    delivery_info = RichTextUploadingField('Условия доставки', blank=False, null=True)
    return_info = RichTextUploadingField('Условия возврата', blank=False, null=True)
    contact_info = RichTextUploadingField('Реквизиты', blank=False, null=True)

    class Meta:
        verbose_name = 'Статические страницы'
        verbose_name_plural = 'Статические страницы'