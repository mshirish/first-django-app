from rest_framework import serializers
from .models import Post, Tag

class TagSerializer(serializers.ModelSerializer): #ModelSerializer works exactly like ModelForm — it introspects your model and generates fields automatically.
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True) #nested serializer. Instead of returning tag IDs, it returns full tag objects. many=True because it's a list. 
    author = serializers.StringRelatedField(read_only=True) #StringRelatedField — calls __str__() on the related object. So author returns "john" instead of 1.


    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'author',
            'tags',
            'published',
            'created_at',
        ]