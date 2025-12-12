"""Module for managing sets of 2D points."""

import struct


class PointSet:
    """A class representing a set of 2D points."""

    def __init__(self, points=None):
        """Initialize the PointSet with a list of points."""
        self.points = points if points is not None else []

    def __len__(self):
        """Return the number of points in the set."""
        return len(self.points)

    def __getitem__(self, index):
        """Get a point by its index."""
        return self.points[index]

    def serialize(self) -> bytes:
        """Serialize the PointSet to a binary format.

        Format:
        - 4 bytes: number of points (unsigned int)
        - For each point:
          - 4 bytes: x (float)
          - 4 bytes: y (float)
        """
        n = len(self.points)
        # I = unsigned int (4 bytes), f = float (4 bytes)
        # Header
        data = struct.pack('>I', n)
        # Points
        for x, y in self.points:
            data += struct.pack('>ff', x, y)
        return data

    @classmethod
    def deserialize(cls, data: bytes) -> 'PointSet':
        """Deserialize a PointSet from binary data."""
        if len(data) < 4:
            raise ValueError("Invalid binary format: too short for header")
        
        n = struct.unpack('>I', data[:4])[0]
        expected_size = 4 + n * 8
        if len(data) != expected_size:
            raise ValueError(
                f"Invalid binary format: expected {expected_size} bytes, "
                f"got {len(data)}"
            )
        
        points = []
        offset = 4
        for _ in range(n):
            x, y = struct.unpack('>ff', data[offset:offset+8])
            points.append((x, y))
            offset += 8
            
        return cls(points)
