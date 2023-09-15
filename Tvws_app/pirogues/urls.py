from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('pirogue/', PirogueListCreateView.as_view(), name='piroguer-list-create'),
    path('pirogue/<int:pk>/', PirogueRetrieveUpdateDestroyView.as_view(), name='piroguer-retrieve-update-destroy'),

    path('position/', PositionListCreateView.as_view(), name='piroguer-list-create'),
    path('position/<int:pk>/', PositionRetrieveUpdateDestroyView.as_view(), name='piroguer-retrieve-update-destroy'),
    path('connected-users/', ConnectedUsersPositionAPI.as_view(), name='connected-users'),



]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
