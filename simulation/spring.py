import math
from .core import Point, PhysicalPoint
from .config import MODO_DEBUG

class SpringConstraint:
    def __init__(self, point_a, point_b, length, stiffness, damping=0.1):
        self.point_a = point_a
        self.point_b = point_b
        self.length = length
        self.stiffness = stiffness
        self.damping = damping

    def distance(self):
        dx = self.point_b.x - self.point_a.x
        dy = self.point_b.y - self.point_a.y
        return math.hypot(dx, dy)

    def get_force_direction(self):
        dist = self.distance()
        if dist == 0:
            return Point(0, 0)
        return Point((self.point_b.x - self.point_a.x) / dist,
                     (self.point_b.y - self.point_a.y) / dist)

    def get_spring_force(self):
        dist = self.distance()
        direction = self.get_force_direction()
        force_magnitude = self.stiffness * (dist - self.length)
        return Point(direction.x * force_magnitude, direction.y * force_magnitude)

    def get_damping_force(self):
        va = self.point_a.velocity if isinstance(self.point_a, PhysicalPoint) else Point(0, 0)
        vb = self.point_b.velocity if isinstance(self.point_b, PhysicalPoint) else Point(0, 0)

        relative_velocity = Point(vb.x - va.x, vb.y - va.y)

        return Point(-self.damping * relative_velocity.x, -self.damping * relative_velocity.y)

    def update(self):
        if not isinstance(self.point_a, PhysicalPoint) and not isinstance(self.point_b, PhysicalPoint):
            return

        spring_force = self.get_spring_force()
        damping_force = self.get_damping_force()
        total_force = Point(spring_force.x + damping_force.x, spring_force.y + damping_force.y)

        if isinstance(self.point_a, PhysicalPoint):
            self.point_a.apply_force(total_force)
        if isinstance(self.point_b, PhysicalPoint):
            self.point_b.apply_force(Point(-total_force.x, -total_force.y))

        if MODO_DEBUG:
            print(f"[DEBUG] Distancia resorte: {self.distance():.2f}")
