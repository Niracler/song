from django.db import models
from .tools import get_songs_path
from taggit.managers import TaggableManager


# Create your models here.

class Tag(models.Model):
    tid = models.BigAutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=32, unique=True, verbose_name='标签名')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ('-tid',)

    def __str__(self):
        return self.name


class Comment(models.Model):
    cid = models.BigAutoField(primary_key=True, verbose_name='ID')
    body = models.CharField(max_length=512, verbose_name='评论内容')
    creator = models.IntegerField(default=1, verbose_name='创建者ID')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ('-cid',)

    def __str__(self):
        return self.body


class Author(models.Model):
    aid = models.BigAutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=128, verbose_name='作者名')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    description = models.TextField(default='这人什么都没写', verbose_name='作者描述')

    class Meta:
        ordering = ('-aid',)

    def __str__(self):
        return self.name


class Song(models.Model):
    sid = models.BigAutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=128, verbose_name='歌曲名称')
    file = models.FileField(upload_to=get_songs_path, verbose_name='歌曲文件链接')
    authors = models.ManyToManyField(Author, related_name='song_author', verbose_name='作者')
    creator = models.IntegerField(default=1, verbose_name='创建者ID')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ('-sid',)

    def __str__(self):
        return self.name


class PlayList(models.Model):
    lid = models.BigAutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=128, verbose_name='歌单名称')
    tracks = models.ManyToManyField(Song, related_name='tracks', verbose_name='歌曲列表')
    creator = models.IntegerField(default=1, verbose_name='创建者ID')
    tags = models.ManyToManyField(Tag, related_name='playlist_tag', verbose_name='标签')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    description = models.TextField(verbose_name='歌单描述')

    class Meta:
        ordering = ('-lid',)

    def __str__(self):
        return self.name
