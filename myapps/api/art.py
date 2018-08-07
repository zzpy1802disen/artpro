from rest_framework import serializers, viewsets
from art.models import Art


# 声明分类模型序列化类
class ArtSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Art
        fields = ('id', 'title', 'summary','content', 'author', 'cover', 'category')


# 声明分类显示视图集
class ArtViewSet(viewsets.ModelViewSet):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer
