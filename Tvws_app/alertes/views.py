from rest_framework import generics
from .models import *
from .serializers import *

class AlerteListCreateView(generics.ListCreateAPIView):
    queryset = Alerte.objects.all()
    serializer_class = AlerteSerializer

class AlerteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alerte.objects.all()
    serializer_class = AlerteSerializer
