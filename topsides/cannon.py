import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# keeping here just in case pixel function doesn't work
#def cannon_volume(r1, r2, r3, l):
#    vol_out = (1/3) * np.pi * (r3**2 + r3*r1 + r1**2) * l
#    vol_in = np.pi * r2**2 * l
#    return vol_out - vol_in

def cannon_volume(p_brick, p_d1, p_d2, p_d3, p_l, p_d1_2):
    BRICK = 19
    l = (BRICK * p_l) / p_brick
    r3 = (BRICK * p_d3) / (p_brick * 2)
    r1 = (BRICK * p_d1) / (p_brick * 2)
    d1 = 2 * r1
    r2 = (d1 * p_d2) / (p_d1_2 * 2)
    vol_out = (1/3) * np.pi * (r3**2 + r3*r1 + r1**2) * l
    vol_in = np.pi * r2**2 * l
    return vol_out - vol_in

if __name__ == "__main__":
    print('Brick Length?')
    p_brick = input()
    print('Cannon Length?')
    p_l = input()
    print('Diameter 1? (side)')
    p_d1 = input()
    print('Diameter 3? (side)')
    p_d3 = input()
    print('Diameter 1? (front)')
    p_d1_2 = input()
    print('Diameter 2? (front)')
    p_d2 = input()


    vol = cannon_volume(float(p_brick), float(p_d1), float(p_d2), float(p_d3), float(p_l), float(p_d1_2),)
    print("Cannon Volume: " + str(vol))
