import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        return str(obj) if isinstance(obj, Decimal) else super().default(obj)
