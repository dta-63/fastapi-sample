import datetime
from bson import ObjectId


def serialize(obj):
    """
    Serialize object supporting mongo object id and datetimes
    """
    if '_id' in obj:
        obj['id'] = str(obj['_id'])
        obj.pop('_id')
    if isinstance(obj, list):
        return [serialize(item) for item in obj]
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S.%f")
    return obj
