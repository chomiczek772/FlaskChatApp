def toJson(obj):
    if isinstance(obj, ({}.__class__, {1, }.__class__, None.__class__)):
        return obj
    if isinstance(obj, [].__class__):
        return [toJson(x) for x in obj]
    else:
        return obj.toJson()
