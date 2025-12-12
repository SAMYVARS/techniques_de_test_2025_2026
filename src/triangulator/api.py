"""API module for the Triangulator service."""

import uuid

from flask import Flask, Response, jsonify, request

from .point_set import PointSet
from .triangulator import Triangulator

app = Flask(__name__)

point_set_storage = {}

db_available = True

@app.route('/pointset', methods=['POST'])
def create_pointset():
    """Create a new PointSet from binary data."""
    if not db_available:
        return jsonify({'error': 'Database unavailable'}), 503

    data = request.data
    try:
        point_set = PointSet.deserialize(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        return jsonify({'error': 'Invalid binary format'}), 400

    point_set_id = str(uuid.uuid4())
    point_set_storage[point_set_id] = point_set
    
    return jsonify({'pointSetId': point_set_id}), 201

@app.route('/pointset/<point_set_id>', methods=['GET'])
def get_pointset(point_set_id):
    """Retrieve a PointSet by its ID."""
    if not db_available:
        return jsonify({'error': 'Database unavailable'}), 503
        
    point_set = point_set_storage.get(point_set_id)
    if not point_set:
        return jsonify({'error': 'PointSet not found'}), 404
        
    return Response(point_set.serialize(), mimetype='application/octet-stream')

@app.route('/triangulation/<point_set_id>', methods=['GET'])
def get_triangulation(point_set_id):
    """Perform triangulation on a PointSet."""
    if not db_available:
        return jsonify({'error': 'PointSetManager unavailable'}), 503

    point_set = point_set_storage.get(point_set_id)
    if not point_set:
        return jsonify({'error': 'PointSet not found'}), 404

    try:
        triangulator = Triangulator(point_set)
        binary_result = triangulator.triangulate_to_bytes()
        return Response(binary_result, mimetype='application/octet-stream')
    except RuntimeError:
        return jsonify({'error': 'Triangulation failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
