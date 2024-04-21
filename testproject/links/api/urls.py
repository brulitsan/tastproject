from django.urls import path, include
from rest_framework import routers

from links.api.views import LinkCreateView, LinkViewSet, CollectionViewSet, LinkCollectionViewSet

router = routers.DefaultRouter()
router.register(r'link-operation', LinkViewSet)
router.register(r'collection-operation', CollectionViewSet)
router.register('link_collection-operations', LinkCollectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_links/', LinkCreateView.as_view()),
    path('link_collection-operations/remove_link/<int:collection_pk>/<int:link_pk>/',
         LinkCollectionViewSet.as_view({'delete': 'remove_link'})),
]
