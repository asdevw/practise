from django.core.exceptions import ValidationError
from django.utils import timezone
def validate_age(value):
    age = abs((timezone.now().date() - value)).days
    if age < (18 * 365):
        raise ValidationError('no no no no')