from rest_framework import viewsets, serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from epic_events.models import Client, User, Contract, Event
from epic_events.serializers import ClientSerializer, UserSerializer, ContractSerializer, EventSerializer
from epic_events.permissions import IsCommercialOrContactClientOrReadOnly, IsGestionOrCommercialContactOrReadOnly, IsGestionGroup, EventPermissions
from rest_framework.response import Response
import django_filters
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from rest_framework.decorators import action
from django.db.models import Q
from sentry_sdk import capture_exception




class CurrentUserView(APIView):
    """
    View to get the details of the currently logged in user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'company_name']

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsCommercialOrContactClientOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ClientFilter
    
    def destroy(self, request, *args, **kwargs):
        return Response({"error": "Suppression de client non autorisée."}, status=status.HTTP_403_FORBIDDEN)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() 
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsGestionGroup]

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)
        # On exclue le superuser.
        queryset = queryset.exclude(is_superuser=True)
        return queryset
    
    def create(self, request, *args, **kwargs):
        group_name = request.data.get('group')
        # Vérification que le groupe fourni est l'un des groupes autorisés
        if group_name not in ['Gestion', 'Commercial', 'Support']:
            return Response({"error": "Invalid group"}, status=status.HTTP_400_BAD_REQUEST)
        group = get_object_or_404(Group, name=group_name)
        request.data['groups'] = [group.id]
        return super().create(request, *args, **kwargs)
        

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # On vérifie si l'utilisateur à modifier est un superuser.
            if instance.is_superuser:
                # Si l'utilisateur qui fait la demande == le superuser à modifier, alors il aura le droit.
                if request.user != instance:
                    return Response({"error": "Vous ne pouvez pas modifier le superutilisateur"}, status=status.HTTP_403_FORBIDDEN)
            data = request.data.copy()
            group_name = data.get('group')
            if group_name:
                group = get_object_or_404(Group, name=group_name)
                data['groups'] = [group.id]
            serializer = self.get_serializer(self.get_object(), data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            instance = self.get_object()
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        except Exception as e:
            capture_exception(e)
            raise e

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_superuser:
            return Response({"error": "Le superuser ne peut pas être supprimé."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
        

class ContractFilter(django_filters.FilterSet):
    class Meta:
        model = Contract
        fields = {
            'client__full_name': ['exact'],
            'client__email': ['exact'],
            'total_amount': ['exact', 'lt', 'gt'],
            'status': ['exact'],
            'amount_due': ['exact', 'gt'],
        }


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsGestionOrCommercialContactOrReadOnly]
    filterset_class = ContractFilter
    is_contract_view = True

    def destroy(self, request, *args, **kwargs):
        return Response({"error": "Suppression de contrat non autorisée."}, status=status.HTTP_403_FORBIDDEN)

class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'contract__client__full_name': ['exact'],
            'contract__client__email': ['exact'],
            'event_date_start': ['exact', 'lt', 'gt'],
            'event_date_end': ['exact', 'lt', 'gt'],
            'support_contact__username':['exact'],
        }


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventPermissions]
    filterset_class = EventFilter


    def get_queryset(self):
        queryset = super().get_queryset()
        support_contact = self.request.query_params.get('support_contact__username')
        
        if support_contact == 'null':
            queryset = queryset.filter(support_contact__isnull=True)
        elif support_contact:
            queryset = queryset.filter(support_contact__username=support_contact)

        return queryset


    def perform_create(self, serializer):
        try:
            # Vérification si l'utilisateur fait bien parti du groupe Commercial
            if not self.request.user.groups.filter(name='Commercial').exists():
                raise serializers.ValidationError("Seul un utilisateur du groupe 'Commercial' peut créer un événement.")
            
            contract_id = self.request.data.get('contract')
            contract = get_object_or_404(Contract, id=contract_id)

            # Vérification si le contrat est signé
            if not contract.status:
                raise serializers.ValidationError("Vous ne pouvez créer un événement que pour les contrats signés.")
            
            # Vérification si l'utilisateur est le contact commercial pour le contrat concerné
            if self.request.user != contract.commercial_contact:
                raise serializers.ValidationError("Vous devez être le contact commercial pour le contrat associé pour créer un événement.")

            serializer.save(contract=contract)
        
        except Exception as e:
            capture_exception(e)
            raise e
    


    def update(self, request, *args, **kwargs):
        try:
            # Vérification si l'utilisateur qui met à jour l'événement fait bien parti du groupe Gestion ou Support
            if not request.user.groups.filter(name__in=['Gestion', 'Support']).exists():
                raise serializers.ValidationError("Seul un utilisateur du groupe 'Gestion' ou 'Support' peut modifier un événement.")

            # Pour un utilisateur du groupe 'Support', vérifier qu'il est bien le support_contact de l'événement
            if request.user.groups.filter(name='Support').exists():
                instance = self.get_object()
                if instance.support_contact != request.user:
                    raise serializers.ValidationError("Seul le support_contact assigné à l'événement peut le modifier.")

            support_contact_id = request.data.get('support_contact')
            if support_contact_id:
                # Vérification si l'utilisateur assigné comme support_contact fait bien parti du groupe Support
                support_contact = get_object_or_404(User, id=support_contact_id)
                if not support_contact.groups.filter(name='Support').exists():
                    raise serializers.ValidationError(f"L'utilisateur {support_contact_id} n'appartient pas au groupe 'Support'.")
            return super().update(request, *args, **kwargs)
        except Exception as e:
            capture_exception(e)
            raise e

    def destroy(self, request, *args, **kwargs):
        return Response({"error": "Suppression d'événement non autorisée."}, status=status.HTTP_403_FORBIDDEN)



    @action(detail=False, methods=['get'])
    def no_support_contact(self, request):
        no_support_contact_events = Event.objects.filter(support_contact__isnull=True)
        serializer = self.get_serializer(no_support_contact_events, many=True)
        return Response(serializer.data)
