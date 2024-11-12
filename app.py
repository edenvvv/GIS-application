from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
areas = []
active_users = 0  # Track active users


def calculate_area_size(coordinates):
    # Calculate area in square kilometers
    try:
        poly = Polygon(coordinates)
        proj = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        projected_poly = transform(proj.transform, poly)
        area_km2 = projected_poly.area / 1_000_000
        return area_km2
    except ValueError as e:
        raise ValueError(f"Invalid coordinates: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred during area calculation: {str(e)}")


@app.route("/save_area", methods=["POST"])
def save_area():
    try:
        area_data = request.json
        area_size_km2 = calculate_area_size(area_data['coordinates'])
        area_data["size_km2"] = area_size_km2
        areas.append(area_data)
        return jsonify(area_data), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while saving the area", "details": str(e)}), 500


@app.route("/areas", methods=["GET"])
def get_areas():
    try:
        return jsonify(areas), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve areas", "details": str(e)}), 500


@socketio.on("draw_polygon")
def handle_draw_polygon(data):
    try:
        emit("draw_polygon", data, broadcast=True)
    except ValueError as e:
        emit("error", {"error": str(e)})
    except Exception as e:
        emit("error", {"error": f"An unexpected error occurred: {str(e)}"})


@socketio.on("user_connected")
def handle_user_connected():
    global active_users
    try:
        active_users += 1
        emit("user_connected", {"active_users": active_users}, broadcast=True)
        print(f"New user connected. Active users: {active_users}")
    except Exception as e:
        emit("error", {"error": f"An unexpected error occurred: {str(e)}"})


@socketio.on("user_disconnected")
def handle_user_disconnected():
    global active_users
    try:
        active_users -= 1
        emit("user_disconnected", {"active_users": active_users}, broadcast=True)
        print(f"User disconnected. Active users: {active_users}")
    except Exception as e:
        emit("error", {"error": f"An unexpected error occurred: {str(e)}"})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5678, allow_unsafe_werkzeug=True)
