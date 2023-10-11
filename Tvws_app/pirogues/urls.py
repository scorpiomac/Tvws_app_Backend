from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from .views import CustomTokenObtainPairView





urlpatterns = [
    path('pirogue/', PirogueListCreateView.as_view(), name='piroguer-list-create'),
    path('pirogue/<int:pk>/', PirogueRetrieveUpdateDestroyView.as_view(), name='piroguer-retrieve-update-destroy'),

    path('position/', PositionListCreateView.as_view(), name='piroguer-list-create'),
    path('position/<int:pk>/', PositionRetrieveUpdateDestroyView.as_view(), name='piroguer-retrieve-update-destroy'),
    path('connected-users/<int:pk>/', ConnectedUsersPositionAPI.as_view(), name='connected-users'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', PirogueRegistration.as_view(), name='register'),
    path('last_positions/', LastPositionsView.as_view(), name='last_positions'),
    path('send_position/', PositionAPIView.as_view(), name='send_position'),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
