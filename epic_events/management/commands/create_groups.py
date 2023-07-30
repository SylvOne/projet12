from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create custom groups'

    def handle(self, *args, **options):
        # Création du groupe "Commercial"
        commercial_group, _ = Group.objects.get_or_create(name='Commercial')
        # Création du groupe "Gestion"
        gestion_group, _ = Group.objects.get_or_create(name='Gestion')

        # Création du groupe "Support"
        support_group, _ = Group.objects.get_or_create(name='Support')

        self.stdout.write(self.style.SUCCESS('Groups and permissions créé avec succès'))
