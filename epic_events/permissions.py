from rest_framework import permissions



class IsCommercialOrContactClientOrReadOnly(permissions.BasePermission):
    """
    Cette permission autorise seulement l'update d'un client,
    si le demandeur est contact de celui-ci
    """
    def has_permission(self, request, view):
        # La création d'un nouveau client est seulement autorisé
        # au groupe Commercial.
        if view.action == 'create':
            return request.user.groups.filter(name='Commercial').exists()

        return True

    def has_object_permission(self, request, view, obj):
        # La lecture est autorisé pour tout le monde,
        if request.method in permissions.SAFE_METHODS:
            return True

        # L'écriture est par contre autorisé uniquement pour le contact du client.
        return obj.contact == request.user


class IsGestionOrCommercialContactOrReadOnly(permissions.BasePermission):
    """
    Cette permission autorise la création d'un contrat uniquement pour le groupe "Gestion"
    et la mise à jour du contrat pour le groupe "Gestion" et pour le contact commercial du contrat
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.groups.filter(name='Gestion').exists()
        elif view.action in ['update', 'partial_update']:
            # Pour l'action 'update', nous devons vérifier si l'utilisateur est le contact commercial du contrat,
            # mais l'objet du contrat n'est pas disponible à ce stade.
            # Nous retournons donc True ici et effectuons la vérification dans `has_object_permission`.
            return True

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action in ['update', 'partial_update']:
            return request.user == obj.commercial_contact or request.user.groups.filter(name='Gestion').exists()

        return True


class IsGestionGroup(permissions.BasePermission):
    """
    Permission pour autoriser uniquement les utilisateurs du groupe Gestion
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Gestion').exists()


class EventPermissions(permissions.BasePermission):
    """
    Cette permission autorise :
    - La création d'un événement seulement par un utilisateur du groupe "Commercial" s'il est le contact commercial du contrat associé à l'événement.
    - La mise à jour de l'événement seulement pour le groupe "Gestion" et "Support".
    - La lecture pour tous les utilisateurs.
    """

    def has_permission(self, request, view):
        # Les utilisateurs de tous les groupes peuvent lire les informations
        if request.method in permissions.SAFE_METHODS:
            return True

        # Seuls les utilisateurs du groupe "Commercial" peuvent créer un événement
        if view.action == 'create':
            return request.user.groups.filter(name='Commercial').exists()
        
        # Les utilisateurs des groupes "Gestion" et "Support" peuvent mettre à jour un événement
        elif view.action in ['update', 'partial_update']:
            return request.user.groups.filter(name__in=['Gestion', 'Support']).exists()

        return False

    def has_object_permission(self, request, view, obj):
        # Les utilisateurs de tous les groupes peuvent lire les informations
        if request.method in permissions.SAFE_METHODS:
            return True

        # Les utilisateurs des groupes "Gestion" peuvent mettre à jour n'importe quel événement
        if view.action in ['update', 'partial_update'] and request.user.groups.filter(name='Gestion').exists():
            return True

        # Les utilisateurs du groupe "Support" peuvent mettre à jour un événement s'ils sont le support_contact
        if view.action in ['update', 'partial_update'] and request.user.groups.filter(name='Support').exists():
            return obj.support_contact == request.user

        return False