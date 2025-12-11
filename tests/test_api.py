import pytest
import struct
import uuid
import src.triangulator.api as api_module
from src.triangulator.api import app, point_set_storage
from src.triangulator.point_set import PointSet
from src.triangulator.triangulator import Triangulator

class TestAPI:

    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        point_set_storage.clear()
        with app.test_client() as client:
            yield client

    def test_create_pointset_success(self, client):
        ps = PointSet([(0.0, 0.0), (1.0, 1.0)])
        binary_data = ps.serialize()

        response = client.post('/pointset', data=binary_data)

        assert response.status_code == 201
        data = response.get_json()
        assert 'pointSetId' in data
        assert data['pointSetId'] in point_set_storage

    def test_create_pointset_bad_request(self, client):
        response = client.post('/pointset', data=b'\x00\x00')
        assert response.status_code == 400

    def test_triangulation_valid_request(self, client):
        ps = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
        ps_id = str(uuid.uuid4())
        point_set_storage[ps_id] = ps

        response = client.get(f'/triangulation/{ps_id}')

        assert response.status_code == 200
        assert response.mimetype == 'application/octet-stream'
        
        data = response.data
        num_triangles = struct.unpack('>I', data[:4])[0]
        assert num_triangles == 1

    def test_triangulation_pointset_not_found(self, client):
        response = client.get('/triangulation/non-existent-id')
        assert response.status_code == 404

    def test_triangulation_server_error(self, client, monkeypatch):
        ps = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
        ps_id = str(uuid.uuid4())
        point_set_storage[ps_id] = ps
        
        def mock_triangulate_error(self):
            raise RuntimeError("Algorithm failed")
        
        monkeypatch.setattr(Triangulator, 'triangulate_to_bytes', mock_triangulate_error)

        response = client.get(f'/triangulation/{ps_id}')
        assert response.status_code == 500

    def test_database_unavailable(self, client, monkeypatch):
        monkeypatch.setattr(api_module, 'db_available', False)

        response = client.post('/pointset', data=b'')
        assert response.status_code == 503

        response = client.get('/triangulation/id_not_matter')
        assert response.status_code == 503
