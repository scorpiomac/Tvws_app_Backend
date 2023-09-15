from django.shortcuts import render
from django.db.models import Subquery, OuterRef
from django.utils import timezone

# Create your views here.
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView

class PirogueListCreateView(generics.ListCreateAPIView):
    queryset = Pirogue.objects.all()
    serializer_class = PirogueSerializer

class PirogueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pirogue.objects.all()
    serializer_class = PirogueSerializer

class PositionListCreateView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class PositionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class ConnectedUsersPositionAPI(APIView):
    def get(self, request, *args, **kwargs):
        requesting_pirogue = request.user

        # Subquery pour récupérer la dernière position de chaque utilisateur
        latest_positions = Position.objects.filter(
            pirogue=OuterRef('pirogue')
        ).order_by('-timestamp').values('latitude', 'longitude')[:1]

        # Récupérer les positions des autres utilisateurs connectés
        positions = Position.objects.filter(
            pirogue__in=Pirogue.objects.exclude(pk=requesting_pirogue.pk),
            timestamp__gte=timezone.now() - timezone.timedelta(minutes=15)  # Filtrer les positions des dernières 15 minutes
        ).annotate(
            last_position_latitude=Subquery(latest_positions, output_field=models.FloatField()),
            last_position_longitude=Subquery(latest_positions, output_field=models.FloatField())
        ).values('pirogue__username', 'last_position_latitude', 'last_position_longitude')

        return Response(positions, status=status.HTTP_200_OK)
