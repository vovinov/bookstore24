from django.db import models
from django.utils.text import slugify
from django.urls import reverse

import random
import string


def rand_slug():
    return ''.join(random.choice(string.ascii_lowercase + string.digits for _ in range(3)))


class Category(models.Model):
    name = models.CharField('Категория', max_length=250, db_index=True)
    parent = models.ForeignKey('Родительская категория', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    slug = models.SlugField('URL', max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


    def __str__(self):
        full_path = [self.name]
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])
    

    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(rand_slug() + self.name)
        super(Category, self).save(*args, **kwargs)

    
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})   