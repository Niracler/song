from django.db.models import Count
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Song, Author, PlayList, Comment, Tag


# -------------------------标签的序列化函数---------------------------------

class TagSerializer(serializers.ModelSerializer):
    num_times = serializers.SerializerMethodField(read_only=True)

    def get_num_times(self, obj):
        queryset = Tag.objects.filter(name=obj.name)
        tags = queryset.annotate(num_times=Count('playlist_tag'))

        return tags[0].num_times

    class Meta:
        model = Tag
        fields = "__all__"


# -------------------------评论的序列化函数---------------------------------

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


# -------------------------作者的序列化函数---------------------------------

class AuthorSerializer(serializers.ModelSerializer):
    """关于作者的序列化函数"""

    num_songs = serializers.SerializerMethodField(read_only=True)

    def get_num_songs(self, obj):
        queryset = Author.objects.filter(name=obj.name)
        authors = queryset.annotate(num_songs=Count('song_author'))

        return authors[0].num_songs

    class Meta:
        model = Author
        fields = "__all__"


class AuthorCreateSerializer(serializers.ModelSerializer):
    """关于作者创建的序列化函数"""

    aid = serializers.IntegerField(label='ID', validators=[UniqueValidator(queryset=Author.objects.all())],
                                   help_text='空的话， 就是自增序列', required=False)
    name = serializers.CharField(label="作者名", required=True, allow_blank=False)

    class Meta:
        model = Author
        fields = ('aid', 'name')


# -------------------------歌曲的序列化函数---------------------------------


class AuthorSmallSerializer(serializers.ModelSerializer):
    """关于作者的序列化函数"""

    class Meta:
        model = Author
        fields = ('aid', 'name')


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"


class SongListSerializer(serializers.ModelSerializer):
    """关于歌曲的序列化函数"""
    authors = AuthorSmallSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = "__all__"


class SongCreateSerializer(serializers.ModelSerializer):
    """关于歌曲创建的序列化函数"""
    sid = serializers.IntegerField(label='ID', validators=[UniqueValidator(queryset=Song.objects.all())],
                                   help_text='空的话， 就是自增序列', required=False)

    class Meta:
        model = Song
        fields = ('sid', 'name', 'file', 'authors')


# -------------------------歌单的序列化函数---------------------------------

class SongSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('sid', 'name', 'file')


class PlayListSerializer(serializers.ModelSerializer):
    """关于歌单的序列化函数"""
    tracks = SongSmallSerializer(many=True)
    tags = serializers.SerializerMethodField('get_tags')

    class Meta:
        model = PlayList
        fields = "__all__"

    def get_tags(self, obj):
        tags = []
        for i in obj.tags.all():
            tag = {'tid': i.tid, 'name': i.name}
            tags.append(tag)
        return tags


class PlayListCreateSerializer(serializers.ModelSerializer):
    """关于歌单创建的序列化函数"""

    lid = serializers.IntegerField(label='ID', validators=[UniqueValidator(queryset=PlayList.objects.all())],
                                   help_text='空的话， 就是自增序列', required=False)
    stags = serializers.CharField(label="文章标签的字符串", help_text='中间用空格隔开', required=False)

    class Meta:
        model = PlayList
        fields = ('lid', 'name', 'stags', 'description')

    def create(self, validated_data):

        playlist = PlayList.objects.create(
            lid=validated_data['lid'],
            name=validated_data['name'],
            description=validated_data['description'],
        )

        try:
            tags = validated_data['stags']
            for tag in tags.split(' '):
                tag, created = Tag.objects.update_or_create(name=tag)
                playlist.tags.add(tag)

            playlist.stags = validated_data['stags']
        except Exception as e:
            playlist.stags = str(e)

        return playlist


class PlayListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('lid', 'tracks')

    def update(self, instance, validated_data):
        for track in validated_data['tracks']:
            instance.tracks.add(track)

        return instance