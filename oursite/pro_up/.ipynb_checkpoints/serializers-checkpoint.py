from rest_framework import serializers
from .models import Pro_info
from sup_med.models import Sup_info


class ThumbnailImageField(serializers.ImageField):
    """
    从 easy_thumbnails.fields.ThumbnailerImageField 字段类型中解析出缩略图信息
    """

    def __init__(self, *args, **kwargs):
        self.size_alias = kwargs.pop('size_alias', 'large')
        kwargs['read_only'] = True
        super(ThumbnailImageField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        try:
            return value[self.size_alias].url
        except Exception:
            return None
         
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pro_info
        fields = '__all__'

class Pro_upSerializer(serializers.ModelSerializer):
    #thumb = ThumbnailImageField(source="p_picture", size_alias='medium')
    class Meta:
        model = Pro_info
        fields = ('pid','category','pname','ptype','price','psize','symptoms','pusage','para','problems','pkeyword','address','stock','sales')
      
class Pro_searchSerializer(serializers.ModelSerializer):
    #thumb = ThumbnailImageField(source="p_picture", size_alias='medium')
    class Meta:
        model = Pro_info
        fields = ('pid','pname','price','sid','sales')

class Pro_clickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pro_info
        fields = ('pid', 'sid', 'category','pname','ptype','price','psize','symptoms','pusage','para','problems','pkeyword','address','stock','sales')

class Pro_newSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pro_info
        fields = ('pid', 'category','pname','ptype','price','psize','symptoms','pusage','para','problems','pkeyword','address','stock','p_picture','sales')  

     
#class test(serializers.ModelSerializer):
    