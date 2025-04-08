import pygame
from .core import PhysicalPoint, Point, Line, RectangleCollider
from .config import MODO_DEBUG

class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = []
        self.lines = []
        self.constraints = []
        self.colliders = []
        self.running = True
        self.delta_time = 0

    def add_point(self, point):
        self.points.append(point)

    def add_colider(self, collider):
        self.colliders.append(collider)

    def add_line(self, line):
        self.lines.append(line)

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def apply_constraints(self):
        for constraint in self.constraints:
            constraint.update()

    def update_points(self, delta_time, colliders=[]):
        for point in self.points:
            if isinstance(point, PhysicalPoint):
                point.update(delta_time, colliders)

    def draw(self, screen):
        for point in self.points:
            point.draw(screen)
        for line in self.lines:
            line.draw(screen)
        for collider in self.colliders:
            collider.draw(screen)

    def run(self, screen, loop=None, background_color=(0, 0, 0)):
        clock = pygame.time.Clock()
        while self.running:
            self.delta_time = clock.tick(60) / 1000.0
            self.handle_events()
            screen.fill(background_color)

            self.apply_constraints()
            self.update_points(self.delta_time, self.colliders)
            self.draw(screen)

            if loop:
                loop()
            pygame.display.flip()
        pygame.quit()
