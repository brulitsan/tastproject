from django.db import transaction
from django.http import Http404
from drf_yasg.inspectors import ViewInspector
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet

from links.api.serializers import LinkCreateSerializer, LinkSerializer, CollectionSerializer, LinkCollectionSerializer
from links.dependencies import get_user_link_data, type_link
from links.models import Link, Collection, LinkCollection

from rest_framework import generics, status, mixins

from links.schemas import LinkSchema, LinksCollectionsSchema


class LinkCreateView(generics.CreateAPIView):
    serializer_class = LinkCreateSerializer
    permission_classes = [IsAuthenticated]
    inspector_class = ViewInspector

    def perform_create(self, serializer: LinkCreateSerializer) -> Response:
        user = self.request.user
        link = LinkSchema(user=user, **serializer.validated_data)
        link_data = get_user_link_data(user, link.url)
        link_data = type_link(link_data).model_dump()
        serializer.save(**link_data)
        return Response(status=status.HTTP_201_CREATED)


class UserLinkListAPIView(generics.ListAPIView):
    serializer_class = LinkSerializer
    inspector_class = ViewInspector

    def get_queryset(self):
        user = self.request.user
        return Link.objects.filter(user=user)


class LinkViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]
    inspector_class = ViewInspector

    def get_user(self):
        return self.request.user

    def get_object(self):
        user = self.get_user()
        link_id = self.kwargs.get('link_id')
        try:
            link = Link.objects.get(id=link_id, user=user)
        except Link.DoesNotExist:
            raise Http404
        return link

    def get_queryset(self):
        user = self.get_user()
        return Link.objects.filter(user=user)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)


class CollectionViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
    inspector_class = ViewInspector

    def get_user(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        user = self.get_user()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        user = self.get_user()
        collection_id = self.kwargs.get('collection_id')
        try:
            collection = Collection.objects.get(id=collection_id, user=user)
        except Collection.DoesNotExist:
            raise Http404
        return collection

    def get_queryset(self):
        user = self.get_user()
        return Collection.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LinkCollectionViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            GenericViewSet):
    queryset = LinkCollection.objects.all()
    serializer_class = LinkCollectionSerializer
    permission_classes = [IsAuthenticated]
    inspector_class = ViewInspector

    def get_user(self):
        return self.request.user

    def get_queryset(self):
        user = self.request.user
        return LinkCollection.objects.filter(collection__user=user)

    def get_collection_and_link(self, link_collection_schema):
        user = self.get_user()
        try:
            collection = Collection.objects.get(user=user, id=link_collection_schema.collection_id)
            link = Link.objects.get(id=link_collection_schema.link_id)
            return collection, link
        except (Collection.DoesNotExist, Link.DoesNotExist):
            return None, None

    @action(methods=['post'], detail=False, url_path='add_link')
    def add_link(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        link_collection_schema = LinksCollectionsSchema.model_validate(serializer.validated_data)
        collection, link = self.get_collection_and_link(link_collection_schema)
        if collection and link:
            LinkCollection.objects.create(collection=collection, link=link)
            return Response(status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, url_path=r'remove_link/(?P<collection_pk>\d+)/(?P<link_pk>\d+)')
    def remove_link(self, request, collection_pk, link_pk):
        collection = Collection.objects.get(id=collection_pk)
        link = Link.objects.get(id=link_pk)

        LinkCollection.objects.filter(collection=collection, link=link).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
