from django.core.exceptions import ValidationError


def check_shaba_validator(number):
    if len(number) != 24:
        raise ValidationError("شماره شبا وارد شده معتبر نیست")

