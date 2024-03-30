from django.db import models

from user.models import User


# Create your models here.


class AddonCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Compatible_Versions(models.Model):
    version = models.CharField("Версия игры", max_length=32)

    def __str__(self):
        return self.version


class Addon(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название аддона")
    description = models.CharField(verbose_name="Краткое описание аддона")
    full_description = models.TextField(verbose_name="Полное описание аддона")
    category = models.ManyToManyField(AddonCategory, related_name="a_category", verbose_name="Категория")

    author = models.CharField(default="Jojin", max_length=32, verbose_name="Автор")
    version = models.ManyToManyField(Compatible_Versions, verbose_name="Версия игры:")
    file = models.FileField(upload_to="addons_file", null=True, verbose_name="Файл с аддоном")
    preview = models.ImageField(upload_to="addons_images/preview", verbose_name="Картинка карточки аддона")

    price = models.DecimalField(max_digits=6, decimal_places=0, verbose_name="Цена")

    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Слаг", default="")

    is_published = models.BooleanField(default=False, verbose_name="Публикация")

    def __str__(self):
        return f"Аддон: {self.name} | Категория: {self.category.name}"


class AddonImage(models.Model):
    image = models.ImageField(upload_to="addons_images", verbose_name="Картинка аддона")
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE, related_name="images")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE, verbose_name="Аддон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    status = models.BooleanField(default=False, verbose_name="Заказ оплачен?")

    def __str__(self):
        return f"Заказ {self.id}"
