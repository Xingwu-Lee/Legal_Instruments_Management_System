# middlewares.py
from flask import request, jsonify

def check_empty_json(request):
    if request.method in ["POST", "PUT", "PATCH"]:
        data = request.get_json()
        if data is not None:
            empty_fields = [field for field, value in data.items() if not value]
            if empty_fields:
                return jsonify({"error": "Fields cannot be empty", "empty_fields": empty_fields}), 400
    return None
