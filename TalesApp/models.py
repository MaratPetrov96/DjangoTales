from django.db.models import *
from django.contrib.auth.models import User
from django.conf import settings as django_settings

class Profile(Model):
    user = OneToOneField(User,on_delete=CASCADE,related_name='profile')
    email = CharField('email',max_length=200)
    city = CharField('city',max_length=255)
    picture = ImageField('image',upload_to='users',default=f'default.jpg')

class Genre(Model):
    title = CharField('title',max_length=255)

class Tale(Model):
    user = ForeignKey(User,on_delete=CASCADE,related_name='tales')
    title = CharField('title',max_length=255)
    content = TextField('content')
    genres = ManyToManyField(Genre,related_name='tales')
    mark = FloatField('Mark',default=0.0)

class Img(Model):
    file = ImageField('image',upload_to='tales')
    tale = ForeignKey(Tale,on_delete=CASCADE,related_name='images')

class Comment(Model):
    user = ForeignKey(User,on_delete=CASCADE,related_name='comments')
    tale = ForeignKey(Tale,on_delete=CASCADE,related_name='comments')
    parent = ForeignKey('self',on_delete=CASCADE,related_name='replies',null=True,blank=True)
    content = TextField('comment')

class Mark(Model):
    user = ForeignKey(User,on_delete=CASCADE,related_name='marks')
    tale = ForeignKey(Tale,on_delete=CASCADE,related_name='marks')
    meaning = IntegerField('Meaning')
