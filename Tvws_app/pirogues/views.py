from django.shortcuts import render
from django.db.models import Subquery, OuterRef, F, Func, Max
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from datetime import timedelta

# Create your views here.
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

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
    def get(self, request,pk):
        # current_user = request.user.id
        current_user = self.kwargs.get('pk')
        # Calcul de la date limite pour considérer un utilisateur comme connecté
        threshold_timestamp = timezone.now() - timedelta(minutes=15)

        positions = Position.objects.exclude(pirogue=current_user).filter(
            timestamp__gte=threshold_timestamp
        ).annotate(
            latest_timestamp=Max('timestamp')
        ).filter(timestamp=F('latest_timestamp'))
        
        # Subrequête pour obtenir le dernier timestamp pour chaque pirogue
        latest_timestamps_subquery = Position.objects.filter(
            pirogue=OuterRef('pirogue')
        ).order_by('-timestamp').values('timestamp')[:1]

        # Récupération des positions correspondant aux derniers timestamps
        positions = Position.objects.filter(
            timestamp__in=Subquery(latest_timestamps_subquery)
        )

        # Filtrer pour obtenir uniquement les positions des utilisateurs connectés
        positions = positions.exclude(pirogue=current_user).filter(
            timestamp__gte=threshold_timestamp,
            is_visible=True
        )
        
         # Récupérer les alertes "mayday" de moins de 5 minutes
        current_time = timezone.now()
        five_minutes_ago = current_time - timedelta(minutes=5)
        alertes = Alerte.objects.filter(
            type_alerte='mayday',
            timestamp__gte=five_minutes_ago
        )

        # Serializer les données
        serializer = PositionSerializer(positions, many=True)
        alertes_serializer = AlerteSerializer(alertes, many=True)

        # Retourner les données
        response_data = {
            'position': serializer.data,
            'alertes': alertes_serializer.data,
        }

        serializer = PositionSerializer(positions, many=True)
        return Response(response_data, status=status.HTTP_200_OK)
    


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PirogueRegistration(APIView):
    def post(self, request):
        serializer = PirogueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LastPositionsView(APIView):
    def get(self, request):
        current_user = request.user

        # Calcul de la date limite pour considérer un utilisateur comme connecté
        threshold_timestamp = timezone.now() - timedelta(minutes=15)

        # Subquery pour obtenir la dernière position de chaque pirogue
        latest_positions = Position.objects.filter(
            pirogue=OuterRef('pirogue')
        ).order_by('-timestamp').values('timestamp')[:1]

        # Récupération des dernières positions de chaque pirogue
        positions = Position.objects.annotate(
            time_since_last_position=timezone.now() - Subquery(latest_positions)
        ).filter(
            
            time_since_last_position__lte=timedelta(minutes=15)
        )

        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    
    
class PositionAPIView(APIView):
    def post(self, request):
        # Récupérer les données de la requête
        pirogue=request.data.get('pirogue')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        if request.data.get('is_visible')=="false":
            is_visible= False
        else:
            is_visible= True
        vitesse = request.data.get('vitesse')
         # Vérifier que la pirogue existe
        try:
            pirogue = Pirogue.objects.get(pk=pirogue)
        except Pirogue.DoesNotExist:
            return Response({'error': 'Pirogue not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Créer la position
        position = Position.objects.create(
            pirogue=pirogue,
            latitude=latitude,
            longitude=longitude,
            is_visible=is_visible,
            vitesse=vitesse,
        )

        # Calculer le temps de transmission
        position.calculate_temps_transmission()
        position.save()

        # Récupérer les alertes "mayday" de moins de 5 minutes
        current_time = timezone.now()
        five_minutes_ago = current_time - timedelta(minutes=5)
        alertes = Alerte.objects.filter(
            type_alerte='mayday',
            timestamp__gte=five_minutes_ago,
        
        )
        
    

        # Serializer les données
        position_serializer = PositionSerializer(position)
        alertes_serializer = AlerteSerializer(alertes, many=True)

        # Retourner les données
        response_data = {
            'position': position_serializer.data,
            'alertes': alertes_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)