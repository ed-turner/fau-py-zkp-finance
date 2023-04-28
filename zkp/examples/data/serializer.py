"""This is all functionality to serialize all code"""

from datetime import datetime, date


def json_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} is not serializable')
