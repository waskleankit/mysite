# from wagtail.api.v2.endpoints import PagesAPIEndpoint
# from wagtail.api.v2.router import WagtailAPIRouter
# from wagtail.images.api.v2.endpoints import ImagesAPIEndpoint
# from wagtail.documents.api.v2.endpoints import DocumentsAPIEndpoint

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet


api_router = WagtailAPIRouter('wagtailapi')

# api_router.register_endpoint('pages',PagesAPIEndpoint)
# api_router.register_endpoint('images',ImagesAPIEndpoint)
# api_router.register_endpoint('documents',DocumentsAPIEndpoint)
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)