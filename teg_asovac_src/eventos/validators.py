from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_ced_passport(data):
    dni_data = data
    return data

def validate_phone_office(phone):
    phone_data = phone
    return phone

def validate_phone_personal(phone_per):
    phone_personal_data = phone_per
    return phone_per

def validate_cap_asovac(cap_asovac):
    cap_asovac_data = cap_asovac
    return cap_asovac
