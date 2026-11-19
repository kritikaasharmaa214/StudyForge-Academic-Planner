"""Strict request validation; never interpolate user inputs into SQL."""
import datetime
import re

class ValidationError(ValueError):
    pass

def text(value, field, max_length=120):
    if not isinstance(value, str) or not value.strip() or len(value.strip()) > max_length:
        raise ValidationError(f'{field} must be 1–{max_length} characters')
    return value.strip()

def integer(value, field, minimum, maximum):
    if isinstance(value, bool):
        raise ValidationError(f'{field} must be an integer')
    try:
        result = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{field} must be an integer') from None
    if str(result) != str(value) and not (type(value) is int):
        raise ValidationError(f'{field} must be an integer')
    if not minimum <= result <= maximum:
        raise ValidationError(f'{field} must be between {minimum} and {maximum}')
    return result

def number(value, field, minimum, maximum):
    if isinstance(value, bool):
        raise ValidationError(f'{field} must be a number')
    try:
        result = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{field} must be a number') from None
    if not minimum <= result <= maximum:
        raise ValidationError(f'{field} must be between {minimum} and {maximum}')
    return result

def date(value, field):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValidationError(f'{field} must be YYYY-MM-DD')
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        raise ValidationError(f'{field} is not a valid date') from None
    return value

def choice(value, field, options):
    if value not in options:
        raise ValidationError(f'{field} must be one of: {", ".join(options)}')
    return value

def color(value):
    if not isinstance(value,str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',value):
        raise ValidationError('color must be a 6-digit hex color')
    return value

def mapping(obj):
    if not isinstance(obj, dict):
        raise ValidationError('JSON request must be an object')
    return obj
