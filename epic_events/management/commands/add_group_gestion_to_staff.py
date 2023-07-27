from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = 'Give is_staff status to all users in the Gestion group'

    def handle(self, *args, **options):
        # obtenir le groupe
        group = Group.objects.get(name='Gestion')

        # donner le statut de personnel à tous les utilisateurs du groupe
        for user in group.user_set.all():
            user.is_staff = True
            user.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated group users'))
