"""Tests for PointSet serialization."""

from src.triangulator.point_set import PointSet


class TestPointSetSerialization:
    """Test suite for PointSet serialization and deserialization."""

    def test_serialize_empty_pointset(self):
        """Test serializing an empty PointSet."""
        point_set = PointSet([])

        serialized = point_set.serialize()

        assert len(serialized) == 4

    def test_serialize_single_point(self):
        """Test serializing a PointSet with a single point."""
        point_set = PointSet([
            (1.0, 2.0),
        ])

        serialized = point_set.serialize()

        assert len(serialized) == 12

    def test_serialize_multiple_points(self):
        """Test serializing a PointSet with multiple points."""
        point_set = PointSet([
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 2.0),
        ])

        serialized = point_set.serialize()

        assert len(serialized) == 28

    def test_serialize_deserialize_pointset(self):
        """Test round-trip serialization and deserialization."""
        original_points = [
            (0.0, 0.0),
            (1.0, 0.0),
            (0.0, 1.0),
        ]
        point_set = PointSet(original_points)

        serialized = point_set.serialize()
        deserialized = PointSet.deserialize(serialized)

        assert len(deserialized) == len(point_set)

