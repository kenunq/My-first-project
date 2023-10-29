from django.db import models

# Create your models here.


class AddonCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Addon(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название аддона')
    description = models.TextField(verbose_name='Краткое описание аддона')
    #возможно сделать хтмл разметку
    full_description = models.TextField(verbose_name='Полное описание аддона')
    category = models.ManyToManyField(AddonCategory, related_name='a_category', verbose_name='Категория')

    file = models.FileField(upload_to='addons_file', null=True, verbose_name='Файл с аддоном')
    preview = models.ImageField(upload_to='addons_images/preview', verbose_name='Картинка карточки аддона')

    price = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='Цена')

    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг', default='')

    is_published = models.BooleanField(default=False, verbose_name='Публикация')

    # так же при добавлении данного метода в админку добавляется кнопка 'СМОТРЕТЬ НА САЙТЕ >'
    # def get_absolute_url(self):
    #     return reverse('guide', kwargs={'guide_slug': self.slug})

    def __str__(self):
        return f"Аддон: {self.name} | Категория: {self.category.name}"


class AddonImage(models.Model):
    image = models.ImageField(upload_to='addons_images', verbose_name='Картинка аддона')
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE, related_name='images')