from simulation.core import Point
import math

# PARAMETROS
ALPHA = math.pi/4 # 45º maximo angulo entre l1 y la horzontal
BETA = math.pi/16 # 11.25º minimo angulo entre l1 y l2
GAMMA = math.pi/2 + BETA

# A is the center of the circle
# T is the point out of the circle
#l1 is the radius of the circle
def find_p(A, T, l1):
    v = T - A
    v_unit = v.normalize()
    return A + v_unit * l1

def inverse_kinematic(A, B, l1, l2, T):
    p = find_p(A, T, l1) # p es la rodilla

    v = T - A
    v_unit = v.normalize()

    v_unit = v_unit.rotate(GAMMA)

    new_B = p + v_unit * l2 # new_B es el pie
    
    return A, p, new_B

def main():
    A = Point(5, 5)
    B = Point(8, 12)
    l1 = 5
    l2 = 4

    T = Point(12,6)

    A, p, new_B = inverse_kinematic(A, B, l1, l2, T)

    print(f"A: {A}")
    print(f"p: {p}")
    print(f"new_B: {new_B}")

main()



    

























# te amo amor, no lo pienses mucho. tqm. enserio te quiero. :3
# como que no lo piense mucho, tutu malo, yo esoty pensando poquito y me canso pq nunc apineso :TT todos tristes