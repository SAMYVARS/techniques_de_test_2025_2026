import pytest
from src.triangulator.point_set import PointSet
from src.triangulator.triangulator import Triangulator

class TestTriangulation:

    def test_triangulate_three_points(self):
        point_set = PointSet([
            (0.0, 0.0),
            (1.0, 0.0),
            (0.0, 1.0),
        ])
        triangulator = Triangulator(point_set)

        triangles = triangulator.triangulate()

        assert len(triangles) == 1

    def test_triangulate_four_points_square(self):
        point_set = PointSet([
            (0.0, 0.0),
            (1.0, 0.0),
            (1.0, 1.0),
            (0.0, 1.0),
        ])
        triangulator = Triangulator(point_set)

        triangles = triangulator.triangulate()

        assert len(triangles) == 2

    def test_triangulate_polygon(self):
        point_set = PointSet([
            (0.0, 0.0),
            (2.0, 0.0),
            (2.0, 2.0),
            (1.0, 3.0),
            (0.0, 2.0),
        ])
        triangulator = Triangulator(point_set)

        triangles = triangulator.triangulate()
        n = len(point_set)

        assert len(triangles) == n - 2

    def test_triangulate_less_3_points(self):
        point_set = PointSet([
            (0.0, 0.0),
            (1.0, 0.0),
        ])
        triangulator = Triangulator(point_set)

        triangles = triangulator.triangulate()

        assert len(triangles) == 0

    def test_triangulate_collinear_points(self):
        point_set = PointSet([
            (0.0, 0.0),
            (1.0, 0.0),
            (2.0, 0.0),
        ])
        triangulator = Triangulator(point_set)

        triangles = triangulator.triangulate()

        assert len(triangles) == 0


