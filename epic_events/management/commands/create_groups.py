from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create custom groups'

    def handle(self, *args, **options):
        # Création du groupe "Commercial" et attribuer des permissions
        commercial_group, _ = Group.objects.get_or_create(name='Commercial')
        # Ajout des permissions nécessaires
        add_commercial_client_permission = Permission.objects.get(codename='add_client', content_type__app_label='epic_events')
        change_commercial_client_permission = Permission.objects.get(codename='change_client', content_type__app_label='epic_events')
        view_commercial_client_permission = Permission.objects.get(codename='view_client', content_type__app_label='epic_events')
        add_commercial_event_permission = Permission.objects.get(codename='add_event', content_type__app_label='epic_events')
        view_commercial_event_permission = Permission.objects.get(codename='view_event', content_type__app_label='epic_events')
        # Ajout des permissions au groupe Commercial
        commercial_group.permissions.add(add_commercial_client_permission, change_commercial_client_permission, view_commercial_client_permission, add_commercial_event_permission, view_commercial_event_permission)
        
        # Création du groupe "Gestion" et attribuer des permissions
        gestion_group, _ = Group.objects.get_or_create(name='Gestion')
        # Ajout des permissions nécessaires
        add_gestion_contract_permission = Permission.objects.get(codename='add_contract', content_type__app_label='epic_events')
        change_gestion_contract_permission = Permission.objects.get(codename='change_contract', content_type__app_label='epic_events')
        view_gestion_contract_permission = Permission.objects.get(codename='view_contract', content_type__app_label='epic_events')
        delete_gestion_contract_permission = Permission.objects.get(codename='delete_contract', content_type__app_label='epic_events')
        add_gestion_event_permission = Permission.objects.get(codename='change_event', content_type__app_label='epic_events')
        view_gestion_event_permission = Permission.objects.get(codename='view_event', content_type__app_label='epic_events')
        delete_gestion_event_permission = Permission.objects.get(codename='delete_event', content_type__app_label='epic_events')
        # Ajout des permissions au groupe Gestion
        gestion_group.permissions.add(add_gestion_contract_permission, change_gestion_contract_permission, view_gestion_contract_permission, delete_gestion_contract_permission, add_gestion_event_permission, view_gestion_event_permission, delete_gestion_event_permission)

        # Création du groupe "Support" et attribuer des permissions
        support_group, _ = Group.objects.get_or_create(name='Support')
        # Ajouter des permissions nécessaires
        view_support_event_permission = Permission.objects.get(codename='view_event', content_type__app_label='epic_events')
         # Ajout des permissions au groupe Gestion
        support_group.permissions.add(view_support_event_permission)

        self.stdout.write(self.style.SUCCESS('Groups and permissions created successfully'))
