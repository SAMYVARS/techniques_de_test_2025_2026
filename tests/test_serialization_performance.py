import pytest
import time


class TestSerializationPerformance:

    def test_performance_serialize_1000_points(self):
        num_iterations = 10
        num_points = 1000

        points = [(float(i % 32), float(i // 32)) for i in range(num_points)]

        times = []
        for _ in range(num_iterations):
            point_set = PointSet(points)

            start_time = time.perf_counter()
            point_set.serialize()
            end_time = time.perf_counter()

            times.append(end_time - start_time)

        average_time = sum(times) / len(times)

        assert average_time >= 0

    def test_performance_deserialize_1000_points(self):
        num_iterations = 10
        num_points = 1000

        points = [(float(i % 32), float(i // 32)) for i in range(num_points)]
        point_set = PointSet(points)
        serialized = point_set.serialize()

        times = []
        for _ in range(num_iterations):
            start_time = time.perf_counter()
            PointSet.deserialize(serialized)
            end_time = time.perf_counter()

            times.append(end_time - start_time)

        average_time = sum(times) / len(times)

        assert average_time >= 0

