from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import AlerteListCreateView, AlerteRetrieveUpdateDestroyView

urlpatterns = [
    path('alertes/', AlerteListCreateView.as_view(), name='alerte-list-create'),
    path('alertes/<int:pk>/', AlerteRetrieveUpdateDestroyView.as_view(), name='alerte-retrieve-update-destroy'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
