"""Triangulation performance tests."""

import time

import pytest

from src.triangulator.point_set import PointSet
from src.triangulator.triangulator import Triangulator


@pytest.mark.performance
class TestTriangulationPerformance:
    """Tests for triangulation performance."""

    def test_performance_triangulate_100_points(self):
        """Measure time to triangulate 100 points."""
        num_iterations = 10
        num_points = 100

        points = [(float(i % 10), float(i // 10)) for i in range(num_points)]

        times = []
        for _ in range(num_iterations):
            point_set = PointSet(points)
            triangulator = Triangulator(point_set)

            start_time = time.perf_counter()
            triangulator.triangulate()
            end_time = time.perf_counter()

            times.append(end_time - start_time)

        average_time = sum(times) / len(times)

        assert average_time >= 0

    def test_performance_triangulate_1000_points(self):
        """Measure time to triangulate 1,000 points."""
        num_iterations = 10
        num_points = 1000

        points = [(float(i % 32), float(i // 32)) for i in range(num_points)]

        times = []
        for _ in range(num_iterations):
            point_set = PointSet(points)
            triangulator = Triangulator(point_set)

            start_time = time.perf_counter()
            triangulator.triangulate()
            end_time = time.perf_counter()

            times.append(end_time - start_time)

        average_time = sum(times) / len(times)

        assert average_time >= 0

    def test_performance_triangulate_10000_points(self):
        """Measure time to triangulate 10,000 points."""
        num_iterations = 5
        num_points = 10000

        points = [(float(i % 100), float(i // 100)) for i in range(num_points)]

        times = []
        for _ in range(num_iterations):
            point_set = PointSet(points)
            triangulator = Triangulator(point_set)

            start_time = time.perf_counter()
            triangulator.triangulate()
            end_time = time.perf_counter()

            times.append(end_time - start_time)

        average_time = sum(times) / len(times)

        assert average_time >= 0

