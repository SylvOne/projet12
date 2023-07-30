from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Create default users and add them to their respective groups'

    def handle(self, *args, **options):
        # Création de l'utilisateur "userCommercial" et ajout au groupe "Commercial"
        user_commercial, _ = User.objects.get_or_create(username='userCommercial', email='usercommercial@example.com')
        user_commercial.set_password('passwordcomm')
        user_commercial.save()
        commercial_group, _ = Group.objects.get_or_create(name='Commercial')
        commercial_group.user_set.add(user_commercial)

        # Création de l'utilisateur "userGestion" et ajout au groupe "Gestion"
        user_gestion, _ = User.objects.get_or_create(username='userGestion', email='usergestion@example.com')
        user_gestion.set_password('passwordgest')
        user_gestion.save()
        gestion_group, _ = Group.objects.get_or_create(name='Gestion')
        gestion_group.user_set.add(user_gestion)

        # Création de l'utilisateur "userSupport" et ajout au groupe "Support"
        user_support, _ = User.objects.get_or_create(username='userSupport', email='usersupport@example.com')
        user_support.set_password('passwordsupp')
        user_support.save()
        support_group, _ = Group.objects.get_or_create(name='Support')
        support_group.user_set.add(user_support)

        self.stdout.write(self.style.SUCCESS('Les utilisateurs ont été créés et ajoutés aux groupes correspondants.'))
