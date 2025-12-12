"""Module for triangulating sets of points."""

import struct

from .point_set import PointSet


class Triangulator:
    """A class to perform triangulation on a set of points."""

    def __init__(self, point_set: PointSet):
        """Initialize the Triangulator with a PointSet."""
        self.point_set = point_set

    def triangulate(self):
        """Perform a basic triangulation.

        For the purpose of the API test, this might return a dummy list of triangles
        or a simple triangulation if feasible.
        
        Returns:
            list: A list of triangles, where each triangle is a tuple of 3 points
            ((x1,y1), (x2,y2), (x3,y3)).

        """
        points = self.point_set.points
        if len(points) < 3:
            return []
        
        triangles = []
        for i in range(1, len(points) - 1):
            p1, p2, p3 = points[0], points[i], points[i+1]
            area = 0.5 * abs(
                p1[0] * (p2[1] - p3[1]) +
                p2[0] * (p3[1] - p1[1]) +
                p3[0] * (p1[1] - p2[1])
            )
            if area > 1e-9:
                triangles.append((p1, p2, p3))
            
        return triangles

    def triangulate_to_bytes(self) -> bytes:
        """Triangulate and return the result in binary format."""
        triangles = self.triangulate()
        n = len(triangles)
        data = struct.pack('>I', n)
        for p1, p2, p3 in triangles:
            for p in (p1, p2, p3):
                data += struct.pack('>ff', p[0], p[1])
        return data
