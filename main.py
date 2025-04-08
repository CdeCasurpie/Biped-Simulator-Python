import pygame
from simulation.core import PhysicalPoint, Point, Line, RectangleCollider
from simulation.spring import SpringConstraint
from simulation.engine import Simulation
from simulation.biped import Biped
from simulation import config


def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Simulación de Resortes")
    return screen



def main():
    config.AMORTIGUACION = 0.97

    sim = Simulation(config.WIDTH, config.HEIGHT)

    point_a = PhysicalPoint(300, 200, mass=10)
    point_b = Point(400, 200)

    point_a.radius = 10
    point_a.color = (255, 0, 0)
    point_b.radius = 5
    point_b.color = (0, 255, 0)

    spring = SpringConstraint(point_a, point_b, length=10, stiffness=250, damping=0.0)
    line = Line(point_a, point_b)


    collider = RectangleCollider(300, 300, 150, 200)
    collider.color = (0, 0, 255) 
    sim.add_colider(collider)



    sim.add_point(point_a)
    sim.add_point(point_b)
    sim.add_constraint(spring)
    sim.add_line(line)

    biped = Biped(100,100,speed=200)

    def loop():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        point_b.x = mouse_x
        point_b.y = mouse_y

        biped.handle_input(delta_time=sim.delta_time)
        biped.draw(screen)
        biped.update(deltatime=sim.delta_time)

    # Initialize game
    screen = initialize_game()
    sim.run(screen, loop, background_color=(20, 20, 20))

if __name__ == "__main__":
    main()
