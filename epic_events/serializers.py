from rest_framework import serializers
from epic_events.models import Client, User, Contract, Event



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'full_name', 'email', 'phone', 'company_name', 'contact', 'creation_date', 'last_update']
        read_only_fields = ['creation_date', 'last_update']

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'client', 'commercial_contact', 'total_amount', 'amount_due', 'creation_date', 'status']
        read_only_fields = ['creation_date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'groups']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'contract', 'event_name', 'event_date_start', 'event_date_end', 'location', 'attendees', 'notes', 'support_contact']

