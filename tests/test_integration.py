import pytest
import struct
from src.triangulator.api import app, point_set_storage
from src.triangulator.point_set import PointSet
import src.triangulator.api as api_module

class TestIntegration:

    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        point_set_storage.clear()
        api_module.db_available = True
        
        with app.test_client() as client:
            yield client

    def test_recuperation_reussie(self, client):
        ps = PointSet([(0.0, 0.0), (1.0, 1.0)])
        
        binary_data = ps.serialize()
        post_response = client.post('/pointset', data=binary_data)
        assert post_response.status_code == 201
        point_set_id = post_response.get_json()['pointSetId']

        get_response = client.get(f'/pointset/{point_set_id}')

        assert get_response.status_code == 200
        assert get_response.data == binary_data

    def test_service_indisponible(self, client, monkeypatch):
        monkeypatch.setattr(api_module, 'db_available', False)

        response = client.get('/pointset/some-id')
        assert response.status_code == 503
        assert response.get_json() == {'error': 'Database unavailable'}

    def test_enchainement_complet(self, client):
        points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        ps = PointSet(points)
        binary_data = ps.serialize()

        upload_response = client.post('/pointset', data=binary_data)
        assert upload_response.status_code == 201
        point_set_id = upload_response.get_json()['pointSetId']

        triangulation_response = client.get(f'/triangulation/{point_set_id}')
        
        assert triangulation_response.status_code == 200
        assert triangulation_response.mimetype == 'application/octet-stream'
        
        result_data = triangulation_response.data
        num_triangles = struct.unpack('>I', result_data[:4])[0]
        assert num_triangles == 1

        assert len(result_data) == 28
