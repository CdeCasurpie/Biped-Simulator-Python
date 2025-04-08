from simulation.core import Point, PhysicalPoint, Line, RectangleCollider
from simulation.config import *
from simulation.spring import SpringConstraint

import pygame

import math


class Biped:
    def __init__(self, x, y, speed=5):
        self.x = x
        self.y = y
        self.points = []
        self.constraints = []
        self.lines = []
        self.speed = speed
        self.initial_speed = speed
        self.step_height = 30
        self.thigh_length = 100
        self.calf_length = 70
        self.ideal_center = x
        self.distance_bween_legs = 70
        self.t_acumm = 0
        self.direction = "right"


        # el bipedo consistira de dos piernas y una cadera, la cadera sera un punto fisico
        # este punto estará sostenido por un resorte superior en un punto fijo con coordenadas
        # x e y. las coordenadas del bipedo son las dadas en el constructor
        # el punto de la cadera es un punto fisico
        
        self.main_point = Point(x, y)
        self.main_point.radius = 5
        self.hip = PhysicalPoint(x, y+50, mass=10)
        self.hip.radius = 10

        self.constraints.append(SpringConstraint(self.hip, self.main_point, 50, 1000/2, 0))

        # luego existen los dos pies, que son puntos fijos, de modo que solo se moveran si lo decidimos
        self.foot_left = Point(x-20, y+180)
        self.foot_left.radius = 7
        self.foot_right = Point(x+20, y+180)
        self.foot_right.radius = 7


        self.foot_left_target = Point(x-20, y+180)
        self.foot_right_target = Point(x+20, y+180)

        self.past_left_foot = Point(x-20, y+180)
        self.past_right_foot = Point(x+20, y+180)

        # luego entre la cadera y los pies existen els dos muslos, que son puntos fijos también
        # sus coordenadas se calculan en base a las coordenadas de la cadera y los pies con 
        # inverse kinematicas
        self.thigh_left = Point(0, 0)
        self.thigh_left.radius = 5
        self.thigh_right = Point(0, 0)
        self.thigh_right.radius = 5

        # las pienas se dibujan con una linea desde la cadera hasta los muslos y de los muslos hasta
        # los pies
        self.lines.append(Line(self.hip, self.thigh_right))
        self.lines.append(Line(self.hip, self.thigh_left))
        self.lines.append(Line(self.thigh_left, self.foot_left, color=(255, 0, 0)))
        self.lines.append(Line(self.thigh_right, self.foot_right, color=(0, 0, 255)))


        self.points.append(self.hip)
        self.points.append(self.main_point)

    def draw(self, screen):
        for point in self.points:
            point.draw(screen)
        for line in self.lines:
            line.draw(screen)

        # drawo directional point
        directional_point = self.get_directional_point()
        directional_point.radius = 5
        directional_point.color = (0, 255, 0)
        directional_point.draw(screen)

        # dibujar centro ideal como una linea vertical desde el main point hasta los pies
        pygame.draw.line(screen, (255, 0, 0), (self.ideal_center, self.main_point.y), (self.ideal_center, self.foot_left.y), 1)
    
    def get_step_height(self):
        # Aumenta la altura del paso proporcionalmente a la velocidad, con un mínimo de 1x
        multiplier = max(1, self.speed / self.initial_speed)
        return self.step_height * multiplier

    def get_distance_between_legs(self):
        # Aumenta la distancia entre las piernas proporcionalmente a la velocidad, con un mínimo de 1x
        multiplier = max(1, self.speed / self.initial_speed)
        return self.distance_bween_legs * multiplier

    def handle_stability(self):
        # si el centro ideal no está entre las dos piernas mover la que está más alejada
        x_max = max(self.foot_left_target.x, self.foot_right_target.x)
        foot_max = self.foot_left_target if self.foot_left_target.x == x_max else self.foot_right_target
        foot_min = self.foot_right_target if self.foot_left_target.x == x_max else self.foot_left_target

        # foot_max es el pie más alejado del centro ideal
        # foot_min es el pie más cercano al centro ideal

        if self.ideal_center < foot_min.x:
            moving_foot = "left" if foot_max == self.foot_left_target else "right"
            if moving_foot == "left":
                self.past_left_foot.x = foot_max.x
                self.past_right_foot.x = foot_min.x
            else:
                self.past_right_foot.x = foot_max.x
                self.past_left_foot.x = foot_min.x
            foot_max.x = self.ideal_center - self.get_distance_between_legs()
            self.t_acumm = 0
        elif self.ideal_center > foot_max.x:
            moving_foot = "right" if foot_max == self.foot_left_target else "left"
            if moving_foot == "left":
                self.past_left_foot.x = foot_min.x
                self.past_right_foot.x = foot_max.x
            else:
                self.past_right_foot.x = foot_min.x
                self.past_left_foot.x = foot_max.x
            foot_min.x = self.ideal_center + self.get_distance_between_legs()
            self.t_acumm = 0

    def move_foots(self, deltatime):
        local_speed = 2.5
        def move_foot_x(foot, target):
            if abs(foot.x - target.x) < 1:
                foot.x = target.x
            elif foot.x < target.x:
                foot.x += min(local_speed * self.speed * deltatime, target.x - foot.x)
            elif foot.x > target.x:
                foot.x -= min(local_speed * self.speed * deltatime, foot.x - target.x)
        
        def move_foot_y(foot, target, past_foot):
            # Calculate step duration based on horizontal distance
            t_step = (abs(target.x - past_foot.x))/(local_speed * self.speed)
            
            if t_step > 0:
                # Calculate vertical speed for the triangular movement
                v_y = 2 * self.get_step_height() / t_step
                
                # Progress ratio - how far we are in the step (0 to 1)
                progress = min(1.0, self.t_acumm / t_step)
                
                if progress < 0.5:
                    # First half - lifting phase (0 to 0.5)
                    # Calculate target height at this point in time
                    target_height = target.y - self.get_step_height() * (progress * 2)
                    # Move towards that height with appropriate speed
                    foot.y = max(foot.y - v_y * deltatime, target_height)
                else:
                    # Second half - lowering phase (0.5 to 1.0)
                    # Calculate target height at this point in time
                    downward_progress = (progress - 0.5) * 2  # 0 to 1
                    target_height = (target.y - self.get_step_height()) + self.get_step_height() * downward_progress
                    # Move towards that height with appropriate speed
                    foot.y = min(foot.y + v_y * deltatime, target_height)
                
                # If we've completed the step cycle, ensure foot is at target position
                if progress >= 1.0:
                    foot.y = target.y
                
                self.t_acumm += deltatime

        move_foot_x(self.foot_left, self.foot_left_target)
        move_foot_x(self.foot_right, self.foot_right_target)
        move_foot_y(self.foot_left, self.foot_left_target, self.past_left_foot)
        move_foot_y(self.foot_right, self.foot_right_target, self.past_right_foot)

    def inverse_kinematics(self, hip, foot, upper_length, lower_length, target=Point(0, 0)):
        #output rodilla
        def get_intersections_of_circles(C1, C2, l1, l2):
            d = math.sqrt((C2.x - C1.x)**2 + (C2.y - C1.y)**2)
            if d > l1 + l2 or d < abs(l1 - l2):
                return None, None  # No intersection

            a = (l1**2 - l2**2 + d**2) / (2 * d)
            h = math.sqrt(l1**2 - a**2)

            x0 = C1.x + a * (C2.x - C1.x) / d
            y0 = C1.y + a * (C2.y - C1.y) / d

            rx = -(C2.y - C1.y) * (h / d)
            ry = (C2.x - C1.x) * (h / d)

            intersection1 = Point(x0 + rx, y0 + ry)
            intersection2 = Point(x0 - rx, y0 - ry)

            return intersection1, intersection2

        intersections = get_intersections_of_circles(hip, foot, upper_length, lower_length)

        if intersections[0] is None:
            return Point((hip.x + foot.x) / 2, (hip.y + foot.y) / 2)
        
        p1, p2 = intersections

        if p1.distance(target) < p2.distance(target):
            return p1
        else:
            return p2
        
        
    

    def get_directional_point(self):
        if self.direction == "left":
            return Point(self.main_point.x - 100, self.main_point.y + 100)
        else:
            return Point(self.main_point.x + 100, self.main_point.y + 100)


    def update(self, deltatime):
        self.ideal_center = self.hip.x

        # calcular posición de los muslos
        left = self.inverse_kinematics(self.hip, self.foot_left, self.thigh_length, self.calf_length, self.get_directional_point())
        right = self.inverse_kinematics(self.hip, self.foot_right, self.thigh_length, self.calf_length, self.get_directional_point())


        self.thigh_left.x = left.x
        self.thigh_left.y = left.y
        self.thigh_right.x = right.x
        self.thigh_right.y = right.y

        for con in self.constraints:
            con.update()

        for point in self.points:
            if isinstance(point, PhysicalPoint):
                point.update(deltatime)

        self.handle_stability()
        self.move_foots(deltatime=deltatime)

    def handle_input(self, delta_time=0.016):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.main_point.x -= self.speed* delta_time
            if keys[pygame.K_RIGHT]:
                self.main_point.x += self.speed* delta_time
                self.direction = "right"
            if keys[pygame.K_UP]:
                self.main_point.y -= self.speed* delta_time
            if keys[pygame.K_DOWN]:
                self.main_point.y += self.speed* delta_time
            if keys[pygame.K_u]:
                self.speed += 1
            if keys[pygame.K_y]:
                self.speed -= 1
