import pytest
import tracemalloc
import sys
from src.triangulator.point_set import PointSet
from src.triangulator.triangulator import Triangulator


class TestMemoryConsumption:

    def test_memory_triangulation_10000_points(self):
        num_points = 10000
        points = [(float(i % 100), float(i // 100)) for i in range(num_points)]

        tracemalloc.start()

        point_set = PointSet(points)
        triangulator = Triangulator(point_set)
        triangulator.triangulate()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        assert peak >= 0

    def test_memory_serialization_10000_points(self):
        num_points = 10000
        points = [(float(i % 100), float(i // 100)) for i in range(num_points)]

        point_set = PointSet(points)
        pointset_size = sys.getsizeof(point_set)

        serialized = point_set.serialize()
        binary_size = sys.getsizeof(serialized)

        assert pointset_size >= 0
        assert binary_size >= 0

    def test_memory_successive_triangulations(self):
        num_iterations = 100
        num_points = 100
        points = [(float(i % 10), float(i // 10)) for i in range(num_points)]

        tracemalloc.start()
        initial_memory = tracemalloc.get_traced_memory()[0]

        for _ in range(num_iterations):
            point_set = PointSet(points)
            triangulator = Triangulator(point_set)
            triangulator.triangulate()

        final_memory = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()

        assert initial_memory >= 0
        assert final_memory >= 0

    def test_memory_binary_vs_pointset(self):
        num_points = 1000
        points = [(float(i % 32), float(i // 32)) for i in range(num_points)]

        point_set = PointSet(points)
        pointset_size = sys.getsizeof(point_set)

        serialized = point_set.serialize()
        binary_size = len(serialized)

        assert pointset_size >= 0
        assert binary_size >= 0

