from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from Cart.models import Cart


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    firstname = None
    lastname = None
    avatar = models.ImageField('Аватар', upload_to='user', blank=True, null=True, default='profile.svg')
    fio = models.CharField('ФИО', max_length=50, blank=True, null=True, default='Иван')
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    email = models.EmailField('Эл. почта', blank=True, null=True, unique=True)
    birthday = models.CharField('Дата рождения', max_length=50, blank=True, null=True)

    is_email_verified = models.BooleanField('EMail подтвержден?', default=False , editable=False)

    total_summ = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return f'{self.fio} {self.phone} '


class Transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='transactions')
    amount = models.IntegerField(default=0)
    is_buy = models.BooleanField(default=False)
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

def user_post_save(sender, instance, created, **kwargs):
    """Создание всех значений по-умолчанию для нового пользовыателя"""
    if created:
        Cart.objects.create(user=instance)




post_save.connect(user_post_save, sender=User)