from flask import Flask, jsonify, request


app = Flask(__name__)

parts = [
    {
        "id": 1,
        "name": "RAM",
        "brand": "Corsair",
        "quantity": 10,
        "price": 45.99,
    },
    {
        "id": 2,
        "name": "SSD",
        "brand": "Samsung",
        "quantity": 8,
        "price": 79.99,
    },
    {
        "id": 3,
        "name": "CPU",
        "brand": "Intel",
        "quantity": 5,
        "price": 199.99,
    },
    {
        "id": 4,
        "name": "Keyboard",
        "brand": "Logitech",
        "quantity": 12,
        "price": 29.99,
    },
]


def validate_part(data):
    """Return an error message when an inventory item is invalid."""
    required_fields = {"name", "brand", "quantity", "price"}
    missing_fields = required_fields - data.keys()

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        return f"Missing required fields: {missing}"

    if not isinstance(data["name"], str) or not data["name"].strip():
        return "name must be a non-empty string"

    if not isinstance(data["brand"], str) or not data["brand"].strip():
        return "brand must be a non-empty string"

    if not isinstance(data["quantity"], int) or isinstance(data["quantity"], bool):
        return "quantity must be a non-negative integer"

    if data["quantity"] < 0:
        return "quantity must be a non-negative integer"

    if (
        not isinstance(data["price"], (int, float))
        or isinstance(data["price"], bool)
        or data["price"] < 0
    ):
        return "price must be a non-negative number"

    return None


@app.route("/", methods=["GET"])
def welcome():
    return jsonify(
        {
            "message": "Welcome to the Computer Inventory Management API",
            "instructions": "Use /parts to retrieve or add inventory items.",
        }
    ), 200


@app.route("/parts", methods=["GET"])
def get_parts():
    return jsonify(parts), 200


@app.route("/parts", methods=["POST"])
def add_part():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    error = validate_part(data)
    if error:
        return jsonify({"error": error}), 400

    new_part = {
        "id": max((part["id"] for part in parts), default=0) + 1,
        "name": data["name"].strip(),
        "brand": data["brand"].strip(),
        "quantity": data["quantity"],
        "price": data["price"],
    }
    parts.append(new_part)

    return jsonify(new_part), 201


if __name__ == "__main__":
    app.run(port=5000)
