from django.conf import settings
from suds.client import Client

from company.models import Staff


def check_is_active(user):
    return user.is_active


def check_is_ok(user, pk):
    if user.pk == pk:
        return True
    return False


def check_is_location(locations, pk):
    for location in locations:
        if location.pk == pk:
            return True
    return False


def check_is_staff(locations, pk):
    for location in locations:
        staffs = Staff.objects.filter(location=location)
        for staff in staffs:
            if staff.pk == pk:
                return True
        return False


def check_is_staff_by_staff_pk(staff, pk):

    staff = Staff.objects.filter(pk=staff).first()
    if staff.pk == pk:
        return True
    return False

