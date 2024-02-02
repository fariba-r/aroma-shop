from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission


@receiver(post_migrate, sender=None)
def handle_group(sender, **kwargs):

    anonymous, created = Group.objects.get_or_create(name="anonymous")
    anonymous_list=["view_image","view_category","view_product","view_comment","view_like","view-detail"]
    for perm in Permission.objects.filter(codename__in=anonymous_list):
        anonymous.permissions.add(perm)
    autenticated, created = Group.objects.get_or_create(name="autenticated")
    autenticated_list=["delete_order","add_order","view_city","view_province"]+anonymous_list
    for perm in Permission.objects.filter(codename__contains='comment'):
        autenticated.permissions.add(perm)
    for perm in Permission.objects.filter(codename__contains='like'):
        autenticated.permissions.add(perm)
    for perm in Permission.objects.filter(codename__in=autenticated_list):
        autenticated.permissions.add(perm)

    master_product, created = Group.objects.get_or_create(name="master_product")
    for perm in Permission.objects.filter(codename__contains='product'):
        master_product.permissions.add(perm)
    for perm in Permission.objects.filter(codename__contains='category'):
        master_product.permissions.add(perm)
    for perm in Permission.objects.filter(codename__contains='discount'):
        master_product.permissions.add(perm)
    for perm in Permission.objects.filter(name='autenticated'):
        master_product.permissions.add(perm)

    controller, created = Group.objects.get_or_create(name="controller")

    controler_permissions = Permission.objects.filter(content_type__app_label='order')
    controller.permissions.set(controler_permissions)
    controler_permissions = Permission.objects.filter(content_type__app_label='member')
    controller.permissions.set(controler_permissions)

    operator, created = Group.objects.get_or_create(name="operator")
    for perm in Permission.objects.filter(codename__contains='view'):
        operator.permissions.add(perm)
    admin_group,created = Group.objects.get_or_create(name='Administrators')  # Adjust the group name if needed
    all_permissions = Permission.objects.all()  # Get all available permissions
    admin_group.permissions.set(all_permissions)
