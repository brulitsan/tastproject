from rest_framework import serializers

from links.models import Link, Collection, LinkCollection


class LinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['url', 'link_type', 'title', 'description', 'image', ]
        read_only_fields = ['link_type', 'title', 'description', 'image', ]


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['url', 'link_type', 'title', 'description', 'image', ]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['user']


class LinkCollectionSerializer(serializers.Serializer):
    collection_id = serializers.IntegerField()
    link_id = serializers.IntegerField()
