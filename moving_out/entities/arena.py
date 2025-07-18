import pymunk as pm
from moving_out import render as r
from moving_out.env_parameters import ARENA_SEGMENT_FRICTION, COLORS_RGB

from .base import Entity

# pytype: disable=attribute-error


class ArenaBoundaries(Entity):
    """Handles physics of arena boundaries to keep everything in one place."""

    def __init__(self, left, right, top, bottom, seg_rad=1):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.seg_rad = seg_rad

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        # thick line segments around the edges
        arena_body = pm.Body(body_type=pm.Body.STATIC)

        self.add_to_space([arena_body])

        rad = self.seg_rad
        points = [
            (self.left - rad, self.top + rad),
            (self.right + rad, self.top + rad),
            (self.right + rad, self.bottom - rad),
            (self.left - rad, self.bottom - rad),
        ]
        arena_segments = []
        for start_point, end_point in zip(points, points[1:] + points[:1]):
            segment = pm.Segment(arena_body, start_point, end_point, rad)
            segment.friction = ARENA_SEGMENT_FRICTION
            arena_segments.append(segment)
        self.add_to_space(*arena_segments)

        width = self.right - self.left
        height = self.top - self.bottom
        arena_square = r.make_rect(width, height, True)
        arena_square.color = (1, 1, 1)
        arena_square.outline_color = COLORS_RGB["grey"]
        txty = (self.left + width / 2, self.bottom + height / 2)
        centre_xform = r.Transform(translation=txty)
        arena_square.add_transform(centre_xform)

        friction_layer = pm.Poly.create_box(arena_body, (width, height))
        friction_layer.sensor = True
        self.add_to_space([friction_layer])

        self.viewer.add_geom(arena_square)
