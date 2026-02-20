from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#category database
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    #configuration for model
    class Meta:
        #order by name
        ordering = ('name',)
        #fix plural name of model
        verbose_name_plural = 'Categories'
    
    #shows category name for each categories
    def __str__(self):
        return self.name

class Item(models.Model):
    #references category id, related_name -> category에서 item으로 역참조 할 때 간단히 하기 위해 사용
    category = models.ForeignKey(Category, related_name='items',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    #description can be longer, so using TextFiled
    #blank is ok, null is ok
    description = models.TextField(blank=True,null=True)
    price = models.FloatField()
    #upload_to: 업로드 장소 지정
    image = models.ImageField(upload_to='item_images',blank=False,null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name