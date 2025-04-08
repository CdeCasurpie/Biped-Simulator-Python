import pygame
from .config import GRAVITY, AMORTIGUACION, MODO_DEBUG
import math

def segment_intersection(p1, p2, q1, q2):
    """
    Retorna el punto de intersección entre los segmentos p1-p2 y q1-q2
    o None si no se intersectan.
    """
    def det(a, b):
        return a.x * b.y - a.y * b.x

    r = p2 - p1
    s = q2 - q1
    denominator = det(r, s)

    if denominator == 0:
        return None  # segmentos paralelos o colineales

    diff = q1 - p1
    t = det(diff, s) / denominator
    u = det(diff, r) / denominator

    if 0 <= t <= 1 and 0 <= u <= 1:
        intersection = Point(p1.x + t * r.x, p1.y + t * r.y)
        return intersection
    return None


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 255, 255)
        self.radius = 2

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def norm(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        norm = self.norm()
        if norm == 0:
            return Point(0, 0)
        return Point(self.x / norm, self.y / norm)

    def rotate(self, angle):
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        return Point(self.x * cos_angle - self.y * sin_angle,
                     self.x * sin_angle + self.y * cos_angle)

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Line:
    def __init__(self, start, end, color = (255, 255, 255), width=2):
        self.start = start
        self.end = end
        self.color = color
        self.width = width

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (int(self.start.x), int(self.start.y)),
                         (int(self.end.x), int(self.end.y)), self.width)

class PhysicalPoint(Point):
    def __init__(self, x, y, mass):
        super().__init__(x, y)
        self.mass = mass
        self.velocity = Point(0, 0)
        self.acceleration = Point(0, 0)

    def apply_force(self, force):
        self.acceleration.x += force.x / self.mass
        self.acceleration.y += force.y / self.mass


    def calculate_intersection(self, collider, point=None):
        prev_pos = Point(self.x, self.y)

        direction = self.velocity.normalize()
        next_pos = Point(self.x + direction.x * self.radius, self.y + direction.y * self.radius)

        # Bordes del rectángulo
        top_left = Point(collider.x, collider.y)
        top_right = Point(collider.x + collider.width, collider.y)
        bottom_left = Point(collider.x, collider.y + collider.height)
        bottom_right = Point(collider.x + collider.width, collider.y + collider.height)

        edges = [
            (top_left, top_right),      # Top
            (top_right, bottom_right),  # Right
            (bottom_right, bottom_left),# Bottom
            (bottom_left, top_left)     # Left
        ]

        for edge_start, edge_end in edges:
            intersection = segment_intersection(prev_pos, next_pos, edge_start, edge_end)
            if intersection:
                return intersection, (edge_end - edge_start).normalize()

        # Colisión con esquinas
        corners = [top_left, top_right, bottom_left, bottom_right]
        for corner in corners:
            to_center = next_pos - corner
            if to_center.norm() < self.radius:
                normal = to_center.normalize()
                intersection = Point(corner.x + normal.x * self.radius, corner.y + normal.y * self.radius)
                return intersection, normal

        return None, None


    def update_chords(self, delta_time, colliders=[]):
        sub_steps = 5  # Divide el movimiento en subpasos
        sub_time = delta_time / sub_steps
        
        for _ in range(sub_steps):
            new_pos = Point(self.x + self.velocity.x * sub_time, self.y + self.velocity.y * sub_time)
            for collider in colliders:
                if collider.collides_with(RectangleCollider(new_pos.x, new_pos.y, 1, 1), radius=self.radius):
                    intersection, tangent = self.calculate_intersection(collider, point=new_pos)
                    if intersection:
                        normal = Point(-tangent.y, tangent.x).normalize()
                        self.x = intersection.x + normal.x * -self.radius
                        self.y = intersection.y + normal.y * -self.radius

                        v_dot_n = self.velocity.x * normal.x + self.velocity.y * normal.y
                        self.velocity.x -= 2 * v_dot_n * normal.x
                        self.velocity.y -= 2 * v_dot_n * normal.y
                        return  # Colisión manejada, salimos
            self.x = new_pos.x
            self.y = new_pos.y




    def update(self, delta_time, colliders=[]):
        gravity_force = Point(0, GRAVITY * self.mass)
        self.apply_force(gravity_force)

        self.velocity.x += self.acceleration.x * delta_time
        self.velocity.y += self.acceleration.y * delta_time

        self.update_chords(delta_time, colliders)

        self.acceleration.x = 0
        self.acceleration.y = 0

        self.velocity.x *= AMORTIGUACION
        self.velocity.y *= AMORTIGUACION

        self.check_bounds(800, 600)

        if MODO_DEBUG:
            print(f"[DEBUG] Posición: ({self.x:.2f}, {self.y:.2f}) Vel: ({self.velocity.x:.2f}, {self.velocity.y:.2f})")

    def check_bounds(self, width, height):
        if self.x < 0:
            self.x = 0
            self.velocity.x *= -1
        elif self.x > width:
            self.x = width
            self.velocity.x *= -1

        if self.y < 0:
            self.y = 0
            self.velocity.y *= -1
        elif self.y > height:
            self.y = height
            self.velocity.y *= -1

class RectangleCollider:
    def __init__(self, x, y, width, height, drawable=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.drawable = drawable

    def draw(self, screen):
        if self.drawable:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 1)
        else:
            pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)
    
    def collides_with(self, point, radius=0):
        """
        point: instancia de Point o PhysicalPoint
        radius: radio del punto
        """
        # Expandimos el rectángulo un poco hacia afuera para simular el radio
        return (
            self.x - radius < point.x < self.x + self.width + radius and
            self.y - radius < point.y < self.y + self.height + radius
        )

    