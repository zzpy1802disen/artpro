from rest_framework import serializers, viewsets

from api.art import ArtSerializer
from art.models import Category


# 声明分类模型序列化类
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    # arts = serializers.StringRelatedField(many=True)
    # 引入其它的序列化
    arts = ArtSerializer(many=True,read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'add_time', 'arts')


# 声明分类显示视图集
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
